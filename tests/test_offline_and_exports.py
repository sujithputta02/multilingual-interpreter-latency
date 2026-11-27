"""Tests for offline fallback, PNG exports, and reproducibility metadata."""
import pandas as pd
from unittest.mock import patch

from src.ingestion.refresh import run_full_pipeline
from src.utils.exports import (
    build_analysis_metadata_bundle,
    render_language_comparison_png,
    render_monthly_trend_png,
)


def test_offline_fallback_preserves_local_cache(tmp_path):
    parquet_file = tmp_path / "cached.parquet"
    pd.DataFrame({
        "call_time": [pd.Timestamp("2024-01-01 10:00:00")],
        "language": ["Spanish"],
        "connect_time_sec": [5.0],
    }).to_parquet(parquet_file)

    with patch("src.ingestion.refresh.fetch_all_records", side_effect=ConnectionError("Network down")):
        res = run_full_pipeline(
            raw_dir=str(tmp_path / "raw"),
            processed_parquet_path=str(parquet_file),
            metadata_path=str(tmp_path / "meta.json"),
            quality_report_path=str(tmp_path / "qr.json"),
            duckdb_path=str(tmp_path / "test.duckdb"),
        )
        assert res["status"] == "success_offline"
        assert res["is_offline"] is True
        assert res["total_records"] == 1


def test_export_generators():
    df = pd.DataFrame({
        "call_time": [pd.Timestamp("2024-01-01 10:00:00"), pd.Timestamp("2024-02-01 11:00:00")],
        "language": ["Spanish", "Russian"],
        "connect_time_sec": [2.0, 120.0],
    })
    meta = build_analysis_metadata_bundle(df)
    assert meta["active_sample_count"] == 2
    assert "metric_definitions" in meta

    lang_df = pd.DataFrame({
        "language": ["Spanish", "Russian"],
        "mean": [2.0, 120.0],
        "median": [2.0, 60.0],
        "p95": [5.0, 350.0],
    })
    png1 = render_language_comparison_png(lang_df)
    assert png1.startswith(b"\x89PNG")

    monthly_df = pd.DataFrame({
        "year_month": ["2024-01", "2024-02"],
        "mean": [10.0, 15.0],
        "median": [3.0, 4.0],
        "p90": [25.0, 35.0],
    })
    png2 = render_monthly_trend_png(monthly_df)
    assert png2.startswith(b"\x89PNG")
