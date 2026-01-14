from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from numpy import asarray, inf, mean, nan
from pandas import DataFrame, MultiIndex, read_csv, to_datetime
from tsam.timeseriesaggregation import TimeSeriesAggregation

if TYPE_CHECKING:
    from eta_incerto.config.config import ConfigOptimization
    from eta_incerto.config.config_series import SeriesFile

log = getLogger(__name__)


class TypicalData:
    """
    Generate seasonal typical periods (summer, winter, transition) from a single
    """

    def __init__(self, config: ConfigOptimization):
        self.config = config

    def _build_feature_weights(self, sf: SeriesFile, series_names: list[str]) -> dict[str, float]:
        # convert std_target in array of floats
        sf.std_target = asarray(sf.std_target, dtype=float)
        # normalize the weights
        sf.std_target = sf.std_target / float(mean(sf.std_target))
        # build dictionary
        return {name: float(w) for name, w in zip(series_names, sf.std_target)}

    def _split_into_seasons(self, df: DataFrame) -> Mapping[str, DataFrame]:
        """
        Winter  : Dec to Feb (12, 1, 2)
        Summer  : Jun to Aug (6, 7, 8)
        Transition: Mar to May + Sep to Nov (3, 4, 5, 9, 10, 11)
        """
        months = df.index.month
        winter_m = (12, 1, 2)
        summer_m = (6, 7, 8)
        trans_m = (3, 4, 5, 9, 10, 11)
        return {
            "summer": df[months.isin(summer_m)],
            "winter": df[months.isin(winter_m)],
            "transition": df[months.isin(trans_m)],
        }

    def _trim_to_complete_periods(self, df: DataFrame, len_period: int) -> DataFrame:
        """Make sure, that only whole periods are included in later steps. It is sampled
        for hours, so len_period=24 requires at least one day per season. Therefore, derives
        for each season, the number of full days available.
        """
        n = (len(df) // len_period) * len_period
        return df.iloc[:n, :]

    def _aggregate_season(
        self,
        df: DataFrame,
        sf: SeriesFile,
        *,
        weight_dict: Mapping[str, float],
    ) -> TimeSeriesAggregation:
        """
        Run TSAM on a single season. Uses hierarchical clustering, medoid representation,
        and rescaled cluster periods.
        """
        agg = TimeSeriesAggregation(
            df,
            noTypicalPeriods=sf.n_typical_periods,
            hoursPerPeriod=sf.len_period,  # is this correct? As it is intended to check for days not hours?
            clusterMethod=sf.cluster_method,
            segmentation=False,
            weightDict=weight_dict,
            rescaleClusterPeriods=True,
        )
        _ = agg.createTypicalPeriods()
        return agg

    def _extract_weights_and_series(
        self,
        agg: TimeSeriesAggregation,
        global_offset: int,
        series_names: Iterable[str],
    ) -> tuple[dict[int, float], dict[str, dict[tuple[int, int], float]]]:
        """
        Map TSAM's cluster IDs to consecutive global period IDs starting at global_offset+1,
        extract per-season normalized weights and series values.
        """
        # cluster IDs in deterministic order (TSAM provides a list)
        cluster_ids: list[int] = list(agg.clusterPeriodIdx)
        id_map = {cid: (global_offset + i + 1) for i, cid in enumerate(cluster_ids)}

        # weights within this season, normalized to 1
        counts: Mapping[int, int] = agg.clusterPeriodNoOccur
        total = float(sum(counts.values())) if counts else 1.0
        season_weights = {id_map[cid]: float(cnt) / total for cid, cnt in counts.items()}

        # typical period series values
        raw = agg.clusterPeriodDict  # {attr_name: {(cid, step)-> value}}
        season_series: dict[str, dict[tuple[int, int], float]] = {name: {} for name in series_names}
        for name in series_names:
            if name not in raw:
                # TSAM may drop a column if it is entirely NaN; guard against that.
                log.warning("Attribute '%s' missing in TSAM output; filling zeros.", name)
                continue
            for (cid, step), val in raw[name].items():
                season_series[name][(id_map[cid], int(step) + 1)] = float(val)

        return season_weights, season_series

    def data_to_periods(self) -> None:
        """
        Main pipeline:
          1) Load & resample the combined CSV
          2) Ensure columns match configured series_names (apply aliases if needed)
          3) Split into seasons
          4) Run TSAM per season (k = n_periods // 3 per season)
          5) Combine results and save files into HDF5 + JSON
        """
        for sf in self.config.series.series_file:
            data_path = sf.raw_data_path
            df_demand_weather = read_csv(data_path)
            # convert first column to datetime
            time_col = df_demand_weather.columns[0]
            df_demand_weather[time_col] = to_datetime(
                df_demand_weather[time_col], format=sf.time_conversion_str, errors="raise"
            )
            # set date as index and sort for resampling
            df_demand_weather = df_demand_weather.set_index(time_col).sort_index()
            # resample according to method
            df_demand_weather = getattr(df_demand_weather.resample(f"{sf.step_length}h"), sf.resample_method)()
            # replace infinite values with NaN
            df_demand_weather = df_demand_weather.replace([inf, -inf], nan)
            # handle NaNs
            df_demand_weather = getattr(df_demand_weather, sf.nan_strategy)(sf.nan_value)
            # make sure columns are named correctly
            series_names = list(sf.series_names.keys())
            df_demand_weather = df_demand_weather[series_names]
            # build dictionary with weights for each series name
            weight_dict = self._build_feature_weights(sf, series_names)
            # split data into winter, summer, spring + autumn
            seasons = self._split_into_seasons(df_demand_weather)
            # number of typical periods per season
            n_tp_per_season = sf.n_typical_periods // 3

            # aggregate per season
            global_offset = 0
            combined_weights: dict[int, float] = {}
            combined_series: dict[str, dict[tuple[int, int], float]] = {name: {} for name in series_names}

            for season_name, season_df in seasons.items():
                if season_df.empty:
                    log.warning("Season '%s' has no data after filtering; skipping.", season_name)
                    # global offset makes sure, that ids are handed over; e.g. winter [1,2,3] global offset makes sure,
                    # that summer ist then [4,5,6] etc.
                    global_offset += n_tp_per_season
                    continue

            trimmed_df = self._trim_to_complete_periods(season_df, sf.len_period)
            if trimmed_df.empty:
                log.warning(
                    "Season '%s' had data but not enough to form at least one complete period of length %d; skipping.",
                    season_name,
                    sf.len_period,
                )
                global_offset += n_tp_per_season
                continue
            # create typical periods with TSAM and store in agg object
            agg = self._aggregate_season(season_df, sf, weight_dict=weight_dict)
            # translate internal TSAM cluster IDs and raw outputs into global typical period IDs
            season_weights, season_series = self._extract_weights_and_series(agg, global_offset, series_names)

            # Average seasons -> divide each season's normalized weights by 3 to avoid dominance by one season
            for gpid, w in season_weights.items():
                combined_weights[gpid] = combined_weights.get(gpid, 0.0) + w / 3.0
            # create global dict of values for one attribute
            for name in series_names:
                combined_series[name].update(season_series[name])

            global_offset += n_tp_per_season

            # Normalize combined weights to sum to 1
            total_w = sum(combined_weights.values())
            if total_w > 0:
                # guarantee now, that all weights now sum to exactly 1
                for k in list(combined_weights):
                    combined_weights[k] = float(combined_weights[k] / total_w)
            else:
                log.warning("No weights produced; falling back to uniform distribution.")
                k = sf.n_typical_periods
                combined_weights = {i + 1: 1.0 / k for i in range(k)}

            # save results
            out_dir = self.config.paths.series_dir / sf.file_name
            out_dir.mkdir(parents=True, exist_ok=True)

            # Save weights.json
            self._write_json(out_dir / "weights.json", {int(k): float(v) for k, v in sorted(combined_weights.items())})

            # Save all typical series into one HDF5 file
            hdf_path = out_dir / "typical_series.h5"
            if hdf_path.exists():
                hdf_path.unlink()  # overwrite if exists

            save_keys = dict(sf.series_names)
            for name in series_names:
                inner_key = save_keys.get(name, name)
                # Convert dict-of-tuples into a DataFrame for saving
                df_save = DataFrame.from_dict(combined_series[name], orient="index", columns=[inner_key])
                df_save.index = MultiIndex.from_tuples(df_save.index, names=["period", "step"])
                df_save.to_hdf(hdf_path, key=name, mode="a")

            log.info("Typical periods (series + weights) written to: %s", out_dir)

    @staticmethod
    def _write_json(path: Path, payload: Mapping) -> None:
        with path.open("w") as f:
            json.dump(payload, f)
