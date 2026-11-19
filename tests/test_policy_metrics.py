"""Unit tests for municipal policy benchmark calculations."""
import pytest
import pandas as pd
from src.analytics.policy_analysis import evaluate_oti_average_goal, evaluate_statutory_review_threshold


def test_oti_goal_evaluation():
    # Spanish average = 25s (satisfies <= 30s)
    # Russian average = 40s (fails <= 30s)
    df = pd.DataFrame({
        "language": ["Spanish"] * 5 + ["Russian"] * 5,
        "connect_time_sec": [25.0] * 5 + [40.0] * 5
    })
    res_df = evaluate_oti_average_goal(df)
    assert len(res_df) == 4  # Spanish, Cantonese, Mandarin, Russian

    sp = res_df[res_df["language"] == "Spanish"].iloc[0]
    assert sp["observed_mean_sec"] == 25.0
    assert sp["delta_from_goal_sec"] == -5.0
    assert sp["satisfies_average_goal"] is True

    ru = res_df[res_df["language"] == "Russian"].iloc[0]
    assert ru["observed_mean_sec"] == 40.0
    assert ru["delta_from_goal_sec"] == 10.0
    assert ru["satisfies_average_goal"] is False


def test_statutory_review_threshold_evaluation():
    df = pd.DataFrame({
        "language": ["Spanish", "Spanish", "Russian", "Arabic"],
        "connect_time_sec": [10.0, 310.0, 50.0, 450.0]
    })
    stat_res = evaluate_statutory_review_threshold(df)
    assert stat_res["total_calls"] == 4
    assert stat_res["threshold_calls_count"] == 2
    assert stat_res["threshold_percentage"] == 50.0
    assert stat_res["official_label"] == "300-Second Statutory Review Threshold"
    assert len(stat_res["language_breakdown"]) == 2
