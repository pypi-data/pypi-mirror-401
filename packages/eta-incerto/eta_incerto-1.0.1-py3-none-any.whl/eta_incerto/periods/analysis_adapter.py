"""
Analysis adapter for typical-period generation.

This module provides a small, analysis-focused API that wraps the typical-period
generation and reconstruction. It keeps TSAM usage out of the analysis modules
(e.g., eta_incerto.analysis.sensitivity).

Important:
- sensitivity.py must NOT import TSAM directly.
- TSAM usage is encapsulated here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


def _import_tsam():
    try:
        from tsam.timeseriesaggregation import TimeSeriesAggregation  # type: ignore

        return TimeSeriesAggregation
    except ImportError as exc:
        raise ImportError(
            "TSAM is required for typical-period generation but is not installed. "
            "Please install `tsam` in your environment."
        ) from exc


def _ensure_datetime_index(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    ts_df = df.loc[:, list(columns)].astype(float).copy()

    if not isinstance(ts_df.index, pd.DatetimeIndex):
        if "Time" in df.columns:
            ts_df.index = pd.to_datetime(df["Time"], errors="raise")
        else:
            raise ValueError("Input data must have a DatetimeIndex or a 'Time' column that can be parsed as datetime.")

    return ts_df.sort_index()


def _clean_and_truncate(ts_df: pd.DataFrame, len_period: int) -> pd.DataFrame:
    ts_df = ts_df.interpolate(limit_direction="both").ffill().bfill()

    n = (len(ts_df) // len_period) * len_period
    if n <= 0:
        raise ValueError("Not enough data to build even one full period.")
    return ts_df.iloc[:n, :]


def _weight_dict(std_target: Mapping[str, float], columns: Sequence[str]) -> dict[str, float]:
    weights_arr = np.array([float(std_target[c]) for c in columns], dtype=float)
    mean_w = float(np.mean(weights_arr))
    denom = mean_w if abs(mean_w) > 1e-12 else 1.0
    weights_arr = weights_arr / denom
    return {c: float(w) for c, w in zip(columns, weights_arr)}


def _season_frames(ts_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    months = ts_df.index.month
    return {
        "summer": ts_df[months.isin((6, 7, 8))],
        "winter": ts_df[months.isin((12, 1, 2))],
        "transition": ts_df[months.isin((3, 4, 5, 9, 10, 11))],
    }


@dataclass(frozen=True)
class _SeasonAggContext:
    tsa_cls: Any
    k_per_season: int
    len_period: int
    cluster_method: str
    weight_dict: dict[str, float]
    columns: Sequence[str]


def _add_season_result(
    *,
    ctx: _SeasonAggContext,
    season_df: pd.DataFrame,
    season_id: int,
    full_reconstruct: pd.DataFrame,
    combined_weights: dict[int, float],
    season_of_period: dict[int, int],
    global_offset: int,
) -> int:
    agg = ctx.tsa_cls(
        season_df,
        noTypicalPeriods=ctx.k_per_season,
        hoursPerPeriod=ctx.len_period,
        clusterMethod=ctx.cluster_method,
        segmentation=False,
        weightDict=ctx.weight_dict,
        rescaleClusterPeriods=True,
    )
    _ = agg.createTypicalPeriods()

    pred_df = agg.predictOriginalData()
    if not isinstance(pred_df, pd.DataFrame):
        raise RuntimeError("TSAM predictOriginalData() did not return a DataFrame.")

    pred_df = pred_df.loc[:, list(ctx.columns)].astype(float)
    full_reconstruct.loc[pred_df.index, list(ctx.columns)] = pred_df.to_numpy()

    cluster_ids = list(agg.clusterPeriodIdx)
    id_map = {cid: (global_offset + i + 1) for i, cid in enumerate(cluster_ids)}

    counts = agg.clusterPeriodNoOccur
    total = float(sum(counts.values())) if counts else 1.0

    for cid, cnt in counts.items():
        pid = id_map[cid]
        w = float(cnt) / total
        combined_weights[pid] = combined_weights.get(pid, 0.0) + w / 3.0
        season_of_period[pid] = season_id

    return global_offset + len(cluster_ids)


def _normalize_weights(combined_weights: dict[int, float], k: int) -> dict[int, float]:
    total_w = float(sum(combined_weights.values()))
    if total_w > 0.0:
        return {int(pid): float(w / total_w) for pid, w in combined_weights.items()}
    return {i + 1: 1.0 / float(k) for i in range(k)}


def _build_reconstruct(full_reconstruct: pd.DataFrame, columns: Sequence[str]) -> dict[str, np.ndarray]:
    if full_reconstruct.isna().any().any():
        full_reconstruct = full_reconstruct.ffill().bfill()

    return {c: np.asarray(full_reconstruct[c].to_numpy(), dtype=float) for c in columns}


def generate_typical_result(
    df: pd.DataFrame,
    columns: Sequence[str],
    std_target: Mapping[str, float],
    k: int,
    seed: int,
    len_period: int,
    cluster_method: str = "hierarchical",
) -> dict[str, Any]:
    """
    Generate typical periods and a full reconstruction for sensitivity analysis.

    Returns a dictionary compatible with `TypicalResult` in sensitivity.py.
    """
    tsa_cls = _import_tsam()

    missing_cols = [c for c in columns if c not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing required columns in df: {missing_cols}")

    ts_df = _ensure_datetime_index(df, columns)
    ts_df = _clean_and_truncate(ts_df, len_period)

    weight_dict = _weight_dict(std_target, columns)

    season_frames = _season_frames(ts_df)
    season_ids = {"summer": 0, "winter": 1, "transition": 2}

    k_per_season = max(1, int(round(k / 3)))

    ctx = _SeasonAggContext(
        tsa_cls=tsa_cls,
        k_per_season=k_per_season,
        len_period=len_period,
        cluster_method=cluster_method,
        weight_dict=weight_dict,
        columns=columns,
    )

    full_reconstruct = pd.DataFrame(index=ts_df.index, columns=list(columns), dtype=float)
    combined_weights: dict[int, float] = {}
    season_of_period: dict[int, int] = {}
    global_offset = 0

    for season_name in ("summer", "winter", "transition"):
        season_df = season_frames[season_name]
        if season_df.empty:
            continue

        global_offset = _add_season_result(
            ctx=ctx,
            season_df=season_df,
            season_id=season_ids[season_name],
            full_reconstruct=full_reconstruct,
            combined_weights=combined_weights,
            season_of_period=season_of_period,
            global_offset=global_offset,
        )

    combined_weights = _normalize_weights(combined_weights, k)
    reconstruct = _build_reconstruct(full_reconstruct, columns)

    return {
        "reconstruct": reconstruct,
        "weights": {int(pid): float(w) for pid, w in combined_weights.items()},
        "season_of_period": {int(pid): int(s) for pid, s in season_of_period.items()},
        "steps_per_period": int(len_period),
        "meta": {
            "K": int(k),
            "seed": int(seed),
            "len_period": int(len_period),
            "cluster_method": str(cluster_method),
            "std_target": {str(name): float(val) for name, val in std_target.items()},
        },
    }
