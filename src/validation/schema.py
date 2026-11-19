"""Schema validation for NYC 311 Interpreter Wait Time records."""
from typing import Any, Dict, List, Tuple
import pandas as pd

REQUIRED_COLUMNS = ["call_time", "language", "connect_time_sec"]


class SchemaValidationError(Exception):
    """Raised when incoming dataset does not match official NYC Open Data schema."""
    pass


def validate_schema(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validates that DataFrame satisfies NYC 311 Interpreter Wait Time schema (PRD Section 12.1).
    Returns (is_valid, error_messages).
    """
    errors = []

    if df is None or not isinstance(df, pd.DataFrame):
        return False, ["Input is not a valid pandas DataFrame."]

    if df.empty:
        return False, ["Dataset is empty (zero rows)."]

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required schema columns: {missing_cols}. Expected: {REQUIRED_COLUMNS}")

    return len(errors) == 0, errors


def assert_valid_schema(df: pd.DataFrame) -> None:
    """Raises SchemaValidationError if schema validation fails."""
    is_valid, errors = validate_schema(df)
    if not is_valid:
        raise SchemaValidationError(" | ".join(errors))
