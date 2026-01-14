# eta_incerto/plotting/scenario.py

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import h5py
import matplotlib.axes
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


@dataclass(frozen=True)
class ScenarioSeries:
    """A single (year, value) series for one scenario/carrier/metric."""

    years: np.ndarray
    values: np.ndarray


class ScenarioPlot:
    """
    Reads scenario carrier trajectories from an eta-incerto result HDF5 and plots:

    - For each carrier: a line plot (x=year) with one line per scenario
    - Can be embedded into an existing matplotlib Axes via plot_into(ax)

    Expected HDF5 layout (as in your example file):
      scenarios/<scenario_name>/carriers/<carrier_name>/<metric>/year
      scenarios/<scenario_name>/carriers/<carrier_name>/<metric>/value

    Metrics typically include: "unit_price", "emissions_per_unit"
    """

    def __init__(self, h5_path: Path):
        self.h5_path = Path(h5_path)

        # filled on demand
        self._scenario_names: list[str] | None = None
        self._carriers: list[str] | None = None
        self._probabilities: dict[str, float] | None = None

    # -----------------------------
    # public helpers
    # -----------------------------
    @property
    def scenario_names(self) -> list[str]:
        self._ensure_index()
        assert self._scenario_names is not None
        return self._scenario_names

    @property
    def carriers(self) -> list[str]:
        self._ensure_index()
        assert self._carriers is not None
        return self._carriers

    @property
    def probabilities(self) -> dict[str, float]:
        self._ensure_index()
        assert self._probabilities is not None
        return self._probabilities

    # -----------------------------
    # core plotting
    # -----------------------------
    def plot_into(
        self,
        ax: matplotlib.axes.Axes,
        *,
        metric: str = "unit_price",
        carriers: Iterable[str] | None = None,
        show_probability_in_legend: bool = True,
        legend: bool = True,
        legend_ncol: int = 3,
        title: str | None = None,
        xlabel: str = "year",
        ylabel_suffix: str | None = None,
        grid: bool = True,
    ) -> list[matplotlib.axes.Axes]:
        """
        Plot one small inset axis per carrier inside the provided `ax`.

        Returns a list of the created inset axes (top-to-bottom).
        """
        self._ensure_index()

        chosen_carriers = list(carriers) if carriers is not None else list(self.carriers)
        if not chosen_carriers:
            raise ValueError("No carriers found/selected to plot.")

        # Clear "container" axis; we will place inset axes inside it.
        ax.cla()
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

        if title:
            ax.set_title(title)

        # Load data for selected carriers
        data = self._load_metric(metric=metric, carriers=chosen_carriers)

        # Create stacked inset axes: N rows, full width
        n = len(chosen_carriers)
        pad = 0.02  # vertical padding fraction inside container
        height = (1.0 - pad * (n + 1)) / n
        inset_axes_list: list[matplotlib.axes.Axes] = []

        line_styles = ["-", "--", ":", "-."]  # continuous, dashed, dotted, dash-dot
        style_map = {s: line_styles[i % len(line_styles)] for i, s in enumerate(self.scenario_names)}

        for i, carrier in enumerate(chosen_carriers):
            # bbox_to_anchor uses (x0, y0, width, height) in axes fraction coords
            y0 = 1.0 - pad - (i + 1) * height - i * pad
            iax = inset_axes(
                ax,
                width="100%",
                height="100%",
                bbox_to_anchor=(0.0, y0, 1.0, height),
                bbox_transform=ax.transAxes,
                loc="lower left",
                borderpad=0.0,
            )

            # Plot all scenarios for this carrier
            df_union = data[carrier]  # index: year, columns: scenario
            for scen in df_union.columns:
                label = scen
                if show_probability_in_legend:
                    p = self.probabilities.get(scen, None)
                    if p is not None:
                        label = f"{scen} (p={p:.3f})"

                iax.plot(
                    df_union.index.values,
                    df_union[scen].values,
                    label=label,
                    linestyle=style_map.get(scen, "-"),
                    linewidth=1.8,
                    color="black",
                )

            if grid:
                iax.grid(True, alpha=0.25)

            # y-label per carrier
            ylab = carrier
            if ylabel_suffix:
                ylab = f"{carrier} {ylabel_suffix}"
            iax.set_ylabel(ylab)

            # only bottom axis gets x-label/ticks
            if i < n - 1:
                iax.set_xticklabels([])
                iax.set_xlabel("")
            else:
                iax.set_xlabel(xlabel, labelpad=-10)

            inset_axes_list.append(iax)

        # legend (above the top inset axis)
        if legend and inset_axes_list:
            top = inset_axes_list[2]

            leg = top.legend(
                loc="lower right",
                fontsize="small",
                ncol=legend_ncol,
                frameon=True,
                fancybox=True,
                framealpha=1.0,
            )
            frame = leg.get_frame()
            frame.set_facecolor("white")
            frame.set_edgecolor("0.7")
            frame.set_linewidth(0.8)

            leg.set_zorder(10)
            # prevent clipping when legend is outside axes
            leg.set_in_layout(False)

        return inset_axes_list

    # -----------------------------
    # internal loading
    # -----------------------------
    def _ensure_index(self) -> None:
        if self._scenario_names is not None and self._carriers is not None and self._probabilities is not None:
            return

        with h5py.File(self.h5_path, "r") as f:
            if "scenarios" not in f:
                raise KeyError(f"No 'scenarios' group found in {self.h5_path}")

            scen_group = f["scenarios"]
            scenario_names = sorted(scen_group.keys())
            if not scenario_names:
                raise ValueError(f"'scenarios' group is empty in {self.h5_path}")

            # infer carriers from first scenario
            first = scen_group[scenario_names[0]]
            if "carriers" not in first:
                raise KeyError(f"No 'carriers' group found under scenarios/{scenario_names[0]}")

            carriers = sorted(first["carriers"].keys())

            # probabilities per scenario (if present)
            probabilities: dict[str, float] = {}
            for s in scenario_names:
                prob_path = f"scenarios/{s}/probability"
                if prob_path in f:
                    probabilities[s] = float(np.array(f[prob_path])[()])
                else:
                    probabilities[s] = float("nan")

        self._scenario_names = scenario_names
        self._carriers = carriers
        self._probabilities = probabilities

    def _read_series(
        self,
        f: h5py.File,
        scenario: str,
        carrier: str,
        metric: str,
    ) -> ScenarioSeries:
        base = f"scenarios/{scenario}/carriers/{carrier}/{metric}"
        year_ds = f"{base}/year"
        val_ds = f"{base}/value"
        if year_ds not in f or val_ds not in f:
            raise KeyError(f"Missing dataset(s) for {base} (expected /year and /value).")

        years = np.array(f[year_ds])
        values = np.array(f[val_ds], dtype=float)

        # Basic sanity
        if years.shape != values.shape:
            raise ValueError(f"Shape mismatch at {base}: year{years.shape} vs value{values.shape}")

        return ScenarioSeries(years=years, values=values)

    def _load_metric(
        self,
        *,
        metric: str,
        carriers: list[str],
    ) -> dict[str, pd.DataFrame]:
        """
        Returns {carrier: DataFrame(index=year, columns=scenario, values=metric_value)}.
        """
        self._ensure_index()
        out: dict[str, pd.DataFrame] = {}

        with h5py.File(self.h5_path, "r") as f:
            for carrier in carriers:
                # read all scenarios into aligned dataframe
                series_by_scenario: dict[str, ScenarioSeries] = {}
                for scen in self.scenario_names:
                    series_by_scenario[scen] = self._read_series(f, scen, carrier, metric)

                # align on union of years
                all_years = sorted(set(np.concatenate([v.years for v in series_by_scenario.values()])))
                df_union = pd.DataFrame(index=pd.Index(all_years, name="year"))

                for scen, s in series_by_scenario.items():
                    tmp = pd.Series(s.values, index=s.years, name=scen)
                    df_union[scen] = tmp.reindex(df_union.index).astype(float)

                out[carrier] = df_union

        return out
