from __future__ import annotations

import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass
class TypicalSeriesPlotter:
    """
    Plotter for "typical period" time series stored in an HDF5.

    Assumptions about each stored series:
      - Either has a MultiIndex (period, step), or columns ['period','step'] that can be set as such.
      - Remaining columns are the variables to plot.

    Features:
      - Plot weights
      - Plot typical periods for one key (subplots by period)
      - Plot multiple keys (blocks of subplots, one block per key)
      - Plot multiple parameters within the SAME period-subplots (overlay per period)
      - Optional weighted-mean (per key/column)
      - Step plotting (no interpolation between values)
      - Optional normalization (None / "zscore" / "minmax") for overlays
    """

    h5_path: Path
    weights_path: Path

    def __post_init__(self) -> None:
        self.h5_path = Path(self.h5_path)
        self.weights_path = Path(self.weights_path)

        if not self.h5_path.exists():
            raise FileNotFoundError(self.h5_path)
        if not self.weights_path.exists():
            raise FileNotFoundError(self.weights_path)

        self.weights: dict[int, float] = self._load_weights(self.weights_path)
        self.keys: list[str] = self._list_hdf_keys()

    # ------------------------- IO / validation -------------------------

    @staticmethod
    def _load_weights(path: Path) -> dict[int, float]:
        raw = json.loads(path.read_text(encoding="utf-8"))
        weights = {int(k): float(v) for k, v in raw.items()}
        s = float(sum(weights.values()))
        if abs(s - 1.0) > 1e-6:
            raise ValueError(f"weights must sum to 1.0, got {s}")
        return weights

    def _list_hdf_keys(self) -> list[str]:
        # IMPORTANT: open & close immediately to avoid PyTables double-open issues
        with pd.HDFStore(self.h5_path, mode="r") as store:
            keys = [k.lstrip("/") for k in store]
        return sorted(keys)

    def list_series(self) -> list[str]:
        return list(self.keys)

    def read_series(self, key: str) -> pd.DataFrame:
        if key not in self.keys:
            raise KeyError(f"{key!r} not found. Available: {self.list_series()}")

        with pd.HDFStore(self.h5_path, mode="r") as store:
            series_frame = store.get(key)

        # normalize to MultiIndex(period, step)
        if isinstance(series_frame.index, pd.MultiIndex) and series_frame.index.nlevels == 2:
            series_frame.index = series_frame.index.set_names(["period", "step"])
            return series_frame.sort_index()

        if "period" in series_frame.columns and "step" in series_frame.columns:
            return series_frame.set_index(["period", "step"]).sort_index()

        raise ValueError(f"{key!r} must have MultiIndex (period, step) or columns ['period','step'].")

    @staticmethod
    def _resolve_column(df_typical: pd.DataFrame, *, key: str, column: str | None) -> str:
        if column is None:
            if df_typical.shape[1] != 1:
                raise ValueError(f"{key!r} has multiple columns {list(df_typical.columns)}. Pass column=...")
            return str(df_typical.columns[0])
        if column not in df_typical.columns:
            raise KeyError(f"column {column!r} not in {list(df_typical.columns)} for key {key!r}")
        return column

    @staticmethod
    def _as_period_list(df_typical: pd.DataFrame, periods: Iterable[int] | None) -> list[int]:
        if periods is None:
            return sorted(df_typical.index.get_level_values("period").unique().astype(int).tolist())
        return [int(p) for p in periods]

    # ------------------------- math helpers -------------------------

    def weighted_mean_profile(self, df_one_col: pd.DataFrame) -> pd.Series:
        """
        Weighted mean profile across typical periods:
           out[step] = sum_p w[p] * x[p, step]
        """
        if df_one_col.shape[1] != 1:
            raise ValueError("weighted_mean_profile expects exactly one column")

        col = str(df_one_col.columns[0])
        periods = sorted(df_one_col.index.get_level_values("period").unique().astype(int).tolist())
        steps = sorted(df_one_col.index.get_level_values("step").unique().tolist())

        out = pd.Series(index=steps, dtype=float)
        out[:] = 0.0

        for p in periods:
            w = self.weights.get(int(p))
            if w is None:
                raise KeyError(f"Missing weight for period {p}")
            prof = df_one_col.xs(p, level="period")[col].reindex(steps)
            out += w * prof

        out.name = f"{col}_weighted_mean"
        out.index.name = "step"
        return out

    @staticmethod
    def _normalize_array(y: np.ndarray, mode: str | None) -> np.ndarray:
        """
        mode:
          - None: no normalization
          - "zscore": (y - mean) / std
          - "minmax": (y - min) / (max - min)
        """
        if mode is None:
            return y
        if mode == "zscore":
            mu = float(np.mean(y))
            sigma = float(np.std(y))
            return (y - mu) / (sigma if sigma > 0 else 1.0)
        if mode == "minmax":
            ymin = float(np.min(y))
            ymax = float(np.max(y))
            denom = (ymax - ymin) if ymax > ymin else 1.0
            return (y - ymin) / denom
        raise ValueError("normalize must be None, 'zscore', or 'minmax'.")

    # ------------------------- plotting helpers -------------------------

    @staticmethod
    def _should_add_legend(*, legend_mode: str, i: int) -> bool:
        if legend_mode == "none":
            return False
        return legend_mode == "each" or (legend_mode == "first" and i == 0)

    @staticmethod
    def _disable_unused_axes(axes: np.ndarray, *, used: int, nrows: int, ncols: int) -> None:
        for j in range(used, nrows * ncols):
            r, c = divmod(j, ncols)
            axes[r][c].axis("off")

    @staticmethod
    def _set_shared_axis_labels(axes: np.ndarray, *, nrows: int, ncols: int, ylabel: str) -> None:
        for r in range(nrows):
            axes[r][0].set_ylabel(ylabel)
        for c in range(ncols):
            axes[-1][c].set_xlabel("step")

    # ------------------------- public plotting API -------------------------

    def plot_weights(self, *, title: str = "Typical period weights") -> plt.Figure:
        periods = sorted(self.weights.keys())
        vals = [self.weights[p] for p in periods]

        fig, ax = plt.subplots()
        ax.bar([str(p) for p in periods], vals)
        ax.set_xlabel("Typical period")
        ax.set_ylabel("Weight (fraction of year)")
        ax.set_title(title)
        ax.grid(True, axis="y", alpha=0.3)
        fig.tight_layout()
        return fig

    def plot_typical_periods(
        self,
        key: str,
        *,
        column: str | None = None,
        periods: Iterable[int] | None = None,
        show_weighted_mean: bool = False,
        ncols: int = 3,
        title: str | None = None,
        legend_mode: str = "first",  # "first" | "each" | "none"
        where: str = "post",  # step style: "pre" | "post" | "mid"
        sharey: bool = True,
    ) -> plt.Figure:
        """
        One key/column: subplots by period. Uses step plot (no interpolation).
        """
        df_typical = self.read_series(key)
        col = self._resolve_column(df_typical, key=key, column=column)
        period_list = self._as_period_list(df_typical, periods)

        n = len(period_list)
        ncols = max(1, int(ncols))
        nrows = (n + ncols - 1) // ncols

        fig, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            sharex=True,
            sharey=sharey,
            squeeze=False,
        )

        wm = self.weighted_mean_profile(df_typical[[col]]) if show_weighted_mean else None
        plot_mean = wm is not None

        for i, p in enumerate(period_list):
            r, c = divmod(i, ncols)
            ax = axes[r][c]

            prof = df_typical.xs(int(p), level="period")[col]

            ax.step(
                prof.index,
                prof.to_numpy(),
                where=where,
                linewidth=1.2,
                label=f"period {p} (w={self.weights.get(int(p), float('nan')):.3f})",
            )

            if plot_mean:
                ax.step(
                    wm.index,
                    wm.to_numpy(),
                    where=where,
                    linestyle="--",
                    linewidth=1.4,
                    label="weighted mean",
                )

            ax.set_title(f"Period {p}")
            ax.grid(True, alpha=0.3)

            if self._should_add_legend(legend_mode=legend_mode, i=i):
                ax.legend(fontsize=8)

        self._disable_unused_axes(axes, used=n, nrows=nrows, ncols=ncols)
        self._set_shared_axis_labels(axes, nrows=nrows, ncols=ncols, ylabel=str(col))

        fig.suptitle(title or f"{key} — typical periods")
        fig.tight_layout()
        return fig

    def plot_periods_with_multiple_parameters(
        self,
        specs: Sequence[dict],
        *,
        periods: Iterable[int] | None = None,
        ncols: int = 3,
        title: str | None = None,
        legend_mode: str = "first",
        normalize: str | None = None,  # None | "zscore" | "minmax"
        show_weighted_mean: bool = False,  # usually False for overlays
        where: str = "post",
    ) -> plt.Figure:
        """
        One FIGURE with subplots by period.
        Inside each period subplot, overlay MULTIPLE parameters (keys/columns).

        specs items:
          {"key": "...", "column": "...", "label": "..."}  (label optional)

        normalize:
          - None: raw units (only sensible if units comparable)
          - "zscore" or "minmax": normalize within each period and series, so shapes compare.
        """
        # Load all series and compute common periods (so overlays align)
        series_data: list[tuple[str, str, str, pd.DataFrame]] = []  # (key, col, label, df_onecol)
        common_periods: set[int] | None = None

        for s in specs:
            key = s["key"]
            df_typical = self.read_series(key)
            col = self._resolve_column(df_typical, key=key, column=s.get("column"))
            label = s.get("label", f"{key}:{col}")

            pset = set(df_typical.index.get_level_values("period").unique().astype(int).tolist())
            common_periods = pset if common_periods is None else (common_periods & pset)

            series_data.append((key, col, label, df_typical[[col]]))

        if common_periods is None or len(common_periods) == 0:
            raise ValueError("No common periods found across the provided specs.")

        period_list = sorted(common_periods) if periods is None else [int(p) for p in periods]

        n = len(period_list)
        ncols = max(1, int(ncols))
        nrows = (n + ncols - 1) // ncols

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, squeeze=False)

        # Optional: weighted mean per series (same curve in every subplot)
        weighted_means: dict[str, pd.Series] = {}
        if show_weighted_mean:
            for _key, _col, label, df1 in series_data:
                weighted_means[label] = self.weighted_mean_profile(df1)

        for i, p in enumerate(period_list):
            r, c = divmod(i, ncols)
            ax = axes[r][c]

            for _key, col, label, df1 in series_data:
                prof = df1.xs(int(p), level="period")[col]
                y = prof.to_numpy(dtype=float)
                y = self._normalize_array(y, normalize)

                ax.step(
                    prof.index,
                    y,
                    where=where,
                    linewidth=1.2,
                    label=label,
                )

                if show_weighted_mean:
                    wm = weighted_means[label]
                    ax.step(
                        wm.index,
                        self._normalize_array(wm.to_numpy(dtype=float), normalize),
                        where=where,
                        linestyle="--",
                        linewidth=1.2,
                        label=f"{label} (weighted mean)",
                    )

            ax.set_title(f"Period {p} (w={self.weights.get(int(p), float('nan')):.3f})")
            ax.grid(True, alpha=0.3)

            if self._should_add_legend(legend_mode=legend_mode, i=i):
                ax.legend(fontsize=8, ncol=2)

        self._disable_unused_axes(axes, used=n, nrows=nrows, ncols=ncols)

        ylabel = "value" if normalize is None else f"value ({normalize})"
        self._set_shared_axis_labels(axes, nrows=nrows, ncols=ncols, ylabel=ylabel)

        fig.suptitle(title or "Typical periods — multiple parameters per subplot")
        fig.tight_layout()
        return fig

    # ------------------------- saving -------------------------

    @staticmethod
    def save_fig(fig: plt.Figure, path: Path, *, dpi: int = 200) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=dpi, bbox_inches="tight")


