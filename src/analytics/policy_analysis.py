"""Policy benchmark assessment engine (PRD Section 6)."""
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np

OTI_COVERED_LANGUAGES = ["Spanish", "Cantonese", "Mandarin", "Russian"]
OTI_TARGET_SECONDS = 30.0
STATUTORY_REVIEW_THRESHOLD_SECONDS = 300.0


def evaluate_oti_average_goal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluates observed performance against the NYC OTI 2024 Language Access
    Implementation Plan 30-second average goal for the four specified languages:
    Spanish, Cantonese, Mandarin, Russian (PRD Section 6.1).
    """
    if df.empty or "language" not in df.columns or "connect_time_sec" not in df.columns:
        return pd.DataFrame()

    results = []
    for lang in OTI_COVERED_LANGUAGES:
        lang_data = df[df["language"].str.lower() == lang.lower()]["connect_time_sec"]
        n = len(lang_data)
        if n > 0:
            mean_val = float(lang_data.mean())
            delta = float(mean_val - OTI_TARGET_SECONDS)
            meets_goal = mean_val <= OTI_TARGET_SECONDS
            median_val = float(lang_data.median())
            p90_val = float(lang_data.quantile(0.90))
            p95_val = float(lang_data.quantile(0.95))
            ge_300_count = int((lang_data >= STATUTORY_REVIEW_THRESHOLD_SECONDS).sum())
            ge_300_pct = float((ge_300_count / n) * 100.0)

            results.append({
                "language": lang,
                "record_count": n,
                "observed_mean_sec": round(mean_val, 2),
                "reference_goal_sec": OTI_TARGET_SECONDS,
                "delta_from_goal_sec": round(delta, 2),
                "satisfies_average_goal": meets_goal,
                "observed_median_sec": round(median_val, 2),
                "observed_p90_sec": round(p90_val, 2),
                "observed_p95_sec": round(p95_val, 2),
                "calls_ge_300s": ge_300_count,
                "pct_ge_300s": round(ge_300_pct, 2),
            })
        else:
            results.append({
                "language": lang,
                "record_count": 0,
                "observed_mean_sec": None,
                "reference_goal_sec": OTI_TARGET_SECONDS,
                "delta_from_goal_sec": None,
                "satisfies_average_goal": None,
                "observed_median_sec": None,
                "observed_p90_sec": None,
                "observed_p95_sec": None,
                "calls_ge_300s": 0,
                "pct_ge_300s": 0.0,
            })

    return pd.DataFrame(results)


def evaluate_statutory_review_threshold(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Evaluates records meeting or exceeding the 300-second statutory review threshold
    under NYC Administrative Code §23-310 (PRD Section 6.2).
    """
    if df.empty or "connect_time_sec" not in df.columns:
        return {
            "total_calls": 0,
            "threshold_calls_count": 0,
            "threshold_percentage": 0.0,
            "language_breakdown": pd.DataFrame(),
            "temporal_distribution": pd.DataFrame(),
        }

    total_n = len(df)
    threshold_mask = df["connect_time_sec"] >= STATUTORY_REVIEW_THRESHOLD_SECONDS
    threshold_df = df[threshold_mask]
    threshold_n = len(threshold_df)
    pct = (threshold_n / total_n) * 100.0 if total_n > 0 else 0.0

    # Language breakdown of threshold calls
    lang_agg = df.groupby("language").agg(
        total_calls=("connect_time_sec", "count"),
        threshold_calls=("connect_time_sec", lambda s: (s >= STATUTORY_REVIEW_THRESHOLD_SECONDS).sum())
    ).reset_index()
    lang_agg["threshold_percentage"] = (lang_agg["threshold_calls"] / lang_agg["total_calls"]) * 100.0
    lang_agg = lang_agg[lang_agg["threshold_calls"] > 0].sort_values(by="threshold_calls", ascending=False).reset_index(drop=True)

    # Sub-300s vs >=300s comparison
    standard_calls = df[~threshold_mask]["connect_time_sec"]
    review_calls = threshold_df["connect_time_sec"]

    distribution_comparison = {
        "standard_calls": {
            "count": len(standard_calls),
            "mean": round(float(standard_calls.mean()), 2) if not standard_calls.empty else 0.0,
            "median": round(float(standard_calls.median()), 2) if not standard_calls.empty else 0.0,
            "p90": round(float(standard_calls.quantile(0.90)), 2) if not standard_calls.empty else 0.0,
        },
        "review_threshold_calls": {
            "count": len(review_calls),
            "mean": round(float(review_calls.mean()), 2) if not review_calls.empty else 0.0,
            "median": round(float(review_calls.median()), 2) if not review_calls.empty else 0.0,
            "p90": round(float(review_calls.quantile(0.90)), 2) if not review_calls.empty else 0.0,
            "min": round(float(review_calls.min()), 2) if not review_calls.empty else 0.0,
            "max": round(float(review_calls.max()), 2) if not review_calls.empty else 0.0,
        }
    }

    return {
        "total_calls": total_n,
        "threshold_calls_count": threshold_n,
        "threshold_percentage": round(pct, 2),
        "language_breakdown": lang_agg,
        "distribution_comparison": distribution_comparison,
        "citation": "NYC Administrative Code §23-310",
        "official_label": "300-Second Statutory Review Threshold",
    }
