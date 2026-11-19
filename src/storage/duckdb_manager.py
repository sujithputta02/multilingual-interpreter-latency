"""DuckDB analytical query manager for high-performance calculations."""
from pathlib import Path
from typing import Optional
import duckdb
import pandas as pd


class DuckDBManager:
    """Manages embedded DuckDB analytical database and direct Parquet querying."""

    def __init__(self, db_path: str = "data/analytics/interpreter_analytics.duckdb"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(db_path)

    def register_parquet(self, parquet_path: str = "data/processed/interpreter_wait_times.parquet", view_name: str = "wait_times") -> None:
        """Registers a Parquet file as a virtual table in DuckDB."""
        if Path(parquet_path).exists():
            self.conn.execute(f"CREATE OR REPLACE VIEW {view_name} AS SELECT * FROM read_parquet('{parquet_path}')")

    def query(self, sql: str, params: Optional[list] = None) -> pd.DataFrame:
        """Executes SQL query and returns result as pandas DataFrame."""
        if params:
            return self.conn.execute(sql, params).fetchdf()
        return self.conn.execute(sql).fetchdf()

    def close(self):
        """Closes the DuckDB connection."""
        self.conn.close()
