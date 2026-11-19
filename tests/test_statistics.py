"""Unit tests for statistical analysis calculations."""
import pytest
import numpy as np
import pandas as pd
from src.analytics.descriptive import calculate_descriptive_stats
from src.analytics.language_analysis import compute_language_summary
from src.analytics.distribution_analysis import compute_mean_median_disparity


def test_descriptive_statistics_synthetic():
    # Synthetic array with known properties:
    # 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 300, 500
    # Length = 12
    # Sum = 1250, Mean = 104.17
    # Median between 50 and 60 = 55.0
    data = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 300, 500]
    res = calculate_descriptive_stats(data)

    assert res["count"] == 12
    assert res["mean"] == pytest.approx(104.17, abs=0.01)
    assert res["median"] == 55.0
    assert res["min"] == 0.0
    assert res["max"] == 500.0
    assert res["long_wait_count"] == 2
    assert res["long_wait_percentage"] == pytest.approx((2/12)*100, abs=0.01)
    assert res["p90"] is not None
    assert res["p95"] is not None


def test_language_summary_grouping():
    df = pd.DataFrame({
        "language": ["Spanish"] * 10 + ["Cantonese"] * 5,
        "connect_time_sec": [20.0] * 9 + [350.0] + [15.0] * 5
    })
    summary = compute_language_summary(df, min_sample_size=6)
    assert len(summary) == 2
    sp_row = summary[summary["language"] == "Spanish"].iloc[0]
    assert sp_row["count"] == 10
    assert sp_row["calls_ge_300s"] == 1
    assert sp_row["pct_ge_300s"] == 10.0
    assert bool(sp_row["has_sufficient_sample"]) is True

    cant_row = summary[summary["language"] == "Cantonese"].iloc[0]
    assert cant_row["count"] == 5
    assert bool(cant_row["has_sufficient_sample"]) is False
