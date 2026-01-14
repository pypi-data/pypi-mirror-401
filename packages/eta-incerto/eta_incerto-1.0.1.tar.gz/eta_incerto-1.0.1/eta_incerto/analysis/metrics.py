from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np


def _as_array(x) -> np.ndarray:
    if isinstance(x, dict):
        # sort by (year, period)
        return np.array(
            [v for _, v in sorted(x.items(), key=lambda kv: kv[0])],
            dtype=float,
        )
    return np.asarray(x, dtype=float).ravel()


def _pairwise_clean(ref_arr: np.ndarray, agg_arr: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Ensure same length and drop positions where either series is NaN/Inf.
    Returns cleaned (ref, agg). If nothing remains, returns empty arrays.
    """
    ref_arr = np.asarray(ref_arr, dtype=float).ravel()
    agg_arr = np.asarray(agg_arr, dtype=float).ravel()

    n = min(ref_arr.size, agg_arr.size)
    ref_arr = ref_arr[:n]
    agg_arr = agg_arr[:n]

    mask = np.isfinite(ref_arr) & np.isfinite(agg_arr)
    return ref_arr[mask], agg_arr[mask]


def rmse_rel(ref: Iterable[float], agg: Iterable[float]) -> float:
    ref_arr = _as_array(ref)
    agg_arr = _as_array(agg)
    ref_arr, agg_arr = _pairwise_clean(ref_arr, agg_arr)

    if ref_arr.size == 0:
        return float("nan")

    denom = max(np.abs(ref_arr).max(), 1e-12)
    return float(np.sqrt(np.mean((agg_arr - ref_arr) ** 2)) / denom)


def energy_bias(ref: Iterable[float], agg: Iterable[float]) -> float:
    ref_arr = _as_array(ref)
    agg_arr = _as_array(agg)
    ref_arr, agg_arr = _pairwise_clean(ref_arr, agg_arr)

    if ref_arr.size == 0:
        return float("nan")

    ref_sum = float(np.sum(ref_arr))
    agg_sum = float(np.sum(agg_arr))
    denom = max(abs(ref_sum), 1e-12)
    return abs(agg_sum - ref_sum) / denom


def peak_error(ref: Iterable[float], agg: Iterable[float]) -> float:
    ref_arr = _as_array(ref)
    agg_arr = _as_array(agg)
    ref_arr, agg_arr = _pairwise_clean(ref_arr, agg_arr)

    if ref_arr.size == 0:
        return float("nan")

    # Peak fürs Sizing: max(|x|)
    ref_peak = float(np.max(np.abs(ref_arr)))
    agg_peak = float(np.max(np.abs(agg_arr)))

    denom = max(ref_peak, 1e-12)
    return abs(agg_peak - ref_peak) / denom


def corr_pearson(ref: Iterable[float], agg: Iterable[float]) -> float:
    ref_arr = _as_array(ref)
    agg_arr = _as_array(agg)
    ref_arr, agg_arr = _pairwise_clean(ref_arr, agg_arr)

    if ref_arr.size == 0:
        return float("nan")

    if np.std(ref_arr) < 1e-12 or np.std(agg_arr) < 1e-12:
        return 0.0

    return float(np.corrcoef(ref_arr, agg_arr)[0, 1])


def sensitivity_index(
    delta_metric: float | None = None,
    delta_weight: float | None = None,
    *,
    base: float | None = None,
    variant: float | None = None,
    factor: float | None = None,
    **_,
) -> float:
    """
    Sensitivity index: |Δmetric| / |Δweight|.

    If delta_weight is not provided, we infer it from factor:
      delta_weight := |factor - 1|
    """
    if delta_metric is None:
        if base is None or variant is None:
            raise TypeError("Provide either delta_metric, or (base and variant).")
        delta_metric = float(variant) - float(base)

    if delta_weight is None:
        if factor is None:
            raise TypeError("delta_weight is required (or provide factor to infer it).")
        delta_weight = abs(float(factor) - 1.0)

    denom = abs(float(delta_weight)) or 1e-12
    return abs(float(delta_metric)) / denom


def _fir_mode_a(delta_rmse_per_feature: dict[str, float]) -> dict[str, float]:
    cleaned: dict[str, float] = {}
    for k, v in delta_rmse_per_feature.items():
        try:
            fv = float(v)
        except (TypeError, ValueError):
            fv = float("nan")
        cleaned[k] = 0.0 if np.isnan(fv) else float(abs(fv))

    total = sum(cleaned.values())
    if total <= 0.0:
        return {k: 0.0 for k in cleaned}

    return {k: v / total for k, v in cleaned.items()}


def _fir_rows_from_data(data) -> list[dict]:
    """Normalize `data` to a list[dict] for MODE B."""
    if isinstance(data, dict):
        return [data]

    if hasattr(data, "to_dict"):
        # pandas DataFrame -> list of records
        try:
            return data.to_dict(orient="records")
        except TypeError:
            return data.to_dict("records")

    # assume iterable of dicts
    try:
        return [row for row in data if isinstance(row, dict)]
    except TypeError as e:
        raise TypeError("MODE B expects dict, DataFrame, or iterable of dicts.") from e


def _fir_mode_b(data, feature: str, metric_prefix: str) -> float:
    rows = _fir_rows_from_data(data)

    values: list[float] = []
    for row in rows:
        for k, v in row.items():
            if not (isinstance(k, str) and k.startswith(metric_prefix) and feature in k):
                continue
            try:
                values.append(abs(float(v)))
            except (TypeError, ValueError):
                continue

    return max(values) if values else 0.0


def feature_influence_ratio(*args, **kwargs):
    """
    Dual-mode function.

    MODE A (old):
        feature_influence_ratio(delta_rmse_per_feature: dict[str, float]) -> dict[str, float]
        Normalizes per-feature magnitudes to sum to 1.0.

    MODE B (new):
        feature_influence_ratio(data, feature: str, metric_prefix: str = "rmse_rel_si_") -> float
        Extracts the maximum absolute metric value from rows whose key starts with metric_prefix
        and contains the given feature name.
    """
    # MODE A: (dict,) and no "feature" kw
    if len(args) == 1 and isinstance(args[0], dict) and "feature" not in kwargs:
        return _fir_mode_a(args[0])

    # MODE B: (data, feature, metric_prefix=?)
    if len(args) < 2:
        raise TypeError("feature_influence_ratio(): expected (data, feature, ...) or (dict,).")

    data, feature = args[0], args[1]
    metric_prefix = kwargs.get("metric_prefix", "rmse_rel_si_")
    return _fir_mode_b(data, feature, metric_prefix)


def gini_index(weights: Iterable[float]) -> float:
    """
    Gini index for a non-negative weight vector (0: equal, ->1: highly concentrated).
    """
    w = _as_array(weights)
    w = np.clip(w, 0.0, None)
    if w.sum() <= 0:
        return 0.0
    w = np.sort(w)
    n = w.size
    cum = np.cumsum(w)
    gini = (n + 1 - 2 * np.sum(cum) / cum[-1]) / n
    return float(max(0.0, min(1.0, gini)))


def delta_weights_pct(w_base: Iterable[float], w_var: Iterable[float]) -> float:
    """
    Scalar percent change magnitude between weight vectors.
    Returns mean absolute relative change.
    """
    base = _as_array(w_base)
    var = _as_array(w_var)

    if base.shape != var.shape:
        raise ValueError(f"Weight vectors must have same shape, got {base.shape} vs {var.shape}")

    denom = np.maximum(np.abs(base), 1e-12)
    rel = (var - base) / denom
    return float(np.mean(np.abs(rel)))


def seasonal_energy_share(series: Iterable[float], season_index: Sequence[int]) -> dict[int, float]:
    """
    Compute per-season energy share given a season index per timestep (same length as series).
    Returns a dict season -> share in [0, 1], summing to 1 (if total energy > 0).
    """
    x = _as_array(series)
    idx = np.asarray(season_index, dtype=int).ravel()
    if x.size != idx.size:
        raise ValueError("series and season_index must have the same length.")

    total = float(np.sum(np.abs(x)))
    if total <= 1e-12:
        return {}

    out: dict[int, float] = {}
    for s in np.unique(idx):
        mask = idx == s
        out[int(s)] = float(np.sum(np.abs(x[mask])) / total)
    return out


def seasonal_share_delta(share_base: dict[int, float], share_var: dict[int, float]) -> dict[int, float]:
    """
    Absolute change in seasonal shares per season key present in either dict.
    """
    seasons = set(share_base) | set(share_var)
    return {s: abs(share_var.get(s, 0.0) - share_base.get(s, 0.0)) for s in seasons}


def ldc_error(
    ref: Iterable[float],
    agg: Iterable[float],
    quantiles: Sequence[float] = (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0),
) -> float:
    """
    Average absolute deviation between load duration curves at given quantiles.
    NaN/Inf-safe: drops positions where either ref/agg is NaN/Inf.
    Returns NaN if there is no valid data left.
    """
    r = _as_array(ref)
    a = _as_array(agg)
    r, a = _pairwise_clean(r, a)

    if r.size == 0:
        return float("nan")

    r_sorted = np.sort(r)[::-1]
    a_sorted = np.sort(a)[::-1]

    def at_q(arr: np.ndarray, q: float) -> float:
        if arr.size == 0:
            return float("nan")
        q = float(q)
        pos = int(q * (arr.size - 1))
        pos = min(max(pos, 0), arr.size - 1)
        return float(arr[pos])

    errs: list[float] = []
    for q in quantiles:
        rv = at_q(r_sorted, q)
        av = at_q(a_sorted, q)
        if np.isfinite(rv) and np.isfinite(av):
            errs.append(abs(av - rv))

    if not errs:
        return float("nan")

    denom = max(float(np.max(np.abs(r_sorted))), 1e-12)
    return float(np.mean(errs) / denom)
