"""Temporal waiting-time analysis (PRD Section 8.5)."""
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np


def compute_hourly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Computes hourly metrics (hours 0-23)."""
    if df.empty or "hour" not in df.columns:
        return pd.DataFrame()

    def agg_fn(s):
        n = len(s)
        return pd.Series({
            "count": n,
            "mean": round(s.mean(), 2),
            "median": round(s.median(), 2),
            "p90": round(s.quantile(0.90), 2),
            "p95": round(s.quantile(0.95), 2),
            "calls_ge_300s": int((s >= 300.0).sum()),
            "pct_ge_300s": round(((s >= 300.0).sum() / n) * 100.0, 2) if n > 0 else 0.0,
        })

    summary = df.groupby("hour")["connect_time_sec"].apply(agg_fn).unstack().reset_index()
    return summary.sort_values("hour").reset_index(drop=True)


def compute_day_of_week_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Computes day-of-week metrics ordered Monday through Sunday."""
    if df.empty or "day_of_week" not in df.columns:
        return pd.DataFrame()

    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def agg_fn(s):
        n = len(s)
        return pd.Series({
            "count": n,
            "mean": round(s.mean(), 2),
            "median": round(s.median(), 2),
            "p90": round(s.quantile(0.90), 2),
            "p95": round(s.quantile(0.95), 2),
            "calls_ge_300s": int((s >= 300.0).sum()),
            "pct_ge_300s": round(((s >= 300.0).sum() / n) * 100.0, 2) if n > 0 else 0.0,
        })

    summary = df.groupby("day_of_week")["connect_time_sec"].apply(agg_fn).unstack().reset_index()
    summary["day_order"] = summary["day_of_week"].apply(lambda d: dow_order.index(d) if d in dow_order else 99)
    summary = summary.sort_values("day_order").drop(columns=["day_order"]).reset_index(drop=True)
    return summary


def compute_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Computes chronological monthly trend across entire dataset."""
    if df.empty or "year_month" not in df.columns:
        return pd.DataFrame()

    def agg_fn(s):
        n = len(s)
        return pd.Series({
            "count": n,
            "mean": round(s.mean(), 2),
            "median": round(s.median(), 2),
            "p90": round(s.quantile(0.90), 2),
            "p95": round(s.quantile(0.95), 2),
            "calls_ge_300s": int((s >= 300.0).sum()),
            "pct_ge_300s": round(((s >= 300.0).sum() / n) * 100.0, 2) if n > 0 else 0.0,
        })

    summary = df.groupby("year_month")["connect_time_sec"].apply(agg_fn).unstack().reset_index()
    return summary.sort_values("year_month").reset_index(drop=True)


def compute_hour_weekday_heatmap_matrix(df: pd.DataFrame, metric: str = "mean") -> pd.DataFrame:
    """
    Computes 2D matrix of Hour (rows: 0-23) by Day of Week (columns: Monday-Sunday)
    for interactive heatmap visualization. Metric can be 'mean', 'median', 'p90', or 'pct_ge_300s'.
    """
    if df.empty or "hour" not in df.columns or "day_of_week" not in df.columns:
        return pd.DataFrame()

    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if metric == "mean":
        pivot = df.pivot_table(index="hour", columns="day_of_week", values="connect_time_sec", aggfunc="mean")
    elif metric == "median":
        pivot = df.pivot_table(index="hour", columns="day_of_week", values="connect_time_sec", aggfunc="median")
    elif metric == "p90":
        pivot = df.pivot_table(index="hour", columns="day_of_week", values="connect_time_sec", aggfunc=lambda s: s.quantile(0.90))
    elif metric == "pct_ge_300s":
        pivot = df.pivot_table(index="hour", columns="day_of_week", values="connect_time_sec", aggfunc=lambda s: ((s >= 300.0).sum() / len(s)) * 100.0)
    else:
        pivot = df.pivot_table(index="hour", columns="day_of_week", values="connect_time_sec", aggfunc="mean")

    # Reindex columns to standard weekly order
    valid_cols = [c for c in dow_order if c in pivot.columns]
    pivot = pivot[valid_cols].round(2)
    return pivot
