from __future__ import annotations

import logging
from pathlib import Path
from typing import ClassVar

import h5py
import matplotlib.axes
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

logger = logging.getLogger(__name__)


class PerformancePlot:
    """
    Plot expected performance metrics (Energy/Costs/Emissions) as 2 stacked bars
    (without invest vs with invest) and make it callable like TopologyPlot/ScenarioPlot:

        performance = PerformancePlot(h5_path=...)
        performance.plot_into(ax)

    Input modes:
      A) pass both files explicitly:
         PerformancePlot(h5_without_invest=..., h5_with_invest=...)

      B) pass one file; we will attempt to derive the partner file by swapping
         'with_invest' <-> 'without_invest' in the filename:
         PerformancePlot(h5_path=...)

    HDF5 expectation (same as your current implementation):
        /__expected__/energy/<trader>_mwh
        /__expected__/costs/<trader>_keur
        /__expected__/emissions/<trader>_t
    """

    TRADER_NAMES_FULL = ("gas_supplier", "electricity_supplier", "electricity_feed_in")

    TRADER_NAME_MAP: ClassVar[dict[str, str]] = {
        "gas_supplier": "gas purchase",
        "electricity_supplier": "electricity purchase",
        "electricity_feed_in": "electricity feed-in",
    }

    TRADER_NAME_COLOR: ClassVar[dict[str, str]] = {
        "gas_supplier": "dimgrey",
        "electricity_supplier": "lightgrey",
        "electricity_feed_in": "black",
    }

    METRIC_PATHS: ClassVar[dict[str, dict[str, str]]] = {
        "energy": {"suffix": "_mwh", "h5_group": "energy", "ylabel": "energy \nMWh"},
        "costs": {"suffix": "_keur", "h5_group": "costs", "ylabel": "costs \nkEUR"},
        "emissions": {"suffix": "_t", "h5_group": "emissions", "ylabel": "emissions \nt"},
    }

    def __init__(
        self,
        *,
        h5_path: str | Path | None = None,
        h5_without_invest: str | Path | None = None,
        h5_with_invest: str | Path | None = None,
        trader_names: tuple[str, ...] | None = None,
    ) -> None:
        # Keep the public interface consistent with other Plot classes:
        # - primary initializer is h5_path
        # - but we still allow explicit pair
        if h5_without_invest is None and h5_with_invest is None:
            if h5_path is None:
                raise ValueError("Provide either h5_path=... or both h5_without_invest=... and h5_with_invest=...")
            self.h5_without_invest, self.h5_with_invest = self._resolve_pair_from_single(Path(h5_path))
        else:
            if h5_without_invest is None or h5_with_invest is None:
                raise ValueError("If you pass one of h5_without_invest/h5_with_invest you must pass both.")
            self.h5_without_invest = Path(h5_without_invest)
            self.h5_with_invest = Path(h5_with_invest)

        self.trader_names = trader_names or self.TRADER_NAMES_FULL
        self.trader_map = self.TRADER_NAME_MAP
        self.trader_color = self.TRADER_NAME_COLOR

    @staticmethod
    def _resolve_pair_from_single(h5_path: Path) -> tuple[Path, Path]:
        """
        Derive (without, with) paths from a single file path by swapping tokens.

        Examples:
          stochastic_expected_with_invest_opex.h5
            -> stochastic_expected_without_invest_opex.h5

          stochastic_expected_without_invest_opex.h5
            -> stochastic_expected_with_invest_opex.h5
        """
        name = h5_path.name
        if "with_invest" in name:
            without = h5_path.with_name(name.replace("with_invest", "without_invest"))
            return without, h5_path
        if "without_invest" in name:
            with_ = h5_path.with_name(name.replace("without_invest", "with_invest"))
            return h5_path, with_

        # Fallback: assume given file is "with invest" and try a common neighbor name.
        # (This is deliberately conservative: it will error later if not found.)
        without = h5_path.with_name(name.replace(".h5", "_without_invest.h5"))
        return without, h5_path

    @staticmethod
    def _read_scalar_dataset(h5: h5py.File, path: str, default: float = 0.0) -> float:
        if path not in h5:
            return default
        val = h5[path][()]
        try:
            return float(val)
        except Exception:
            return default

    def _collect_expected_values(self, h5_path: Path) -> dict[str, dict[str, float]]:
        if not h5_path.exists():
            raise FileNotFoundError(f"HDF5 file not found: {h5_path}")

        out: dict[str, dict[str, float]] = {k: {} for k in self.METRIC_PATHS}

        with h5py.File(h5_path, "r") as f:
            base = "__expected__"
            if base not in f:
                raise KeyError(
                    f"Group '/{base}' not found in {h5_path}. "
                    "Expected metrics must be stored under '/__expected__/...'."
                )

            for quantity_name, meta in self.METRIC_PATHS.items():
                grp = meta["h5_group"]
                suffix = meta["suffix"]
                for trader in self.trader_names:
                    ds_path = f"{base}/{grp}/{trader}{suffix}"
                    out[quantity_name][trader] = self._read_scalar_dataset(f, ds_path, default=0.0)

        return out

    @staticmethod
    def _format_total(v: float) -> str:
        av = abs(v)
        if av >= 1:
            return f"{v:.2f}"
        if av >= 0.1:
            return f"{v:.3f}"
        return f"{v:.4f}"

    @staticmethod
    def _grouped_stacked_two_bars_per_metric(
        ax: plt.Axes,
        *,
        metric_order: list[str],
        metric_meta: dict[str, dict[str, str]],
        trader_names: tuple[str, ...],
        expected_without: dict[str, dict[str, float]],
        expected_with: dict[str, dict[str, float]],
        trader_label: dict[str, str],
        trader_color: dict[str, str],
    ) -> None:
        n_metrics = len(metric_order)

        # group geometry
        group_gap = 1.2  # space between metric groups
        intra_gap = 0.5  # gap between without/with inside group
        bar_width = 0.85

        x_without = np.arange(n_metrics) * (2 + group_gap)
        x_with = x_without + (1 + intra_gap)
        x_all = np.concatenate([x_without, x_with])

        # stacking accumulators per bar
        prev_pos = np.zeros_like(x_all, dtype=float)
        prev_neg = np.zeros_like(x_all, dtype=float)

        # values per trader across all bars
        def vals_for_trader(trader: str) -> np.ndarray:
            vals = []
            for m in metric_order:
                vals.append(float(expected_without[m].get(trader, 0.0)))
            for m in metric_order:
                vals.append(float(expected_with[m].get(trader, 0.0)))
            return np.array(vals, dtype=float)

        # plot stacked bars (across all metrics + both cases)
        for trader in trader_names:
            vals = vals_for_trader(trader)
            bottom = np.where(vals < 0, prev_neg, prev_pos)

            ax.bar(
                x_all,
                vals,
                width=bar_width,
                bottom=bottom,
                color=trader_color.get(trader, "grey"),
                edgecolor="black",
                linewidth=0.6,
                label=trader_label.get(trader, trader),
            )

            prev_pos = np.where(vals >= 0, prev_pos + vals, prev_pos)
            prev_neg = np.where(vals < 0, prev_neg + vals, prev_neg)

        totals = prev_pos + prev_neg

        # total labels
        for x, y in zip(x_all, totals, strict=True):
            off = 0.03 * (abs(y) + 1e-9)
            txt = ax.text(
                x,
                y + (off if y >= 0 else -off),
                PerformancePlot._format_total(y),
                ha="center",
                va="bottom" if y >= 0 else "top",
                fontsize=10,
                fontweight="bold",
            )
            txt.set_path_effects([pe.withStroke(linewidth=3, foreground="white")])

        # x ticks for each bar
        tick_pos = x_all
        tick_lbl = (["wo"] * n_metrics) + (["wi"] * n_metrics)
        ax.set_xticks(tick_pos, tick_lbl)

        # group labels centered under each pair
        centers = (x_without + x_with) / 2
        for c, m in zip(centers, metric_order, strict=True):
            ylab = metric_meta[m]["ylabel"]  # e.g. "energy \nMWh"
            ax.text(
                c,
                -0.03,
                ylab,
                ha="center",
                va="top",
                transform=ax.get_xaxis_transform(),
                fontsize=12,
                clip_on=False,  # prevents cutting off the 2nd line
            )

        # separator lines between groups
        for i in range(n_metrics - 1):
            sep_x = (x_with[i] + x_without[i + 1]) / 2
            ax.axvline(sep_x, color="black", linewidth=0.6, alpha=0.25)

        ax.grid(axis="y", alpha=0.35)
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", labelsize=9, pad=1)

    def plot_into(
        self,
        ax: matplotlib.axes.Axes,
        *,
        title: str | None = None,
        legend: bool = True,
        legend_ncol: int = 3,
    ) -> list[matplotlib.axes.Axes]:
        """
        Container-axis style like ScenarioPlot:
        - clear the container axis
        - create ONE inset axis for the performance bars
        - put legend above that inset axis (same code as ScenarioPlot)
        Returns a list with the created inset axis.
        """
        expected_without = self._collect_expected_values(self.h5_without_invest)
        expected_with = self._collect_expected_values(self.h5_with_invest)

        # Clear "container" axis; we will place inset axes inside it.
        ax.cla()
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

        if title:
            ax.set_title(title)

        # One inset axis filling (most of) the container
        # Leave a bit of top room for the legend above the inset axis
        iax = inset_axes(
            ax,
            width="100%",
            height="100%",
            bbox_to_anchor=(0.0, 0.0, 1.0, 1.0),
            bbox_transform=ax.transAxes,
            loc="lower left",
            borderpad=0.0,
        )

        iax.set_facecolor("white")

        metric_order = list(self.METRIC_PATHS.keys())

        # draw the grouped bars into the inset axis
        self._grouped_stacked_two_bars_per_metric(
            iax,
            metric_order=metric_order,
            metric_meta=self.METRIC_PATHS,
            trader_names=self.trader_names,
            expected_without=expected_without,
            expected_with=expected_with,
            trader_label=self.trader_map,
            trader_color=self.trader_color,
        )

        # ---- ScenarioPlot-style legend: above the inset axis ----
        if legend:
            handles, labels = iax.get_legend_handles_labels()

            leg = iax.legend(
                handles,
                labels,
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
            # prevent clipping / layout fights when legend is outside axes
            leg.set_in_layout(False)

        return [iax]

    def generate_plots(self, plot_path: str | Path, figure_name: str = "performance_expected") -> Path:
        """
        Standalone export (kept for convenience).
        """
        plot_path = Path(plot_path)
        plot_path.mkdir(parents=True, exist_ok=True)

        # Create a container axis and let plot_into subdivide it.
        fig = plt.figure(figsize=(15, 5), constrained_layout=True)
        ax = fig.add_subplot(1, 1, 1)
        self.plot_into(ax, legend=True)

        out = plot_path / f"{figure_name}.pdf"
        fig.savefig(out, format="pdf", bbox_inches="tight")
        plt.close(fig)

        logger.info("Saved performance plot to %s", out)
        return out
