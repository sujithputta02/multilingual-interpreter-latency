"""Pagination controller for complete dataset retrieval (PRD Section 11.1)."""
from typing import Any, Callable, Dict, List, Optional
import pandas as pd
from src.ingestion.api_client import NYCOpenDataClient
from src.utils.logging import setup_logger

logger = setup_logger("pagination")


def fetch_all_records(
    client: NYCOpenDataClient,
    batch_size: int = 50000,
    max_records: Optional[int] = None,
    progress_callback: Optional[Callable[[int], None]] = None
) -> List[Dict[str, Any]]:
    """
    Retrieves records across all pages until exhaustion or max_records reached.
    """
    all_records: List[Dict[str, Any]] = []
    offset = 0

    logger.info(f"Beginning dataset acquisition from {client.endpoint} (batch size: {batch_size})")

    while True:
        current_limit = batch_size
        if max_records and (offset + batch_size > max_records):
            current_limit = max_records - offset
            if current_limit <= 0:
                break

        logger.info(f"Fetching batch offset={offset}, limit={current_limit}...")
        batch = client.fetch_batch(limit=current_limit, offset=offset)

        if not batch:
            logger.info("Reached end of dataset (empty batch returned).")
            break

        all_records.extend(batch)
        count_so_far = len(all_records)
        logger.info(f"Retrieved {len(batch)} records in current batch. Total so far: {count_so_far}")

        if progress_callback:
            progress_callback(count_so_far)

        if len(batch) < current_limit:
            logger.info("Batch returned fewer records than limit. Dataset fully acquired.")
            break

        offset += len(batch)

        if max_records and count_so_far >= max_records:
            logger.info(f"Target record cap reached ({count_so_far}/{max_records}).")
            break

    logger.info(f"Completed ingestion: {len(all_records)} total records collected.")
    return all_records
