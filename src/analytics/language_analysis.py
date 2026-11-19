"""Language-wise waiting-time analysis (PRD Section 8.4)."""
from typing import Dict, List, Optional
import pandas as pd
import numpy as np


def compute_language_summary(
    df: pd.DataFrame,
    min_sample_size: int = 100,
    sort_by: str = "count",
    ascending: bool = False
) -> pd.DataFrame:
    """
    Computes comprehensive language-wise metrics:
    Call volume, Mean, Median, P90, P95, Std, IQR, Long-wait count (>=300s), Long-wait %
    Flags groups with sample size < min_sample_size as having limited statistical support.
    """
    if df.empty or "language" not in df.columns or "connect_time_sec" not in df.columns:
        return pd.DataFrame()

    def agg_stats(s):
        n = len(s)
        mean_v = s.mean()
        median_v = s.median()
        p90_v = s.quantile(0.90)
        p95_v = s.quantile(0.95)
        std_v = s.std() if n > 1 else 0.0
        iqr_v = s.quantile(0.75) - s.quantile(0.25)
        lw_count = (s >= 300.0).sum()
        lw_pct = (lw_count / n) * 100.0 if n > 0 else 0.0

        return pd.Series({
            "count": n,
            "mean": round(mean_v, 2),
            "median": round(median_v, 2),
            "p90": round(p90_v, 2),
            "p95": round(p95_v, 2),
            "std": round(std_v, 2),
            "iqr": round(iqr_v, 2),
            "calls_ge_300s": int(lw_count),
            "pct_ge_300s": round(lw_pct, 2),
        })

    summary = df.groupby("language")["connect_time_sec"].apply(agg_stats).unstack().reset_index()
    summary["has_sufficient_sample"] = summary["count"] >= min_sample_size

    if sort_by in summary.columns:
        summary = summary.sort_values(by=sort_by, ascending=ascending).reset_index(drop=True)

    return summary


def compare_languages(df: pd.DataFrame, selected_languages: List[str]) -> pd.DataFrame:
    """
    Generates comparison table for explicitly selected languages.
    """
    filtered = df[df["language"].isin(selected_languages)]
    return compute_language_summary(filtered, min_sample_size=1, sort_by="count", ascending=False)
