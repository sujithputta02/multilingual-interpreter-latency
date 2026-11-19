"""Data quality and integrity checks."""
from datetime import datetime, timezone
from typing import Any, Dict
import pandas as pd
import numpy as np


def run_data_quality_checks(raw_df: pd.DataFrame, source_metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Performs comprehensive data quality audit as mandated by PRD Section 12.5.
    Returns a data quality report dictionary.
    """
    total_records = len(raw_df)
    missing_call_time = int(raw_df["call_time"].isna().sum()) if "call_time" in raw_df.columns else total_records
    missing_language = int(raw_df["language"].isna().sum()) if "language" in raw_df.columns else total_records
    missing_connect_time = int(raw_df["connect_time_sec"].isna().sum()) if "connect_time_sec" in raw_df.columns else total_records

    # Numeric conversion check for connect_time_sec
    numeric_connect_time = pd.to_numeric(raw_df["connect_time_sec"], errors="coerce")
    non_numeric_connect_time = int(numeric_connect_time.isna().sum() - missing_connect_time)
    negative_connect_time = int((numeric_connect_time < 0).sum())

    # Extreme value observations (PRD Section 12.3 - must inspect, not exclude)
    calls_300s_or_more = int((numeric_connect_time >= 300).sum())
    calls_1800s_or_more = int((numeric_connect_time >= 1800).sum())

    # Timestamp parsing diagnostic
    parsed_timestamps = pd.to_datetime(raw_df["call_time"], errors="coerce")
    invalid_timestamps = int(parsed_timestamps.isna().sum() - missing_call_time)

    # Duplicate rows check (PRD Section 11.3: identical rows represent legitimate distinct calls)
    identical_rows_count = int(raw_df.duplicated(subset=["call_time", "language", "connect_time_sec"]).sum())

    # Date range and languages
    valid_dates = parsed_timestamps.dropna()
    min_date = valid_dates.min().isoformat() if not valid_dates.empty else None
    max_date = valid_dates.max().isoformat() if not valid_dates.empty else None

    distinct_languages_count = int(raw_df["language"].dropna().str.strip().str.title().nunique()) if "language" in raw_df.columns else 0

    # Valid records count (excluding rows with missing critical fields or negative wait times)
    valid_mask = (
        parsed_timestamps.notna() &
        raw_df["language"].notna() &
        (raw_df["language"].astype(str).str.strip() != "") &
        numeric_connect_time.notna() &
        (numeric_connect_time >= 0)
    )
    valid_records_count = int(valid_mask.sum())
    invalid_records_count = total_records - valid_records_count

    report = {
        "report_generated_utc": datetime.now(timezone.utc).isoformat(),
        "source_metadata": source_metadata or {},
        "original_record_count": total_records,
        "valid_record_count": valid_records_count,
        "invalid_record_count": invalid_records_count,
        "missing_values": {
            "call_time": missing_call_time,
            "language": missing_language,
            "connect_time_sec": missing_connect_time,
        },
        "anomalies": {
            "non_numeric_connect_time": non_numeric_connect_time,
            "negative_connect_time": negative_connect_time,
            "invalid_timestamps": invalid_timestamps,
            "identical_triplet_records_preserved": identical_rows_count,
        },
        "extreme_values_retained": {
            "statutory_threshold_300s_or_more": calls_300s_or_more,
            "severe_threshold_1800s_or_more": calls_1800s_or_more,
            "max_connect_time_sec": float(numeric_connect_time.max()) if not numeric_connect_time.dropna().empty else None,
            "min_connect_time_sec": float(numeric_connect_time.min()) if not numeric_connect_time.dropna().empty else None,
        },
        "coverage": {
            "min_date": min_date,
            "max_date": max_date,
            "distinct_languages_observed": distinct_languages_count,
        },
        "exclusions": {
            "negative_wait_times_excluded": negative_connect_time,
            "unparseable_timestamps_excluded": invalid_timestamps,
            "null_values_excluded": int(total_records - valid_records_count - negative_connect_time - invalid_timestamps),
            "justification": "Records with null values or negative waiting times violate physical queue assumptions and are excluded from core statistical analysis. All exclusions are tracked."
        }
    }
    return report
