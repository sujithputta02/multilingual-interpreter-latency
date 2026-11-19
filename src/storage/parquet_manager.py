"""Parquet storage manager for processed dataset (PRD Section 10.2 & 16.1)."""
from pathlib import Path
from typing import Optional
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def save_processed_parquet(df: pd.DataFrame, file_path: str = "data/processed/interpreter_wait_times.parquet") -> None:
    """Saves DataFrame to Parquet with optimal compression and directory creation."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, str(path), compression="snappy")


def load_processed_parquet(file_path: str = "data/processed/interpreter_wait_times.parquet") -> Optional[pd.DataFrame]:
    """Loads processed DataFrame from Parquet if file exists."""
    path = Path(file_path)
    if not path.exists():
        return None
    return pd.read_parquet(str(path))
