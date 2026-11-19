"""NYC Open Data API client (PRD Section 11)."""
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

from src.utils.logging import setup_logger

logger = setup_logger("api_client")

DEFAULT_API_ENDPOINT = "https://data.cityofnewyork.us/resource/dzvt-6g3v.json"
DEFAULT_METADATA_ENDPOINT = "https://data.cityofnewyork.us/api/views/dzvt-6g3v.json"


class NYCOpenDataClient:
    """Client for acquiring NYC 311 Interpreter Wait Time records via Socrata API."""

    def __init__(
        self,
        endpoint: str = DEFAULT_API_ENDPOINT,
        app_token: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
    ):
        self.endpoint = endpoint
        self.app_token = app_token
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/json",
            "User-Agent": "Beyond-The-Average-Research-Platform/1.0",
        }
        if self.app_token:
            headers["X-App-Token"] = self.app_token
        return headers

    def fetch_dataset_metadata(self) -> Dict[str, Any]:
        """Fetches published metadata from NYC Open Data view API."""
        try:
            resp = requests.get(DEFAULT_METADATA_ENDPOINT, headers=self._get_headers(), timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "rowsUpdatedAt": data.get("rowsUpdatedAt"),
                    "viewCount": data.get("viewCount"),
                    "columns": [c.get("fieldName") for c in data.get("columns", [])],
                    "metadata_retrieval_status": "success",
                }
        except Exception as e:
            logger.warning(f"Could not fetch online metadata: {e}")
        return {"metadata_retrieval_status": "failed_or_offline"}

    def fetch_batch(self, limit: int = 50000, offset: int = 0) -> List[Dict[str, Any]]:
        """Fetches a single paginated batch with retries and exponential backoff."""
        params = {
            "$limit": limit,
            "$offset": offset,
            "$order": ":id",  # Stable ordering
        }
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = requests.get(
                    self.endpoint,
                    params=params,
                    headers=self._get_headers(),
                    timeout=self.timeout
                )
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 429:
                    sleep_time = self.backoff_factor ** attempt
                    logger.warning(f"Rate limited (429). Retrying in {sleep_time:.1f}s...")
                    time.sleep(sleep_time)
                else:
                    logger.error(f"API request failed with status {resp.status_code}: {resp.text[:200]}")
            except requests.RequestException as e:
                sleep_time = self.backoff_factor ** attempt
                logger.warning(f"Network error on attempt {attempt}/{self.max_retries}: {e}. Retrying in {sleep_time:.1f}s...")
                time.sleep(sleep_time)

        raise ConnectionError(f"Failed to fetch batch at offset {offset} after {self.max_retries} attempts.")
