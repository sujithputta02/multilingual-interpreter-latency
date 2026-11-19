"""Beyond the Average: Main Streamlit Research Application."""
import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

from src.storage.parquet_manager import load_processed_parquet
from src.ingestion.refresh import run_full_pipeline
from src.utils.metadata import load_json
from src.analytics.descriptive import calculate_descriptive_stats

# Page config
st.set_page_config(
    page_title="Beyond the Average | NYC 311 Interpreter Wait Times",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner="Loading analytical dataset...")
def get_cached_dataset():
    """Loads processed dataset from local Parquet storage."""
    parquet_path = "data/processed/interpreter_wait_times.parquet"
    if not Path(parquet_path).exists():
        return None
    return load_processed_parquet(parquet_path)


def main():
    st.sidebar.title("Beyond the Average")
    st.sidebar.caption("Policy-Aware, Distribution-Sensitive Research Platform")

    # Ingestion / Refresh Control
    metadata_path = "data/metadata/ingestion_metadata.json"
    meta = load_json(metadata_path)
    if meta:
        st.sidebar.markdown(f"**Dataset:** NYC Open Data (`dzvt-6g3v`)")
        st.sidebar.markdown(f"**Records:** {meta.get('total_processed_records', 'N/A'):,}")
        retrieval_dt = meta.get('retrieval_timestamp_utc', '')[:16].replace("T", " ")
        st.sidebar.markdown(f"**Refreshed (UTC):** `{retrieval_dt}`")
    else:
        st.sidebar.warning("No local dataset found. Ingestion required.")

    if st.sidebar.button("🔄 Refresh Dataset", help="Acquire latest records from NYC Open Data"):
        with st.spinner("Executing pipeline and acquiring data..."):
            try:
                res = run_full_pipeline(max_records=50000, force_download=True)
                st.cache_data.clear()
                st.sidebar.success(f"Acquired {res['total_processed_records']:,} records!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Refresh failed: {e}")

    df = get_cached_dataset()

    if df is None or df.empty:
        st.title("Beyond the Average: Research Platform")
        st.info("The local analytical dataset has not been initialized yet.")
        if st.button("Initialize Pipeline & Download Initial Research Data"):
            with st.spinner("Downloading NYC 311 Interpreter Wait Time records..."):
                try:
                    res = run_full_pipeline(max_records=50000)
                    st.cache_data.clear()
                    st.success("Dataset successfully acquired and processed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Initialization error: {e}")
        return

    # Global Filters (PRD Section 14)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Global Research Filters")

    # Date filter
    min_date = df["call_time"].dt.date.min()
    max_date = df["call_time"].dt.date.max()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter calls by connection timestamp."
    )

    # Language multi-select
    all_languages = sorted(df["language"].dropna().unique().tolist())
    selected_languages = st.sidebar.multiselect(
        "Filter Languages (Leave empty for all)",
        options=all_languages,
        default=[],
        help="Select one or more languages. Unselected includes all observed languages."
    )

    # Time of Day filter
    time_periods = ["All Periods"] + sorted(df["time_period"].dropna().unique().tolist())
    selected_period = st.sidebar.selectbox("Time Period", options=time_periods)

    # Day of Week filter
    dow_options = ["All Days", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected_dow = st.sidebar.selectbox("Day of Week", options=dow_options)

    # Apply Filters
    filtered_df = df.copy()

    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_d, end_d = date_range
        filtered_df = filtered_df[
            (filtered_df["call_time"].dt.date >= start_d) &
            (filtered_df["call_time"].dt.date <= end_d)
        ]

    if selected_languages:
        filtered_df = filtered_df[filtered_df["language"].isin(selected_languages)]

    if selected_period != "All Periods":
        filtered_df = filtered_df[filtered_df["time_period"] == selected_period]

    if selected_dow != "All Days":
        filtered_df = filtered_df[filtered_df["day_of_week"] == selected_dow]

    # Store filtered dataset in session state for pages
    st.session_state["raw_df"] = df
    st.session_state["filtered_df"] = filtered_df
    st.session_state["all_languages"] = all_languages

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Active Sample:** `{len(filtered_df):,}` / `{len(df):,}` calls")
    if st.sidebar.button("Reset Filters"):
        st.rerun()

    # Default Landing Screen
    st.title("Beyond the Average")
    st.markdown("### A Policy-Aware, Distribution-Sensitive Analysis of Multilingual Public-Service Interpreter Waiting Times")
    st.markdown("""
    This research platform investigates interpreter connection waiting times in municipal public services
    using the **New York City 311 Interpreter Wait Time** dataset (`dzvt-6g3v`).

    Use the sidebar to navigate between research modules:
    1. **Overview:** Executive descriptive statistics and monthly distribution trends.
    2. **Language Analysis:** Granular language-wise waiting time comparisons and inferential tests.
    3. **Temporal Analysis:** Diurnal (hourly), weekly, and heat-mapped temporal dynamics.
    4. **Distribution & Policy:** Mean-vs-Median disparity and statutory benchmarks (§23-310 and OTI 30s Goal).
    5. **Data Quality & Methodology:** Reproducibility reports, IEEE literature review audit, and statutory definitions.
    """)

    # Quick Summary Cards
    stats = calculate_descriptive_stats(filtered_df["connect_time_sec"])
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Observed Calls", f"{stats['count']:,}")
    c2.metric("Mean Wait Time", f"{stats['mean']}s")
    c3.metric("Median (P50)", f"{stats['median']}s")
    c4.metric("Tail (P95)", f"{stats['p95']}s")
    c5.metric("Calls >= 300s", f"{stats['long_wait_count']:,} ({stats['long_wait_percentage']}%)")

    st.info("💡 **Methodological Note:** Notice the divergence between the Mean and Median. When distributions are heavily right-skewed, relying on average-only reporting masks prolonged delays experienced in upper percentiles.")


if __name__ == "__main__":
    main()
