"""Unit tests for Phase 6 comparison, ranking shifts, confidence intervals, and sensitivity analysis."""
import pytest
import pandas as pd

from src.analytics.comparison_analysis import (
    compute_metric_ranking_shifts,
    find_similar_mean_divergent_tail_pairs,
    compute_confidence_intervals,
)
from src.analytics.sensitivity_analysis import (
    sample_size_sensitivity,
    temporal_period_sensitivity,
)


def _build_synthetic_cohort() -> pd.DataFrame:
    # LangA: low spread, mean ~20, p95 ~20
    # LangB: heavy tail, mean ~20 (95 calls at 5s, 5 calls at 305s -> mean=20.0, p95=305)
    # LangC: medium, mean ~50
    rows = []
    for _ in range(100):
        rows.append({"language": "LangA", "connect_time_sec": 20.0, "year": 2023})
    for _ in range(94):
        rows.append({"language": "LangB", "connect_time_sec": 2.0, "year": 2023})
    for _ in range(6):
        rows.append({"language": "LangB", "connect_time_sec": 305.0, "year": 2023})
    for _ in range(100):
        rows.append({"language": "LangC", "connect_time_sec": 50.0, "year": 2024})
    return pd.DataFrame(rows)


def test_ranking_shifts_and_divergent_tail_pairs():
    df = _build_synthetic_cohort()
    shifts = compute_metric_ranking_shifts(df, min_sample_size=50)
    assert len(shifts) == 3
    lang_b = shifts[shifts["language"] == "LangB"].iloc[0]
    # LangB is rank 2 on mean (20.18s), but rank 3 (worst) on P95 (305.0s)
    assert lang_b["rank_mean"] == 2
    assert lang_b["rank_p95"] == 3
    assert lang_b["shift_mean_to_p95"] == 1

    pairs = find_similar_mean_divergent_tail_pairs(df, min_sample_size=50, mean_tolerance_sec=1.0, min_p95_gap_sec=50.0)
    assert len(pairs) == 1
    assert {pairs.iloc[0]["language_a"], pairs.iloc[0]["language_b"]} == {"LangA", "LangB"}


def test_confidence_intervals():
    df = _build_synthetic_cohort()
    ci = compute_confidence_intervals(df["connect_time_sec"], n_bootstrap=100)
    assert ci["count"] == 300
    assert ci["mean_ci"][0] <= ci["mean"] <= ci["mean_ci"][1]
    assert ci["median_ci"][0] <= ci["median"] <= ci["median_ci"][1]
    assert ci["p95_ci"][0] <= ci["p95"] <= ci["p95_ci"][1]
    assert ci["pct_ge_300s_ci"][0] <= ci["pct_ge_300s"] <= ci["pct_ge_300s_ci"][1]


def test_sensitivity_analyses():
    df = _build_synthetic_cohort()
    s_df = sample_size_sensitivity(df, thresholds=[50, 100, 500])
    assert len(s_df) == 3
    assert s_df.iloc[0]["qualifying_languages"] == 3
    assert s_df.iloc[2]["qualifying_languages"] == 0

    t_df = temporal_period_sensitivity(df)
    assert list(t_df["year"]) == [2023, 2024]
