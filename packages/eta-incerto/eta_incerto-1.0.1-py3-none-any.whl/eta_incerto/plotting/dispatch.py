from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass(frozen=True, slots=True)
class HeatmapStyle:
    cmap: str = "bwr"
    vmin: float | None = None
    vmax: float | None = None
    interpolation: str = "none"
    aspect: str = "auto"
    cbar_label: str = "kW"
    figsize: tuple[float, float] = (14, 6)
    show_xticks: bool = False
    xtick_count: int = 12


@dataclass(slots=True)
class DispatchPlotter:
    """
    HDF5 layout (as in baseline_opex.h5):

        /config
        /<scenario_name>/unit_dispatch/units/<unit>/<component>/{keys,values}

    Example:
        gas_eta_S1/unit_dispatch/units/chp1/p_heat_out/values   (T,)
        gas_eta_S1/unit_dispatch/units/chp1/p_heat_out/keys     (T,) bytes like b"(1, 1, 1)"
    """

    h5_path: str | Path
    unit_dispatch_group: str = "unit_dispatch/units"

    def __post_init__(self) -> None:
        self.h5_path = Path(self.h5_path)
        if not self.h5_path.exists():
            raise FileNotFoundError(f"H5 file not found: {self.h5_path}")

    # -------------------------
    # Discovery helpers
    # -------------------------
    def list_scenarios(self) -> list[str]:
        """Scenarios are top-level groups except 'config'."""
        with h5py.File(self.h5_path, "r") as h5f:
            top_level = [name for name in h5f if isinstance(h5f[name], h5py.Group)]
        return sorted(name for name in top_level if name != "config")

    def list_units(self, scenario: str) -> list[str]:
        base = f"{scenario}/{self.unit_dispatch_group}"
        with h5py.File(self.h5_path, "r") as h5f:
            if base not in h5f:
                raise KeyError(f"'{base}' not found in file.")
            return sorted(h5f[base])

    def list_components(self, scenario: str, *, only_power: bool = False) -> list[str]:
        """Union of component names across all units in a scenario."""
        base = f"{scenario}/{self.unit_dispatch_group}"
        comps: set[str] = set()

        with h5py.File(self.h5_path, "r") as h5f:
            if base not in h5f:
                raise KeyError(f"'{base}' not found in file.")

            units_group = h5f[base]
            for unit in units_group:
                unit_group = units_group[unit]
                for comp in unit_group:
                    comp_name = str(comp)
                    if only_power and not comp_name.startswith("p_"):
                        continue
                    comps.add(comp_name)

        return sorted(comps)

    # -------------------------
    # Loading helpers
    # -------------------------
    @staticmethod
    def _decode_bytes_array(arr: np.ndarray) -> list[str]:
        if arr.dtype.kind not in {"S", "O"}:
            return [str(x) for x in arr.tolist()]

        decoded: list[str] = []
        for item in arr:
            if isinstance(item, (bytes, np.bytes_)):
                decoded.append(item.decode("utf-8", errors="replace"))
            else:
                decoded.append(str(item))
        return decoded

    def load_component_frame(
        self,
        scenario: str,
        component: str,
        *,
        fill_missing: float = np.nan,
    ) -> pd.DataFrame:
        """
        Build a (n_steps x n_units) DataFrame for one component across all units.

        Units lacking the component are NaN (masked in plot).
        Index is taken from '<unit>/<component>/keys' if present.
        """
        units = self.list_units(scenario)
        base = f"{scenario}/{self.unit_dispatch_group}"

        series_by_unit: dict[str, np.ndarray] = {}
        index_keys: list[str] | None = None

        with h5py.File(self.h5_path, "r") as h5f:
            for unit in units:
                comp_path = f"{base}/{unit}/{component}"
                if comp_path not in h5f:
                    continue

                comp_group = h5f[comp_path]
                if "values" not in comp_group:
                    continue

                values = np.asarray(comp_group["values"], dtype=float).reshape(-1)

                if index_keys is None and "keys" in comp_group:
                    keys_arr = np.asarray(comp_group["keys"])
                    index_keys = self._decode_bytes_array(keys_arr)

                series_by_unit[unit] = values

        if not series_by_unit:
            raise KeyError(
                f"No data found for component='{component}' in scenario='{scenario}'. "
                f"Try list_components(scenario, only_power=True)."
            )

        n_steps = max(len(v) for v in series_by_unit.values())
        if index_keys is None or len(index_keys) != n_steps:
            index_keys = [str(i) for i in range(n_steps)]

        dispatch_frame = pd.DataFrame(index=index_keys, columns=units, dtype=float)
        dispatch_frame.loc[:, :] = fill_missing

        for unit, values in series_by_unit.items():
            padded = (
                np.pad(values, (0, n_steps - len(values)), constant_values=np.nan)
                if len(values) < n_steps
                else values[:n_steps]
            )
            dispatch_frame[unit] = padded

        return dispatch_frame

    # -------------------------
    # Plotting
    # -------------------------

    @staticmethod
    def add_year_separators_and_labels(
        ax: plt.Axes,
        *,
        n_years: int,
        n_periods: int,
        n_time_steps: int,
        show_day_grid: bool = True,
        day_grid_alpha: float = 0.18,
        year_line_width: float = 1.6,
        year_line_alpha: float = 0.7,
    ) -> None:
        """
        Adds:
          - thick vertical lines at year boundaries
          - major x ticks labeled Y1..Yn at year centers
          - optional thin day grid lines (each period)
        Assumes x-axis is 0..(total_steps-1) with each column = one time step.
        """
        steps_per_year = n_periods * n_time_steps
        total_steps = n_years * steps_per_year

        # ----- Year boundary lines -----
        # Draw at boundaries between columns; using x = boundary - 0.5 aligns with imshow cells.
        for y in range(1, n_years):
            x = y * steps_per_year - 0.5
            ax.axvline(x, linewidth=year_line_width, alpha=year_line_alpha)

        # ----- Day (period) grid lines -----
        if show_day_grid:
            for x in range(n_time_steps, total_steps, n_time_steps):
                ax.axvline(x - 0.5, linewidth=0.6, alpha=day_grid_alpha)

        # ----- Representative labels (center of each year block) -----
        centers = np.array(
            [y * steps_per_year + (steps_per_year - 1) / 2 for y in range(n_years)],
            dtype=float,
        )
        ax.set_xticks(centers)
        ax.set_xticklabels([f"Y{y + 1}" for y in range(n_years)], fontsize=9)
        ax.set_xlabel("Representative week per year (Y1..Yn)")

    def plot_heatmap(
        self,
        scenario: str,
        component: str,
        *,
        style: HeatmapStyle | None = None,
        unit_order: Sequence[str] | None = None,
        title: str | None = None,
        save_path: str | Path | None = None,
        show: bool = True,
    ):
        style = style or HeatmapStyle()

        dispatch_frame = self.load_component_frame(scenario, component)

        if unit_order is not None:
            missing = [u for u in unit_order if u not in dispatch_frame.columns]
            if missing:
                raise ValueError(f"unit_order contains unknown units: {missing}")
            dispatch_frame = dispatch_frame.loc[:, list(unit_order)]

        # units as rows
        data = dispatch_frame.to_numpy(dtype=float).T  # (n_units, n_steps)
        masked = np.ma.masked_invalid(data)

        finite = np.isfinite(data)
        if not finite.any():
            raise ValueError("No finite values to plot.")

        vmin = style.vmin
        vmax = style.vmax
        if vmin is None or vmax is None:
            max_abs = float(np.nanmax(np.abs(data[finite])))
            max_abs = max(max_abs, 1e-9)
            vmin = -max_abs if vmin is None else vmin
            vmax = +max_abs if vmax is None else vmax

        fig, ax = plt.subplots(figsize=style.figsize)

        im = ax.imshow(
            masked,
            cmap=style.cmap,
            vmin=vmin,
            vmax=vmax,
            aspect=style.aspect,
            interpolation=style.interpolation,
        )
        im.cmap.set_bad(color="lightgray")

        ax.set_yticks(np.arange(dispatch_frame.shape[1]))
        ax.set_yticklabels(dispatch_frame.columns, fontsize=9)
        ax.set_xlabel("Time step")
        ax.set_ylabel("Unit")

        ax.set_title(title or f"{scenario} | {component}")

        if not style.show_xticks:
            ax.set_xticks([])
        else:
            n_steps = dispatch_frame.shape[0]
            tick_count = min(style.xtick_count, max(4, n_steps // 10))
            idx = np.linspace(0, n_steps - 1, tick_count, dtype=int)
            ax.set_xticks(idx)
            ax.set_xticklabels([dispatch_frame.index[i] for i in idx], fontsize=8)

        # Colorbar like your snippet (separate axes)
        ax_pos = ax.get_position().get_points().flatten()
        cax = fig.add_axes([0.93, ax_pos[1] + 0.05, 0.012, ax_pos[3] - ax_pos[1] - 0.1])
        fig.colorbar(im, ax=ax, cax=cax)

        text_x = cax.get_position().x0 + cax.get_position().width / 2
        text_y = cax.get_position().y1 + 0.01
        fig.text(text_x, text_y, style.cbar_label, ha="center", va="bottom", rotation=90)

        fig.tight_layout(rect=[0.0, 0.0, 0.92, 1.0])

        if save_path is not None:
            out = Path(save_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(out, dpi=200)

        if show:
            plt.show()

        return fig, ax

    def plot_components(
        self,
        scenario: str,
        components: Sequence[str],
        *,
        style: HeatmapStyle | None = None,
        show: bool = True,
    ):
        style = style or HeatmapStyle()
        figs = []
        for comp in components:
            figs.append(
                self.plot_heatmap(
                    scenario=scenario,
                    component=comp,
                    style=style,
                    show=show,
                )
            )
        return figs

    def load_components_matrix(
        self,
        scenario: str,
        components: Sequence[str],
        *,
        fill_missing: float = np.nan,
        row_order: Sequence[tuple[str, str]] | None = None,
    ) -> pd.DataFrame:
        """
        Build a single matrix with rows=(unit,component) and cols=time steps.
        """
        base = f"{scenario}/{self.unit_dispatch_group}"
        units = self.list_units(scenario)

        values_by_row: dict[tuple[str, str], np.ndarray] = {}
        index_keys: list[str] | None = None
        n_steps = 0

        with h5py.File(self.h5_path, "r") as h5f:
            for unit in units:
                unit_path = f"{base}/{unit}"
                if unit_path not in h5f:
                    continue

                unit_group = h5f[unit_path]
                for comp in components:
                    if comp not in unit_group:
                        continue

                    comp_group = unit_group[comp]
                    if "values" not in comp_group:
                        continue

                    vals = np.asarray(comp_group["values"], dtype=float).reshape(-1)

                    if index_keys is None and "keys" in comp_group:
                        keys_arr = np.asarray(comp_group["keys"])
                        index_keys = self._decode_bytes_array(keys_arr)

                    values_by_row[(unit, comp)] = vals
                    n_steps = max(n_steps, len(vals))

        if not values_by_row:
            raise KeyError(f"No data found for components={list(components)} in scenario='{scenario}'.")

        if index_keys is None or len(index_keys) != n_steps:
            index_keys = [str(i) for i in range(n_steps)]

        rows = list(row_order) if row_order is not None else sorted(values_by_row, key=lambda x: (x[0], x[1]))

        if row_order is not None:
            missing = [rc for rc in rows if rc not in values_by_row]
            if missing:
                raise ValueError(f"row_order contains unknown rows: {missing}")

        mat = np.full((len(rows), n_steps), fill_missing, dtype=float)

        for i, rc in enumerate(rows):
            v = values_by_row[rc]
            v = np.pad(v, (0, n_steps - len(v)), constant_values=np.nan) if len(v) < n_steps else v[:n_steps]
            mat[i, :] = v

        return pd.DataFrame(
            mat,
            index=pd.MultiIndex.from_tuples(rows, names=["unit", "component"]),
            columns=index_keys,
        )

    def plot_combined_heatmap(
        self,
        scenario: str,
        components: Sequence[str],
        *,
        style: HeatmapStyle | None = None,
        title: str | None = None,
        save_path: str | Path | None = None,
        show: bool = True,
        # optional: compress row labels
        show_component_prefix: bool = True,
    ):
        style = style or HeatmapStyle()

        combined = self.load_components_matrix(scenario, components)

        data = combined.to_numpy(dtype=float)
        masked = np.ma.masked_invalid(data)

        finite = np.isfinite(data)
        if not finite.any():
            raise ValueError("No finite values to plot.")

        vmin = style.vmin
        vmax = style.vmax
        if vmin is None or vmax is None:
            max_abs = float(np.nanmax(np.abs(data[finite])))
            max_abs = max(max_abs, 1e-9)
            vmin = -max_abs if vmin is None else vmin
            vmax = +max_abs if vmax is None else vmax

        fig, ax = plt.subplots(figsize=style.figsize)

        im = ax.imshow(
            masked,
            cmap=style.cmap,
            vmin=vmin,
            vmax=vmax,
            aspect=style.aspect,
            interpolation=style.interpolation,
        )

        # Turn off your default x tick logic
        ax.set_xticks([])  # optional; we'll override below anyway

        self.add_year_separators_and_labels(
            ax,
            n_years=10,
            n_periods=7,
            n_time_steps=24,
            show_day_grid=True,
        )
        im.cmap.set_bad(color="lightgray")

        # y labels
        idx = combined.index  # MultiIndex (unit, component)
        if show_component_prefix:
            ylabels = [f"{u} | {c}" for (u, c) in idx.to_list()]
        else:
            ylabels = [f"{u}-{c}" for (u, c) in idx.to_list()]

        ax.set_yticks(np.arange(len(ylabels)))
        ax.set_yticklabels(ylabels, fontsize=8)

        ax.set_xlabel("Time step")
        ax.set_ylabel("Unit | Component")
        ax.set_title(title or f"{scenario} | combined components")

        # x ticks (same idea as before)
        if not style.show_xticks:
            ax.set_xticks([])
        else:
            n_steps = combined.shape[1]
            tick_count = min(style.xtick_count, max(4, n_steps // 10))
            xt = np.linspace(0, n_steps - 1, tick_count, dtype=int)
            ax.set_xticks(xt)
            ax.set_xticklabels([combined.columns[i] for i in xt], fontsize=8)

        # colorbar axis (same style)
        ax_pos = ax.get_position().get_points().flatten()
        cax = fig.add_axes([0.93, ax_pos[1] + 0.05, 0.012, ax_pos[3] - ax_pos[1] - 0.1])
        fig.colorbar(im, ax=ax, cax=cax)

        text_x = cax.get_position().x0 + cax.get_position().width / 2
        text_y = cax.get_position().y1 + 0.01
        fig.text(text_x, text_y, style.cbar_label, ha="center", va="bottom", rotation=90)

        fig.tight_layout(rect=[0.0, 0.0, 0.92, 1.0])

        if save_path is not None:
            out = Path(save_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(out, dpi=200)

        if show:
            plt.show()

        return fig, ax, combined


if __name__ == "__main__":
    h5_path = "examples/deterministic/results/baseline_with_invest_opex.h5"
    plotter = DispatchPlotter(h5_path)

    # single component plots:
    scenario = plotter.list_scenarios()[0]
    components = plotter.list_components(scenario, only_power=True)

    style = HeatmapStyle(vmin=-30, vmax=30, show_xticks=False)
    plotter.plot_heatmap(scenario, component="p_heat_out", style=style)  # all heating converters; sthnht discharge
    plotter.plot_heatmap(scenario, component="p_el_out", style=style)  # chps
    plotter.plot_heatmap(scenario, component="p_cool_in", style=style)  # cooling consumers
    plotter.plot_heatmap(scenario, component="p_cool_out", style=style)  # cooling providers
    plotter.plot_heatmap(scenario, component="amount", style=style)  # electricity, gas suppliers

    # overall plots:
    scenario = plotter.list_scenarios()[0]

    comps = ["p_heat_out", "p_el_out", "p_cool_in", "p_cool_out", "amount"]

    style = HeatmapStyle(vmin=-30, vmax=30, show_xticks=False)

    fig, ax, combined = plotter.plot_combined_heatmap(
        scenario=scenario,
        components=comps,
        style=style,
        title="All components (10 years x representative week)",
        show=True,
    )

    plotter.add_year_separators_and_labels(
        ax,
        n_years=10,
        n_periods=7,
        n_time_steps=24,
        show_day_grid=True,
    )
    plt.show()

    plotter.plot_combined_heatmap(
        scenario=scenario,
        components=comps,
        style=style,
        title="All components (mixed units)",
    )
