"""
PDF reporting for std_target sensitivity analysis.

This module creates a multi-page PDF report from the SensitivityReport dict
returned by eta_incerto.analysis.sensitivity.

Plots are based on the original exploration notebook and are designed to be:
- robust (skip missing columns gracefully),
- readable (one page per plot group),
- PEP8-compliant.

No TSAM imports here.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


def _ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _get_table(report: dict[str, Any]) -> pd.DataFrame:
    table = report.get("table")
    if not isinstance(table, pd.DataFrame):
        raise TypeError("Report['table'] must be a pandas DataFrame.")
    return table


def _index_level_name(table: pd.DataFrame, preferred: Sequence[str]) -> str | None:
    if not isinstance(table.index, pd.MultiIndex):
        return None
    names = [n for n in table.index.names if n is not None]
    for p in preferred:
        if p in names:
            return p
    return names[0] if names else None


def _unique_varied_features(table: pd.DataFrame) -> list[str]:
    if isinstance(table.index, pd.MultiIndex):
        lvl = _index_level_name(table, preferred=("varied_feature", "feature"))
        if lvl is None:
            return []
        return list(pd.Index(table.index.get_level_values(lvl)).unique())

    if "varied_feature" in table.columns:
        return sorted(table["varied_feature"].unique().tolist())

    return []


def _extract_factor_sweep(table: pd.DataFrame, varied_feature: str) -> pd.DataFrame:
    """
    Return a DataFrame with a 'factor' column for one varied feature.
    Robust against 'factor' being both index level and existing column.
    """
    if isinstance(table.index, pd.MultiIndex):
        lvl = _index_level_name(table, preferred=("varied_feature", "feature"))
        if lvl is None:
            raise ValueError("Cannot determine varied-feature level in table index.")

        sub = table.xs(varied_feature, level=lvl, drop_level=False).copy()

        # We want factor as a COLUMN (not only an index level).
        # If factor is already a column, don't bring index levels as columns (avoid duplicates).
        sub = sub.reset_index(drop=True) if "factor" in sub.columns else sub.reset_index()

        # If factor exists as index level name but came out unnamed, try to recover it
        if "factor" not in sub.columns:
            for c in sub.columns:
                if str(c).startswith("level_") and c != "level_0" and pd.api.types.is_numeric_dtype(sub[c]):
                    sub = sub.rename(columns={c: "factor"})
                    break

        if "factor" not in sub.columns:
            raise ValueError("Could not extract 'factor' as a column from the sensitivity table.")

        # Ensure we still have varied_feature as a column for downstream plotting (if needed)
        if "varied_feature" not in sub.columns and lvl in sub.columns:
            sub = sub.rename(columns={lvl: "varied_feature"})

        return sub

    # fallback: filter by column
    return table[table["varied_feature"] == varied_feature].copy()


def _plot_fir(pdf: PdfPages, fir: dict[str, float]) -> None:
    if not fir:
        return

    fir_series = pd.Series(fir, name="FIR").sort_values(ascending=False)

    fig = plt.figure(figsize=(6, 4))
    plt.bar(fir_series.index, fir_series.values)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Feature Influence Ratio (sum = 1)")
    plt.title("Relative importance of features (RMSE-based FIR)")
    plt.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)


def _plot_rmse_curves(pdf: PdfPages, table: pd.DataFrame) -> None:
    """
    Notebook-equivalent RMSE plots:
    For each varied feature, plot rmse_rel_<feature> vs factor if available.
    Fallback: plot rmse_rel_mean if per-feature columns are not present.
    """
    varied_features = _unique_varied_features(table)
    if not varied_features:
        return

    rmse_feature_cols = [c for c in table.columns if c.startswith("rmse_rel_") and not c.startswith("rmse_rel_si_")]
    has_per_feature = len(rmse_feature_cols) > 0
    fallback_col = "rmse_rel_mean" if "rmse_rel_mean" in table.columns else None

    for feat in varied_features:
        sub = _extract_factor_sweep(table, feat)
        if "factor" not in sub.columns:
            continue
        sub = sub.sort_values("factor")

        rmse_col = f"rmse_rel_{feat}"
        if has_per_feature and rmse_col in sub.columns:
            y = sub[rmse_col].astype(float).to_numpy()
            ylabel = f"rmse_rel ({feat})"
            title = f"RMSE_rel vs weight factor for {feat}"
        elif fallback_col is not None and fallback_col in sub.columns:
            y = sub[fallback_col].astype(float).to_numpy()
            ylabel = "rmse_rel_mean"
            title = f"RMSE_rel_mean vs weight factor (varied: {feat})"
        else:
            continue

        x = sub["factor"].astype(float).to_numpy()

        fig = plt.figure(figsize=(5, 3))
        plt.plot(x, y, marker="o")
        plt.xlabel("Weight factor applied to this feature")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)


def _plot_cross_feature_si_heatmap(pdf: PdfPages, table: pd.DataFrame) -> None:
    """
    Notebook-equivalent cross-feature sensitivity heatmap:
    - use columns rmse_rel_si_<affected_feature>
    - average over factors
    - plot matrix with consistent feature order and inverted x-axis
    """
    si_cols = [c for c in table.columns if c.startswith("rmse_rel_si_")]
    if not si_cols:
        return

    si = table[si_cols].copy()
    si.columns = [c.replace("rmse_rel_si_", "") for c in si_cols]

    lvl = _index_level_name(table, preferred=("varied_feature", "feature"))
    if lvl is None or not isinstance(table.index, pd.MultiIndex):
        return

    si_mean = si.groupby(level=lvl).mean()

    feature_order = sorted(set(si_mean.index).intersection(set(si_mean.columns)))
    if not feature_order:
        feature_order = sorted(set(si_mean.index).union(set(si_mean.columns)))

    si_mat = si_mean.reindex(index=feature_order, columns=feature_order).fillna(0.0).to_numpy(dtype=float)
    n = len(feature_order)
    if n == 0:
        return

    vmax = float(np.max(np.abs(si_mat))) if np.isfinite(si_mat).all() else 1.0
    if vmax == 0.0:
        vmax = 1.0

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    im = ax.imshow(si_mat, vmin=-vmax, vmax=vmax)

    cbar = fig.colorbar(im, ax=ax, shrink=0.85)
    cbar.set_label("Mean Sensitivity Index (RMSE_rel)")

    ax.set_yticks(range(n))
    ax.set_yticklabels(feature_order)

    ax.set_xticks(range(n))
    ax.set_xticklabels(feature_order, rotation=45, ha="right")

    ax.invert_xaxis()
    ax.grid(False)

    ax.set_title("Cross-feature sensitivity (aligned diagonals)")
    fig.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)


def _plot_structural_effects(pdf: PdfPages, table: pd.DataFrame) -> None:
    """
    Notebook-equivalent "structural effects" plots:
    tries to plot these columns if present:
    - delta_gini
    - delta_weights_pct_mean_abs
    - delta_weights_pct_max_abs
    Fallback to:
    - gini_weights (absolute, not delta)
    - delta_weights_pct (single scalar)
    """
    varied_features = _unique_varied_features(table)
    if not varied_features:
        return

    preferred_cols = ["delta_gini", "delta_weights_pct_mean_abs", "delta_weights_pct_max_abs"]
    fallback_cols: list[str] = []
    if "gini_weights" in table.columns:
        fallback_cols.append("gini_weights")
    if "delta_weights_pct" in table.columns:
        fallback_cols.append("delta_weights_pct")

    for feat in varied_features:
        sub = _extract_factor_sweep(table, feat)
        if "factor" not in sub.columns:
            continue
        sub = sub.sort_values("factor")

        cols = [c for c in preferred_cols if c in sub.columns] or [c for c in fallback_cols if c in sub.columns]
        if not cols:
            continue

        fig = plt.figure(figsize=(7, 3))
        for col in cols:
            plt.plot(
                sub["factor"].astype(float).to_numpy(),
                sub[col].astype(float).to_numpy(),
                marker="o",
                label=col,
            )

        plt.xlabel("Weight factor applied to this feature")
        plt.ylabel("Metric magnitude")
        plt.title(f"Structural effects when changing the weight of {feat}")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)


def save_sensitivity_report_pdf(report: dict[str, Any], pdf_path: Path) -> None:
    """
    Save a multi-page PDF report with plots similar to the original notebook.
    """
    _ensure_parent_dir(pdf_path)
    table = _get_table(report)
    fir = report.get("per_feature_fir", {}) or {}

    with PdfPages(pdf_path) as pdf:
        if isinstance(fir, dict):
            _plot_fir(pdf, fir)

        _plot_rmse_curves(pdf, table)
        _plot_cross_feature_si_heatmap(pdf, table)
        _plot_structural_effects(pdf, table)
