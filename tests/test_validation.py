"""Unit tests for schema and data validation."""
import pytest
import pandas as pd
from src.validation.schema import validate_schema, SchemaValidationError, assert_valid_schema


def test_validate_schema_success():
    df = pd.DataFrame({
        "call_time": ["2024-01-01T12:00:00.000"],
        "language": ["Spanish"],
        "connect_time_sec": [25.0]
    })
    is_valid, errors = validate_schema(df)
    assert is_valid is True
    assert len(errors) == 0


def test_validate_schema_missing_column():
    df = pd.DataFrame({
        "call_time": ["2024-01-01T12:00:00.000"],
        "language": ["Spanish"]
        # connect_time_sec missing
    })
    is_valid, errors = validate_schema(df)
    assert is_valid is False
    assert any("connect_time_sec" in err for err in errors)


def test_validate_schema_empty():
    df = pd.DataFrame()
    is_valid, errors = validate_schema(df)
    assert is_valid is False


def test_assert_valid_schema_raises():
    df = pd.DataFrame({"wrong_col": [1, 2, 3]})
    with pytest.raises(SchemaValidationError):
        assert_valid_schema(df)
