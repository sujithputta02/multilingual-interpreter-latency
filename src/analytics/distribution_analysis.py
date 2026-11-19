"""Distribution-sensitive analysis and comparison engine (PRD Section 8.6 & 9)."""
from typing import Any, Dict, List, Tuple
import pandas as pd
import numpy as np


def compute_mean_median_disparity(df: pd.DataFrame, min_sample_size: int = 100) -> pd.DataFrame:
    """
    Computes disparity between Mean and Median waiting times across languages (PRD Section 9).
    Highlights groups where positive skew is masked by average-only reporting.
    """
    if df.empty or "language" not in df.columns or "connect_time_sec" not in df.columns:
        return pd.DataFrame()

    def agg_fn(s):
        n = len(s)
        mean_v = s.mean()
        median_v = s.median()
        p90_v = s.quantile(0.90)
        p95_v = s.quantile(0.95)
        diff = mean_v - median_v
        tail_ratio = p95_v / median_v if median_v > 0 else np.nan

        return pd.Series({
            "count": n,
            "mean": round(mean_v, 2),
            "median": round(median_v, 2),
            "mean_minus_median": round(diff, 2),
            "p90": round(p90_v, 2),
            "p95": round(p95_v, 2),
            "p95_to_median_ratio": round(tail_ratio, 2) if not np.isnan(tail_ratio) else None,
            "calls_ge_300s": int((s >= 300.0).sum()),
            "pct_ge_300s": round(((s >= 300.0).sum() / n) * 100.0, 2) if n > 0 else 0.0,
        })

    summary = df.groupby("language")["connect_time_sec"].apply(agg_fn).unstack().reset_index()
    summary = summary[summary["count"] >= min_sample_size].sort_values(by="mean_minus_median", ascending=False).reset_index(drop=True)
    return summary


def compute_ecdf(series: pd.Series, max_points: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes Empirical Cumulative Distribution Function (ECDF).
    Subsamples evenly to max_points if series is large to ensure responsive UI rendering.
    """
    clean = series.dropna().sort_values().values
    n = len(clean)
    if n == 0:
        return np.array([]), np.array([])

    if n > max_points:
        idx = np.linspace(0, n - 1, max_points).astype(int)
        x = clean[idx]
        y = (idx + 1) / n
    else:
        x = clean
        y = np.arange(1, n + 1) / n

    return x, y
