"""End-to-end dataset acquisition, refresh, and pipeline execution (PRD Section 11 & 12)."""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
import pandas as pd

from src.ingestion.api_client import NYCOpenDataClient
from src.ingestion.pagination import fetch_all_records
from src.validation.schema import validate_schema, SchemaValidationError
from src.validation.quality_checks import run_data_quality_checks
from src.processing.cleaning import clean_dataset
from src.processing.features import derive_features
from src.storage.parquet_manager import save_processed_parquet, load_processed_parquet
from src.storage.duckdb_manager import DuckDBManager
from src.utils.logging import setup_logger
from src.utils.metadata import save_json, load_json, get_environment_info

logger = setup_logger("refresh_pipeline")


def run_full_pipeline(
    max_records: Optional[int] = None,
    batch_size: int = 50000,
    force_download: bool = False,
    raw_dir: str = "data/raw",
    processed_parquet_path: str = "data/processed/interpreter_wait_times.parquet",
    metadata_path: str = "data/metadata/ingestion_metadata.json",
    quality_report_path: str = "data/metadata/data_quality_report.json",
    duckdb_path: str = "data/analytics/interpreter_analytics.duckdb",
) -> Dict[str, Any]:
    """
    Executes complete data pipeline (Phases 1-4):
    1. Acquire raw data from NYC Open Data (or load cached snapshot if offline/not forced)
    2. Preserve raw snapshot
    3. Validate schema
    4. Clean data & preserve legitimate duplicates / extremes
    5. Derive temporal and policy features
    6. Save processed dataset to Parquet
    7. Generate and save Data Quality Report
    8. Update DuckDB analytical views
    """
    logger.info("Initiating Beyond the Average data pipeline execution...")
    Path(raw_dir).mkdir(parents=True, exist_ok=True)
    Path(processed_parquet_path).parent.mkdir(parents=True, exist_ok=True)

    client = NYCOpenDataClient()
    online_metadata = client.fetch_dataset_metadata()

    # Ingest data
    records = None
    acquisition_mode = "online_api"

    try:
        raw_list = fetch_all_records(client, batch_size=batch_size, max_records=max_records)
        if not raw_list:
            raise ValueError("Zero records retrieved from API.")
        raw_df = pd.DataFrame(raw_list)

        # Preserve unmodified raw snapshot (PRD Section 11.1)
        snapshot_timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        snapshot_filename = f"raw_wait_times_{snapshot_timestamp}.parquet"
        snapshot_filepath = Path(raw_dir) / snapshot_filename
        raw_df.to_parquet(snapshot_filepath, compression="snappy")
        logger.info(f"Preserved raw snapshot at {snapshot_filepath} with {len(raw_df)} records.")

    except Exception as e:
        logger.warning(f"Could not retrieve from live API ({e}). Checking local cache for offline mode...")
        existing_df = load_processed_parquet(processed_parquet_path)
        if existing_df is not None:
            logger.info("Successfully loaded existing validated local Parquet dataset (Offline Mode).")
            return {
                "status": "success_offline",
                "message": "Operated using previously validated local dataset.",
                "total_records": len(existing_df),
                "is_offline": True,
            }
        else:
            raise ConnectionError(f"API unavailable and no local dataset found: {e}")

    # Schema Validation
    is_valid_schema, schema_errors = validate_schema(raw_df)
    if not is_valid_schema:
        err_msg = " | ".join(schema_errors)
        logger.error(f"Schema validation failed: {err_msg}")
        raise SchemaValidationError(err_msg)

    # Data Quality Audit
    quality_report = run_data_quality_checks(raw_df, online_metadata)
    save_json(quality_report, quality_report_path)
    logger.info(f"Generated data quality report at {quality_report_path}")

    # Cleaning & Normalization
    valid_df, excluded_df = clean_dataset(raw_df)
    logger.info(f"Cleaning complete: {len(valid_df)} valid records, {len(excluded_df)} excluded.")

    # Feature Engineering
    features_df = derive_features(valid_df)
    logger.info(f"Derived analytical features for {len(features_df)} records.")

    # Parquet Storage
    save_processed_parquet(features_df, processed_parquet_path)
    logger.info(f"Stored processed Parquet dataset at {processed_parquet_path}")

    # Ingestion Metadata
    ingestion_metadata = {
        "dataset_name": "NYC 311 Interpreter Wait Time",
        "dataset_id": "dzvt-6g3v",
        "retrieval_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total_raw_records": len(raw_df),
        "total_processed_records": len(features_df),
        "excluded_records": len(excluded_df),
        "raw_snapshot_path": str(snapshot_filepath),
        "processed_parquet_path": processed_parquet_path,
        "online_metadata": online_metadata,
        "environment": get_environment_info(),
    }
    save_json(ingestion_metadata, metadata_path)
    logger.info(f"Saved ingestion metadata at {metadata_path}")

    # DuckDB registration
    try:
        db = DuckDBManager(duckdb_path)
        db.register_parquet(processed_parquet_path)
        db.close()
        logger.info(f"Registered Parquet dataset with DuckDB at {duckdb_path}")
    except Exception as e:
        logger.warning(f"DuckDB registration note: {e}")

    return {
        "status": "success",
        "total_raw_records": len(raw_df),
        "total_processed_records": len(features_df),
        "excluded_records": len(excluded_df),
        "date_range": [quality_report["coverage"]["min_date"], quality_report["coverage"]["max_date"]],
        "distinct_languages": quality_report["coverage"]["distinct_languages_observed"],
    }
