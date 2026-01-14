"""
Sensitivity analysis module for the typical-periods computation.

This file orchestrates baseline and variant runs of the typical-periods
generation (by calling the domain logic in periods/data_to_periods.py),
computes quality and sensitivity metrics, aggregates all results, and
(optionally) stores them for reporting.

Only the adapter function `run_periods_and_extract()` must be customized
to connect to your actual typical-periods implementation.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypedDict

import numpy as np
import pandas as pd

from eta_incerto.periods.analysis_adapter import generate_typical_result

from .metrics import (
    corr_pearson,
    delta_weights_pct,
    energy_bias,
    feature_influence_ratio,
    gini_index,
    peak_error,
    rmse_rel,
    seasonal_energy_share,
    seasonal_share_delta,
    sensitivity_index,
)
from .sensitivity_reporting import save_sensitivity_report_pdf

if TYPE_CHECKING:
    from eta_incerto.config.config import ConfigOptimization


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


class TypicalResult(TypedDict):
    """
    Canonical in-memory representation of a typical-periods output.

    All downstream analysis modules depend only on this structure, not on the
    internal implementation of the typical-periods algorithm.
    """

    reconstruct: dict[str, np.ndarray]  # full reconstructed series per feature
    weights: dict[int, float]  # period_id -> global weight (sum ≈ 1)
    season_of_period: dict[int, int]  # period_id -> season_id (optional)
    steps_per_period: int  # number of timesteps per typical period
    meta: dict[str, Any]  # metadata: K, seed, std_target, etc.


@dataclass(frozen=True)
class StdTargetSweepConfig:
    """
    Configuration for a one-at-a-time std_target sensitivity sweep.
    """

    dataset_path: str
    columns: Sequence[str]
    std_target_base: Mapping[str, float]
    k: int
    seed: int
    variation_factors: Sequence[float]
    len_period: int

    # Optional settings for the aggregation method
    cluster_method: str = "hierarchical"

    # Optional outputs
    results_dir: str | None = None

    # Optional season index for seasonal-share metrics
    season_index: Sequence[int] | None = None


class SensitivityReport(TypedDict):
    """
    Bundle of all outputs of the std_target sensitivity sweep.

    table: per-run metrics table (MultiIndex by varied_feature and factor)
    per_feature_fir: Feature Influence Ratio per varied feature
    summary: light-weight dict suitable for JSON export
    """

    table: pd.DataFrame
    per_feature_fir: dict[str, float]
    summary: dict[str, Any]


# ---------------------------------------------------------------------------
# Adapter: typical-periods runner (must not import TSAM directly)
# ---------------------------------------------------------------------------


def run_periods_and_extract(
    df: pd.DataFrame,
    columns: Sequence[str],
    std_target: Mapping[str, float],
    k: int,
    seed: int,
    len_period: int,
    cluster_method: str = "hierarchical",
) -> TypicalResult:
    """
    Adapter around eta-incerto's domain logic for typical-period generation.

    Notes
    -----
    - This function must NOT import TSAM directly.
    - TSAM (if used) must remain encapsulated inside eta_incerto.periods.
    """
    return generate_typical_result(
        df=df,
        columns=columns,
        std_target=std_target,
        k=k,
        seed=seed,
        len_period=len_period,
        cluster_method=cluster_method,
    )


# ---------------------------------------------------------------------------
# Metrics helpers
# ---------------------------------------------------------------------------


def _compute_quality_metrics_per_feature(ref: np.ndarray, recon: np.ndarray) -> dict[str, float]:
    """
    Compute feature-level quality metrics between reference and reconstruction.
    """
    return {
        "rmse_rel": float(rmse_rel(ref, recon)),
        "corr": float(corr_pearson(ref, recon)),
        "peak_error": float(peak_error(ref, recon)),
    }


def _seasonal_share_delta_mean(
    df_ref: pd.DataFrame,
    df_recon: pd.DataFrame,
    columns: Sequence[str],
    season_index: Sequence[int],
) -> float:
    """
    Compute mean seasonal-share delta across all features.

    Note: seasonal_energy_share() in metrics.py expects a single series and a season_index,
    so we aggregate per feature and then average the deltas.
    """
    deltas: list[float] = []
    for col in columns:
        share_ref = seasonal_energy_share(df_ref[col].to_numpy(), season_index)
        share_rec = seasonal_energy_share(df_recon[col].to_numpy(), season_index)
        per_season_delta = seasonal_share_delta(share_ref, share_rec)
        deltas.append(float(np.mean(list(per_season_delta.values()))) if per_season_delta else 0.0)
    return float(np.mean(deltas)) if deltas else 0.0


def _compute_global_quality_metrics(
    df_ref: pd.DataFrame,
    df_recon: pd.DataFrame,
    columns: Sequence[str],
    season_index: Sequence[int] | None = None,
) -> dict[str, float]:
    """
    Compute global metrics aggregated over all features.

    This includes energy bias and optional seasonal metrics if season_index is
    provided.
    """
    energy_biases: list[float] = [energy_bias(df_ref[col].to_numpy(), df_recon[col].to_numpy()) for col in columns]
    metrics: dict[str, float] = {"energy_bias_mean": float(np.mean(energy_biases))}

    if season_index is not None:
        metrics["seasonal_share_delta"] = _seasonal_share_delta_mean(df_ref, df_recon, columns, season_index)

    return metrics


def _weights_metrics(weights: Mapping[int, float]) -> dict[str, float]:
    """
    Compute basic weight distribution metrics (Gini index).
    """
    w = np.array(list(weights.values()), dtype=float)
    return {"gini_weights": float(gini_index(w))}


def _apply_nan_strategy(df_ref: pd.DataFrame) -> pd.DataFrame:
    """
    Robust NaN/Inf handling for the reference dataframe (config-independent).

    Strategy:
    1) Replace inf/-inf with NaN
    2) Time-consistent interpolation (both directions)
    3) Final fallback fill with 0.0 (so metrics never see NaN)
    """
    clean_df = df_ref.replace([np.inf, -np.inf], np.nan)
    clean_df = clean_df.interpolate(limit_direction="both")
    return clean_df.fillna(0.0)


# ---------------------------------------------------------------------------
# Main entry: one-at-a-time std_target sensitivity sweep
# ---------------------------------------------------------------------------


def run_std_target_sensitivity(config: StdTargetSweepConfig) -> SensitivityReport:
    """
    Execute a one-at-a-time sensitivity sweep over std_target weights.
    """
    raw_df = pd.read_csv(config.dataset_path)
    columns = list(config.columns)

    # If the dataset contains a Time column, set it as DateTimeIndex.
    if "Time" in raw_df.columns:
        raw_df["Time"] = pd.to_datetime(raw_df["Time"], errors="raise")
        raw_df = raw_df.set_index("Time")

    ts_df = raw_df.sort_index()

    # Reference data
    df_ref = ts_df.loc[:, columns].astype(float).copy()
    df_ref = _apply_nan_strategy(df_ref)

    # Baseline run
    baseline = run_periods_and_extract(
        df=df_ref,
        columns=columns,
        std_target=config.std_target_base,
        k=config.k,
        seed=config.seed,
        len_period=config.len_period,
        cluster_method=config.cluster_method,
    )

    df_recon_base = pd.DataFrame({c: baseline["reconstruct"][c] for c in columns}, index=df_ref.index)

    # Baseline metrics per feature
    base_metrics_per_feature: dict[str, dict[str, float]] = {}
    for col in columns:
        base_metrics_per_feature[col] = _compute_quality_metrics_per_feature(
            df_ref[col].to_numpy(),
            df_recon_base[col].to_numpy(),
        )

    # Baseline global metrics
    base_global_metrics = _compute_global_quality_metrics(
        df_ref=df_ref,
        df_recon=df_recon_base,
        columns=columns,
        season_index=config.season_index,
    )

    base_weight_metrics = _weights_metrics(baseline["weights"])

    # Collect rows for the result table
    rows: list[dict[str, Any]] = []
    index: list[tuple[str, float]] = []

    for varied_feature in columns:
        for factor in config.variation_factors:
            variant_std_target = dict(config.std_target_base)
            variant_std_target[varied_feature] = float(variant_std_target[varied_feature] * factor)

            variant = run_periods_and_extract(
                df=df_ref,
                columns=columns,
                std_target=variant_std_target,
                k=config.k,
                seed=config.seed,
                len_period=config.len_period,
                cluster_method=config.cluster_method,
            )

            df_recon_var = pd.DataFrame({c: variant["reconstruct"][c] for c in columns}, index=df_ref.index)

            var_metrics_per_feature: dict[str, dict[str, float]] = {}
            for col in columns:
                var_metrics_per_feature[col] = _compute_quality_metrics_per_feature(
                    df_ref[col].to_numpy(),
                    df_recon_var[col].to_numpy(),
                )

            var_global_metrics = _compute_global_quality_metrics(
                df_ref=df_ref,
                df_recon=df_recon_var,
                columns=columns,
                season_index=config.season_index,
            )

            var_weight_metrics = _weights_metrics(variant["weights"])

            row: dict[str, Any] = {
                "varied_feature": varied_feature,
                "factor": float(factor),
                "rmse_rel_mean": float(np.mean([var_metrics_per_feature[c]["rmse_rel"] for c in columns])),
                "corr_mean": float(np.mean([var_metrics_per_feature[c]["corr"] for c in columns])),
                "peak_error_mean": float(np.mean([var_metrics_per_feature[c]["peak_error"] for c in columns])),
                "energy_bias_mean": float(var_global_metrics["energy_bias_mean"]),
                "gini_weights": float(var_weight_metrics["gini_weights"]),
                "delta_weights_pct": float(delta_weights_pct(baseline["weights"], variant["weights"])),
            }

            if "seasonal_share_delta" in var_global_metrics:
                row["seasonal_share_delta"] = float(var_global_metrics["seasonal_share_delta"])

            for affected_feature in columns:
                si = sensitivity_index(
                    base=base_metrics_per_feature[affected_feature]["rmse_rel"],
                    variant=var_metrics_per_feature[affected_feature]["rmse_rel"],
                    factor=float(factor),
                )
                row[f"rmse_rel_si_{affected_feature}"] = float(si)

            rows.append(row)
            index.append((varied_feature, float(factor)))

    table = pd.DataFrame(rows)
    table.index = pd.MultiIndex.from_tuples(index, names=["varied_feature", "factor"])

    per_feature_fir: dict[str, float] = {
        feature: float(feature_influence_ratio(table, feature, metric_prefix="rmse_rel_si_")) for feature in columns
    }

    summary: dict[str, Any] = {
        "baseline": {
            "rmse_rel_mean": float(np.mean([base_metrics_per_feature[c]["rmse_rel"] for c in columns])),
            "corr_mean": float(np.mean([base_metrics_per_feature[c]["corr"] for c in columns])),
            "peak_error_mean": float(np.mean([base_metrics_per_feature[c]["peak_error"] for c in columns])),
            **base_global_metrics,
            **base_weight_metrics,
        },
        "per_feature_fir": per_feature_fir,
        "meta": {
            "dataset_path": str(config.dataset_path),
            "columns": list(columns),
            "K": int(config.k),
            "seed": int(config.seed),
            "len_period": int(config.len_period),
            "cluster_method": str(config.cluster_method),
            "variation_factors": list(map(float, config.variation_factors)),
            "std_target_base": {k: float(v) for k, v in config.std_target_base.items()},
        },
    }

    report: SensitivityReport = {"table": table, "per_feature_fir": per_feature_fir, "summary": summary}

    if config.results_dir is not None:
        results_dir = Path(config.results_dir)
        results_dir.mkdir(parents=True, exist_ok=True)

        table_path = results_dir / "std_target_sensitivity.parquet"
        summary_path = results_dir / "std_target_sensitivity_summary.json"

        table.to_parquet(table_path)
        with summary_path.open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

    return report


# ---------------------------------------------------------------------------
# Production entry point: config-driven run (called from EtaIncerto)
# ---------------------------------------------------------------------------


def run_std_target_sensitivity_from_config(config: ConfigOptimization) -> None:
    """
    Run std_target sensitivity based purely on eta-incerto configuration.
    """
    base_results_dir = Path(config.paths.results_dir) / config.analysis.results_subdir
    base_plots_dir = Path(config.paths.plots_dir)

    base_results_dir.mkdir(parents=True, exist_ok=True)
    base_plots_dir.mkdir(parents=True, exist_ok=True)

    for sf in config.series.series_file:
        dataset_path = Path(sf.raw_data_path)
        columns = list(sf.series_names.keys())

        if len(sf.std_target) != len(columns):
            raise ValueError(
                f"Length mismatch: sf.std_target must match sf.series_names ({len(sf.std_target)} != {len(columns)})."
            )

        std_target_base = {col: float(w) for col, w in zip(columns, sf.std_target)}

        results_dir = base_results_dir / sf.file_name
        results_dir.mkdir(parents=True, exist_ok=True)

        plots_dir = base_plots_dir / sf.file_name
        plots_dir.mkdir(parents=True, exist_ok=True)

        sweep_cfg = StdTargetSweepConfig(
            dataset_path=str(dataset_path),
            columns=columns,
            std_target_base=std_target_base,
            k=int(sf.n_typical_periods),
            seed=int(getattr(config.analysis, "seed", 0)),
            variation_factors=list(getattr(config.analysis, "factors", [0.5, 0.75, 1.0, 1.25, 1.5])),
            len_period=int(sf.len_period),
            cluster_method=str(getattr(sf, "cluster_method", "hierarchical")),
            results_dir=str(results_dir),
            season_index=None,
        )

        report = run_std_target_sensitivity(sweep_cfg)

        if bool(getattr(config.analysis, "make_plots", True)):
            pdf_name = str(getattr(config.analysis, "pdf_name", "sensitivity_report.pdf"))
            pdf_path = plots_dir / pdf_name
            save_sensitivity_report_pdf(report, pdf_path)
