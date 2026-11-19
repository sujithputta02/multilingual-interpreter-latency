"""Integration tests for ingestion pipeline and local persistence."""
import pytest
from pathlib import Path
from src.storage.parquet_manager import load_processed_parquet
from src.storage.duckdb_manager import DuckDBManager
from src.utils.metadata import load_json


def test_processed_dataset_exists_and_valid():
    df = load_processed_parquet()
    assert df is not None
    assert not df.empty
    assert len(df) >= 1000
    expected_cols = [
        "call_time", "language", "connect_time_sec", "year", "month",
        "year_month", "date", "hour", "day_of_week", "time_period",
        "is_300s_or_more", "is_oti_language", "wait_category"
    ]
    for col in expected_cols:
        assert col in df.columns


def test_duckdb_integration():
    db = DuckDBManager()
    db.register_parquet()
    res = db.query("SELECT COUNT(*) as total_calls, AVG(connect_time_sec) as avg_wait FROM wait_times")
    assert not res.empty
    assert res.iloc[0]["total_calls"] >= 1000
    assert res.iloc[0]["avg_wait"] > 0
    db.close()


def test_metadata_and_quality_reports_exist():
    quality_report = load_json("data/metadata/data_quality_report.json")
    assert quality_report is not None
    assert quality_report["valid_record_count"] >= 1000
    assert "extreme_values_retained" in quality_report

    ingest_meta = load_json("data/metadata/ingestion_metadata.json")
    assert ingest_meta is not None
    assert ingest_meta["dataset_id"] == "dzvt-6g3v"
