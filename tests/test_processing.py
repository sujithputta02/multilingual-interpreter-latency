"""Unit tests for data cleaning and feature engineering."""
import pytest
import pandas as pd
from src.processing.cleaning import clean_dataset
from src.processing.features import derive_features, assign_time_period, assign_wait_category


def test_cleaning_and_duplicate_preservation():
    # Per PRD Section 11.3: identical triplet rows represent legitimate distinct calls and must NOT be dropped
    raw_df = pd.DataFrame({
        "call_time": ["2024-05-01T10:00:00.000", "2024-05-01T10:00:00.000", "2024-05-01T10:00:00.000"],
        "language": ["  spanish  ", "  spanish  ", "  spanish  "],
        "connect_time_sec": ["45", "45", "45"]
    })
    valid_df, excluded_df = clean_dataset(raw_df)
    assert len(valid_df) == 3
    assert len(excluded_df) == 0
    assert (valid_df["language"] == "Spanish").all()
    assert (valid_df["connect_time_sec"] == 45.0).all()


def test_cleaning_extreme_values_preserved():
    # Per PRD Section 12.3: extreme waiting times must be preserved
    raw_df = pd.DataFrame({
        "call_time": ["2024-05-01T10:00:00.000", "2024-05-01T11:00:00.000"],
        "language": ["Russian", "Cantonese"],
        "connect_time_sec": [350.0, 2400.0]
    })
    valid_df, excluded_df = clean_dataset(raw_df)
    assert len(valid_df) == 2
    assert 2400.0 in valid_df["connect_time_sec"].values


def test_cleaning_negative_and_null_exclusion():
    raw_df = pd.DataFrame({
        "call_time": ["2024-05-01T10:00:00.000", "2024-05-01T11:00:00.000", None],
        "language": ["Spanish", "Mandarin", "French"],
        "connect_time_sec": [-10.0, 50.0, 20.0]
    })
    valid_df, excluded_df = clean_dataset(raw_df)
    assert len(valid_df) == 1
    assert valid_df.iloc[0]["language"] == "Mandarin"
    assert len(excluded_df) == 2


def test_feature_derivation():
    df = pd.DataFrame({
        "call_time": [pd.Timestamp("2024-03-15 14:30:00")],
        "raw_language": ["Spanish"],
        "language": ["Spanish"],
        "connect_time_sec": [320.0]
    })
    features = derive_features(df)
    row = features.iloc[0]
    assert row["year"] == 2024
    assert row["month"] == 3
    assert row["hour"] == 14
    assert row["time_period"] == "Afternoon"
    assert bool(row["is_300s_or_more"]) is True
    assert bool(row["is_oti_language"]) is True
    assert row["wait_category"] == ">=300s (Statutory Review)"
