"""Descriptive and distribution-sensitive statistics engine (PRD Section 8.3)."""
from typing import Any, Dict, Optional, Union
import numpy as np
import pandas as pd


def calculate_descriptive_stats(series: Union[pd.Series, np.ndarray]) -> Dict[str, Any]:
    """
    Computes core statistical and distribution-sensitive metrics (PRD Section 8.3):
    - Count
    - Mean
    - Median (P50)
    - Minimum & Maximum
    - Standard Deviation
    - IQR (P75 - P25)
    - P90 & P95
    - Long-wait count (>= 300s)
    - Long-wait percentage (share of calls >= 300s)
    """
    clean_series = pd.Series(series).dropna()
    n = len(clean_series)
    if n == 0:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
            "std": None,
            "iqr": None,
            "p90": None,
            "p95": None,
            "long_wait_count": 0,
            "long_wait_percentage": 0.0,
        }

    mean_val = float(clean_series.mean())
    median_val = float(clean_series.median())
    min_val = float(clean_series.min())
    max_val = float(clean_series.max())
    std_val = float(clean_series.std()) if n > 1 else 0.0

    q25 = float(clean_series.quantile(0.25))
    q75 = float(clean_series.quantile(0.75))
    iqr_val = float(q75 - q25)

    p90_val = float(clean_series.quantile(0.90))
    p95_val = float(clean_series.quantile(0.95))

    long_wait_count = int((clean_series >= 300.0).sum())
    long_wait_pct = float((long_wait_count / n) * 100.0)

    return {
        "count": n,
        "mean": round(mean_val, 2),
        "median": round(median_val, 2),
        "min": round(min_val, 2),
        "max": round(max_val, 2),
        "std": round(std_val, 2),
        "iqr": round(iqr_val, 2),
        "p90": round(p90_val, 2),
        "p95": round(p95_val, 2),
        "long_wait_count": long_wait_count,
        "long_wait_percentage": round(long_wait_pct, 2),
    }