if __name__ == "__main__":
    h5_path = r"C:\Git\eta-incerto\examples\deterministic\series\eta\typical_series.h5"
    weights_path = r"C:\Git\eta-incerto\examples\deterministic\series\eta\weights.json"

    plotter = TypicalSeriesPlotter(h5_path=h5_path, weights_path=weights_path)

    fig_w = plotter.plot_weights()
    plotter.save_fig(fig_w, Path("plots/weights.png"))

    # 1) Single key -> typical periods (subplots by period)
    fig = plotter.plot_typical_periods(
        "ambient_temperature",
        column="T_db",
        show_weighted_mean=False,
        legend_mode="first",
        where="post",
    )
    plotter.save_fig(fig, Path("plots/ambient_temperature_typicals.png"))

    # 3) Period subplots, overlay multiple parameters inside each period
    #    a) raw units (only if comparable)
    fig = plotter.plot_periods_with_multiple_parameters(
        specs=[
            {"key": "cn_consumer", "column": "P_in", "label": "CN load"},
            {"key": "hnht_consumer", "column": "P_in", "label": "HNHT load"},
            {"key": "hnlt_consumer", "column": "P_in", "label": "HNLT load"},
            {"key": "ambient_temperature", "column": "T_db", "label": "T_amb"},
            {"key": "hnlt_producer", "column": "P_in", "label": "Producer"},
        ],
        ncols=3,
        normalize=None,
        legend_mode="first",
        title="Loads per typical period (raw units)",
        where="post",
    )
    plotter.save_fig(fig, Path("plots/periods_overlay_loads_raw.png"))

    #    b) normalized (best for mixed units like temperature + power)
    fig = plotter.plot_periods_with_multiple_parameters(
        specs=[
            {"key": "ambient_temperature", "column": "T_db", "label": "T_amb"},
            {"key": "cn_consumer", "column": "P_in", "label": "CN load"},
            {"key": "hnlt_producer", "column": "P_in", "label": "Producer"},
            {"key": "hnht_consumer", "column": "P_in", "label": "HNHT load"},
            {"key": "hnlt_consumer", "column": "P_in", "label": "HNLT load"},
        ],
        ncols=3,
        normalize="zscore",  # or "minmax"
        legend_mode="first",
        title="Multiple parameters per typical period (normalized)",
        where="post",
    )
    plotter.save_fig(fig, Path("plots/periods_overlay_mixed_normalized.png"))
