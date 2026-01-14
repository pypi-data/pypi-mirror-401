from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np
from pydantic import BaseModel, Field


class TablePlot(BaseModel):
    """
    Load KPIs from an HDF5 file and plot them as an A4-ready matplotlib table.

    Scenario groups are discovered automatically (no hard-coded scenario names).
    By default, we assume scenarios are top-level H5 groups.
    """

    h5_path: Path = Field(..., description="Path to the HDF5 results file.")
    title: str = "KPI Table"
    fontsize: int = 10
    header_fontsize: int = 14
    table_bbox: tuple[float, float, float, float] = (0.02, 0.05, 0.96, 0.88)
    section_facecolor: tuple[float, float, float] = (0.95, 0.95, 0.95)

    # If you want custom scenario labels (e.g. ["Base", "HP", "HP+..."]), provide these.
    # If empty, labels are auto-generated: S1..Sn
    scenario_labels: Sequence[str] = ()

    # Limit number of scenarios shown (useful if the file contains many groups)
    max_scenarios: int = 3

    # ---- H5 discovery ----
    def _discover_scenarios(self, f: h5py.File) -> list[str]:
        """
        Discover scenario group keys.

        Default heuristic: top-level groups that look like scenario containers.
        If your H5 has a different structure, adapt this function.
        """
        keys: list[str] = []
        for k, obj in f.items():
            if isinstance(obj, h5py.Group):
                keys.append(k)

        # Stable order: alphabetical (keeps it reproducible)
        keys = sorted(keys)

        # Clip to max_scenarios
        if self.max_scenarios and len(keys) > self.max_scenarios:
            keys = keys[: self.max_scenarios]

        return keys

    # ---- Reading & formatting ----
    def _read_scalar(self, f: h5py.File, dataset_path: str, default: float = np.nan) -> float:
        try:
            if dataset_path in f:
                return float(f[dataset_path][()])
        except Exception:
            pass
        return default

    @staticmethod
    def _fmt_de(x: float, nd: int = 1, scale: float = 1.0) -> str:
        try:
            if x is None or np.isnan(x) or np.isinf(x):
                return "—"
        except Exception:
            return "—"
        v = float(x) * scale
        return f"{v:.{nd}f}".replace(".", ",")

    # ---- KPI row construction ----
    def _build_rows(self, f: h5py.File, scen_keys: Sequence[str]) -> list[list[str]]:
        rows: list[list[str]] = []

        def vals(ds_suffix: str, nd: int = 1, scale: float = 1.0) -> list[str]:
            return [self._fmt_de(self._read_scalar(f, f"{sk}/{ds_suffix}"), nd=nd, scale=scale) for sk in scen_keys]

        # Helper for section header rows: put blanks in scenario columns
        def section(name: str) -> None:
            rows.append([name, *([""] * len(scen_keys))])

        # --- Technical ---
        section("technical")
        rows.append(["Thermal output power HP in kW", *vals("investment/hp_hnlt_outside_p_out_nom", nd=1)])

        # Storage volume: keep as placeholder unless you know the dataset path.
        rows.append(["Volume thermal storage [m³]", *(["0,0"] * len(scen_keys))])

        rows.append(
            [
                "Heating energy consumed (electricity supplier) [MWh]",
                *vals("energy/electricity_supplier_mwh", nd=2),
            ]
        )

        # --- Economical ---
        section("economic")
        # capex
        rows.append(["CAPEX", *vals("objective/capex", nd=1)])
        rows.append(["optimal NPV in kEUR", *vals("objective/npv", nd=1)])
        rows.append(["investment costs in kEUR", *vals("investment/hp_hnlt_outside_investment_cost", nd=1)])
        # opex
        rows.append(["electricity costs in kEUR", *vals("costs/electricity_supplier_keur", nd=1)])
        rows.append(["electricity feed-in in kEUR", *vals("costs/electricity_feed_in_keur", nd=1)])
        rows.append(["gas costs in kEUR", *vals("costs/gas_supplier_keur", nd=1)])

        # --- Ecological ---
        section("ecological")
        rows.append(["emissions in t CO_2", *vals("emissions/total_t", nd=1)])

        return rows

    # ---- Plotting ----
    def plot_into(self, ax: plt.Axes) -> None:
        ax.axis("off")

        with h5py.File(self.h5_path, "r") as f:
            scen_keys = self._discover_scenarios(f)

            if len(scen_keys) == 0:
                ax.text(0.5, 0.5, "No scenario groups found in H5.", ha="center", va="center")
                return

            # Labels
            if self.scenario_labels and len(self.scenario_labels) == len(scen_keys):
                labels = list(self.scenario_labels)
            else:
                labels = [f"S{i + 1}" for i in range(len(scen_keys))]

            # Title
            ax.text(
                0.5,
                0.97,
                self.title,
                ha="center",
                va="top",
                fontsize=self.header_fontsize,
                fontweight="bold",
                transform=ax.transAxes,
            )

            # Rows + table
            rows = self._build_rows(f, scen_keys)
            col_labels = ["", *labels]

            tbl = ax.table(
                cellText=rows,
                colLabels=col_labels,
                cellLoc="left",
                colLoc="center",
                loc="upper center",
                bbox=list(self.table_bbox),
            )

        tbl.auto_set_font_size(False)
        tbl.set_fontsize(self.fontsize)

        # Header styling
        for c in range(len(col_labels)):
            cell = tbl[0, c]
            cell.set_text_props(fontweight="bold")
            cell.set_linewidth(1.0)

        # Section rows styling: blanks in all scenario columns
        for r in range(1, len(rows) + 1):  # header is row 0
            is_section = all(rows[r - 1][c] == "" for c in range(1, len(col_labels)))
            if is_section:
                for c in range(len(col_labels)):
                    cell = tbl[r, c]
                    cell.set_text_props(fontweight="bold")
                    cell.set_facecolor(self.section_facecolor)
                    cell.set_linewidth(1.0)
                    if c > 0:
                        cell.get_text().set_text("")

        # Column widths (first col wider; remaining cols share)
        ncols = len(col_labels)
        first_w = 0.60
        other_w = (1.0 - first_w) / max(1, (ncols - 1))

        for (_r, c), cell in tbl.get_celld().items():
            if c == 0:
                cell.set_width(first_w)
            else:
                cell.set_width(other_w)

    def plot(self, *, figsize: tuple[float, float] = (8.27, 11.69)) -> plt.Figure:
        fig = plt.figure(figsize=figsize, constrained_layout=True)
        ax = fig.add_subplot(111)
        self.plot_into(ax)
        return fig
