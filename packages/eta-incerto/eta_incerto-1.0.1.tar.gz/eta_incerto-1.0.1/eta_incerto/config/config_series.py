import json
from logging import getLogger
from pathlib import Path
from typing import Any, ClassVar

from numpy import arange
from pandas import DataFrame, HDFStore, Series, read_csv, read_hdf
from pydantic import BaseModel, Field, field_validator, model_validator

from eta_incerto.periods.data_to_periods import TypicalData

log = getLogger(__name__)


class SeriesFile(BaseModel):
    raw_data_path: Path
    series_names: dict[str, str]
    nan_strategy: str
    nan_value: int
    resample_method: str
    time_conversion_str: str
    len_period: int
    step_length: int
    n_typical_periods: int = Field(..., description="must be divisible by three")
    std_target: list[int]
    cluster_method: str
    file_name: str

    @field_validator("raw_data_path")
    @classmethod
    def check_file_exists(cls, v: Path):
        if not v.exists():
            raise ValueError(f"Series file not found: {v}")
        return v

    @field_validator("n_typical_periods", mode="before")
    @classmethod
    def period_plausibility(cls, n_typical_periods):
        if n_typical_periods % 3 != 0:
            raise ValueError("n_typical_periods must be divisible by 3 (for three seasons). Got %s", n_typical_periods)
        return n_typical_periods

    @model_validator(mode="after")
    def number_of_std(self):
        if len(self.std_target) != len(self.series_names):
            raise ValueError(
                "std_target with length %s must match series_names length %s",
                len(self.std_target),
                len(self.series_names),
            )
        return self


class ConfigSeries(BaseModel):
    series_file: list[SeriesFile]
    typical_cls: ClassVar[type] = TypicalData

    @staticmethod
    def extend_to_years_index(df_in: DataFrame, dims: Any) -> DataFrame:
        """Expand a (period, step)-indexed DataFrame across all simulation years."""
        value_temp = {}
        for (period, step), value in df_in.iloc[:, 0].items():
            for year in arange(1, dims.n_years * dims.year_length + 1, dims.year_length):
                value_temp[(year, period, step)] = value
        return Series(value_temp).to_frame(df_in.columns[0])

    @classmethod
    def load_typical_day(cls, config: dict, dims: Any, file_name: str) -> dict:
        """Load or build typical-day time series using HDF5."""

        typical_path = Path(config.paths.series_dir) / file_name
        hdf_path = typical_path / "typical_series.h5"

        # Generate if missing
        if not hdf_path.exists():
            log.info("No typical periods found. Generating them now...")
            typical = cls.typical_cls(config)
            typical.data_to_periods()  # writes typical_series.h5 + weights.json
        else:
            log.info("Typical periods already exist at %s. Skipping regeneration.", hdf_path)

        # get predefined value from series_names dict
        series_file_cfg = next(sf for sf in config.series.series_file if sf.file_name == file_name)

        # Load each series from HDF5 (keys are series names)
        with HDFStore(hdf_path, mode="r") as store:
            keys = [k.strip("/") for k in store]

        data = {}
        for series_name in keys:
            df_hdf = read_hdf(hdf_path, key=series_name)
            df_hdf = cls.extend_to_years_index(df_hdf, dims)

            if series_name not in series_file_cfg.series_names:
                raise KeyError(f"No mapping found for series '{series_name}' in config.series.series_names")

            target_key = series_file_cfg.series_names[series_name]

            data[series_name] = {target_key: df_hdf.iloc[:, 0].to_dict()}

        # Load weights
        weights_path = typical_path / "weights.json"
        with weights_path.open() as f:
            weights: dict = json.load(f)

        weights_new = {}
        for year in arange(1, dims.n_years * dims.year_length + 1, dims.year_length):
            weights_new = {
                **weights_new,
                **{
                    (year, int(key)): value * 8760 / (dims.n_time_steps * dims.step_length)
                    for key, value in weights.items()
                },
            }
        data["weights"] = weights_new
        return data

    @classmethod
    def load_series_df(cls, config: dict, file_name: str) -> DataFrame:
        """Loads the"""

        series_folder_path = Path(config.paths.series_dir) / file_name
        df_path = series_folder_path / "series.csv"
        return read_csv(df_path)
