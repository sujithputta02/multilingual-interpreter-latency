"""Feature engineering and analytical derivations (PRD Section 12.4)."""
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np


def assign_time_period(hour: int, time_periods_cfg: Optional[Dict[str, Any]] = None) -> str:
    """Categorizes hour into project-defined time period."""
    if time_periods_cfg and "categories" in time_periods_cfg:
        for cat in time_periods_cfg["categories"]:
            if cat["start_hour"] <= hour < cat["end_hour"]:
                return cat["name"]
    # Default fallback boundaries
    if 0 <= hour < 6:
        return "Night"
    elif 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"


def assign_wait_category(seconds: float) -> str:
    """Binned category for waiting-time distribution analysis."""
    if seconds <= 30.0:
        return "0-30s (Within Goal)"
    elif seconds <= 60.0:
        return "31-60s"
    elif seconds <= 120.0:
        return "61-120s"
    elif seconds < 300.0:
        return "121-299s"
    else:
        return ">=300s (Statutory Review)"


def derive_features(df: pd.DataFrame, time_periods_cfg: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Derives all analytical features from cleaned DataFrame.
    """
    out = df.copy()

    # Temporal feature extraction
    ts = pd.to_datetime(out["call_time"])
    out["year"] = ts.dt.year.astype("int32")
    out["month"] = ts.dt.month.astype("int32")
    out["year_month"] = ts.dt.strftime("%Y-%m")
    out["date"] = ts.dt.date
    out["hour"] = ts.dt.hour.astype("int32")
    out["day_of_week"] = ts.dt.day_name()
    out["day_of_week_num"] = ts.dt.day_of_week.astype("int32")
    out["week_of_year"] = ts.dt.isocalendar().week.astype("int32")

    # Time period classification
    out["time_period"] = out["hour"].apply(lambda h: assign_time_period(h, time_periods_cfg))

    # Policy flags and thresholds
    out["is_300s_or_more"] = (out["connect_time_sec"] >= 300.0).astype(bool)
    out["wait_category"] = out["connect_time_sec"].apply(assign_wait_category)

    # NYC OTI 4-Language Policy benchmark flag
    oti_languages = {"Spanish", "Cantonese", "Mandarin", "Russian"}
    out["is_oti_language"] = out["language"].isin(oti_languages).astype(bool)

    return out
