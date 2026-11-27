"""Reproducibility metadata and publication-ready PNG/CSV export helpers (PRD Section 14, 15.2, 16.3)."""
import io
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.utils.metadata import get_environment_info


def build_analysis_metadata_bundle(
    df: pd.DataFrame,
    date_range: Optional[tuple] = None,
    selected_languages: Optional[List[str]] = None,
    selected_period: str = "All Periods",
    selected_dow: str = "All Days",
) -> Dict[str, Any]:
    """Builds a reproducible JSON metadata bundle describing active filters and definitions."""
    min_dt = df["call_time"].min().isoformat() if not df.empty else None
    max_dt = df["call_time"].max().isoformat() if not df.empty else None

    return {
        "export_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_source": "NYC Open Data - 311 Interpreter Wait Time (dzvt-6g3v)",
        "active_sample_count": int(len(df)),
        "observed_date_range": {"min": min_dt, "max": max_dt},
        "active_filters": {
            "date_range": [str(d) for d in date_range] if date_range else None,
            "selected_languages": selected_languages or "All",
            "time_period": selected_period,
            "day_of_week": selected_dow,
        },
        "metric_definitions": {
            "mean": "Arithmetic average waiting time in seconds",
            "median": "50th percentile (P50) waiting time in seconds",
            "p90": "90th percentile waiting time in seconds",
            "p95": "95th percentile waiting time in seconds",
            "oti_30s_goal": "NYC OTI 2024 Language Access Plan target <= 30.0s mean for Spanish, Cantonese, Mandarin, Russian",
            "statutory_300s_threshold": "NYC Administrative Code §23-310 review trigger for calls >= 300.0s",
        },
        "environment": get_environment_info(),
    }


def render_language_comparison_png(lang_df: pd.DataFrame, top_n: int = 10, title_suffix: str = "") -> bytes:
    """Renders a publication-ready PNG chart comparing Mean, Median, and P95 across top languages."""
    sub = lang_df.head(top_n).copy()
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)

    x = range(len(sub))
    width = 0.27
    ax.bar([i - width for i in x], sub["mean"], width=width, label="Mean (s)", color="#2563eb")
    ax.bar(x, sub["median"], width=width, label="Median (P50, s)", color="#10b981")
    ax.bar([i + width for i in x], sub["p95"], width=width, label="95th Percentile (P95, s)", color="#ef4444")

    ax.axhline(30.0, color="#059669", linestyle="--", linewidth=1.2, label="OTI 30s Avg Goal")
    ax.axhline(300.0, color="#b91c1c", linestyle=":", linewidth=1.4, label="§23-310 300s Threshold")

    ax.set_xticks(list(x))
    ax.set_xticklabels(sub["language"], rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("Waiting Time (Seconds)")
    ax.set_title(f"Interpreter Waiting Times: Mean vs. Median vs. P95{title_suffix}", fontsize=12, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(loc="upper right", fontsize=8)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def render_monthly_trend_png(monthly_df: pd.DataFrame) -> bytes:
    """Renders a publication-ready PNG chart of monthly waiting-time trajectories."""
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=200)

    ax.plot(monthly_df["year_month"], monthly_df["mean"], marker="o", linewidth=2, label="Mean (s)", color="#2563eb")
    ax.plot(monthly_df["year_month"], monthly_df["median"], marker="s", linestyle="--", linewidth=1.8, label="Median (s)", color="#10b981")
    ax.plot(monthly_df["year_month"], monthly_df["p90"], marker="^", linestyle=":", linewidth=1.8, label="P90 (s)", color="#f59e0b")
    ax.axhline(30.0, color="#ef4444", linestyle="--", linewidth=1.2, label="OTI 30s Goal")

    # Thin x-ticks if many months
    step = max(1, len(monthly_df) // 12)
    ax.set_xticks(range(0, len(monthly_df), step))
    ax.set_xticklabels(monthly_df["year_month"].iloc[::step], rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("Waiting Time (Seconds)")
    ax.set_title("Monthly Interpreter Waiting-Time Trajectory", fontsize=12, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(loc="upper right", fontsize=8)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()
