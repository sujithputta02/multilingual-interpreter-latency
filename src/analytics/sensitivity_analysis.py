"""Sensitivity analysis across sample-size thresholds and temporal periods (PRD Phase 6)."""
from typing import List, Optional
import pandas as pd
import numpy as np

from src.analytics.language_analysis import compute_language_summary
from src.analytics.policy_analysis import evaluate_oti_average_goal


def sample_size_sensitivity(
    df: pd.DataFrame,
    thresholds: Optional[List[int]] = None,
) -> pd.DataFrame:
    """
    Evaluates how many languages qualify and how top/worst rankings behave
    across minimum sample-size cutoffs (e.g., 30, 50, 100, 500, 1000).
    """
    if thresholds is None:
        thresholds = [30, 50, 100, 500, 1000]

    if df.empty:
        return pd.DataFrame()

    base = compute_language_summary(df, min_sample_size=1)
    total_langs = len(base)
    total_calls = len(df)

    rows = []
    for k in thresholds:
        elig = base[base["count"] >= k]
        covered_calls = int(elig["count"].sum())
        max_mean_lang = elig.sort_values("mean", ascending=False).iloc[0]["language"] if not elig.empty else None
        max_mean_val = float(elig["mean"].max()) if not elig.empty else None
        max_p95_lang = elig.sort_values("p95", ascending=False).iloc[0]["language"] if not elig.empty else None
        max_p95_val = float(elig["p95"].max()) if not elig.empty else None

        rows.append({
            "min_sample_threshold": k,
            "qualifying_languages": len(elig),
            "excluded_languages": total_langs - len(elig),
            "calls_covered": covered_calls,
            "calls_coverage_pct": round((covered_calls / total_calls) * 100.0, 2) if total_calls > 0 else 0.0,
            "highest_mean_language": max_mean_lang,
            "highest_mean_sec": max_mean_val,
            "highest_p95_language": max_p95_lang,
            "highest_p95_sec": max_p95_val,
        })

    return pd.DataFrame(rows)


def temporal_period_sensitivity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluates stability of core metrics and policy benchmarks across calendar years
    (or available year_month quarters) to test temporal sensitivity.
    """
    if df.empty or "year" not in df.columns:
        return pd.DataFrame()

    rows = []
    for yr, sub in df.groupby("year"):
        s = sub["connect_time_sec"]
        n = len(s)
        ge_300 = int((s >= 300.0).sum())
        oti = evaluate_oti_average_goal(sub)
        oti_map = {r["language"]: r["observed_mean_sec"] for _, r in oti.iterrows()} if not oti.empty else {}

        rows.append({
            "year": int(yr),
            "total_calls": n,
            "distinct_languages": int(sub["language"].nunique()),
            "overall_mean_sec": round(float(s.mean()), 2),
            "overall_median_sec": round(float(s.median()), 2),
            "overall_p90_sec": round(float(s.quantile(0.90)), 2),
            "overall_p95_sec": round(float(s.quantile(0.95)), 2),
            "calls_ge_300s": ge_300,
            "pct_ge_300s": round((ge_300 / n) * 100.0, 2) if n > 0 else 0.0,
            "spanish_mean_sec": oti_map.get("Spanish"),
            "cantonese_mean_sec": oti_map.get("Cantonese"),
            "mandarin_mean_sec": oti_map.get("Mandarin"),
            "russian_mean_sec": oti_map.get("Russian"),
        })

    return pd.DataFrame(rows).sort_values("year").reset_index(drop=True)
