"""Data cleaning and normalization according to PRD Section 12.2 and 12.3."""
from typing import Tuple
import pandas as pd
import numpy as np


def clean_dataset(raw_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cleans raw dataset while strictly obeying PRD requirements:
    1. Preserves raw_language while creating normalized language column.
    2. Converts connect_time_sec to numeric float.
    3. Preserves legitimate duplicate rows (identical values across fields).
    4. Preserves extreme waiting times (e.g. >= 300s, >= 1800s).
    5. Flags and separates invalid rows (negative waits, unparseable timestamps, nulls).

    Returns:
        (valid_df, excluded_df)
    """
    df = raw_df.copy()

    # Preserve original raw language
    df["raw_language"] = df["language"]

    # Normalize language: strip whitespace, title-case for standard languages
    # Keep original text if null
    df["language"] = df["language"].astype(str).str.strip().str.title()

    # Numeric conversion for connect_time_sec
    df["connect_time_sec"] = pd.to_numeric(df["connect_time_sec"], errors="coerce")

    # Parse timestamps
    df["call_time_parsed"] = pd.to_datetime(df["call_time"], errors="coerce")

    # Validation mask
    is_valid = (
        df["call_time_parsed"].notna() &
        df["language"].notna() &
        (df["language"] != "Nan") &
        (df["language"] != "") &
        df["connect_time_sec"].notna() &
        (df["connect_time_sec"] >= 0)
    )

    valid_df = df[is_valid].copy()
    valid_df["call_time"] = valid_df["call_time_parsed"]
    valid_df = valid_df.drop(columns=["call_time_parsed"])

    excluded_df = df[~is_valid].copy()

    return valid_df, excluded_df
