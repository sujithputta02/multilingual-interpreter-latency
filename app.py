"""Beyond the Average: Main Streamlit Research Application & BI Dashboard."""
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
from src.utils.ui import apply_bi_theme, render_kpi, render_banner

# Page configuration
st.set_page_config(
    page_title="Beyond the Average | BI Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_bi_theme()


@st.cache_data(show_spinner="Connecting to analytical data warehouse...")
def get_cached_dataset():
    """Loads processed dataset from local Parquet storage."""
    parquet_path = "data/processed/interpreter_wait_times.parquet"
    if not Path(parquet_path).exists():
        return None
    return load_processed_parquet(parquet_path)


def main():
    # Sidebar BI Branding
    st.sidebar.markdown("""
    <div style="padding: 10px 0 20px 0;">
        <h2 style="margin: 0; font-size: 1.4rem; font-weight: 700; color: #1e293b;">Beyond the Average</h2>
        <span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #3b82f6; font-weight: 600;">Executive Research & BI Platform</span>
    </div>
    """, unsafe_allow_html=True)

    # Ingestion / Warehouse Status
    metadata_path = "data/metadata/ingestion_metadata.json"
    meta = load_json(metadata_path)
    if meta:
        st.sidebar.markdown(f"**Source Feed:** NYC Open Data (`dzvt-6g3v`)")
        st.sidebar.markdown(f"**Loaded Records:** `{meta.get('total_processed_records', 0):,}`")
        retrieval_dt = meta.get('retrieval_timestamp_utc', '')[:16].replace("T", " ")
        st.sidebar.markdown(f"**Last Sync (UTC):** `{retrieval_dt}`")
    else:
        st.sidebar.warning("No local warehouse found. Initialization required.")

    if st.sidebar.button("🔄 Sync Live Open Data Feed", help="Fetch latest records from NYC Open Data API"):
        with st.spinner("Executing ETL ingestion pipeline..."):
            try:
                res = run_full_pipeline(max_records=50000, force_download=True)
                st.cache_data.clear()
                st.sidebar.success(f"Synced {res['total_processed_records']:,} records!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Sync error: {e}")

    df = get_cached_dataset()

    if df is None or df.empty:
        render_banner("Beyond the Average", "Research & BI Platform for Municipal Multilingual Services")
        st.info("The local analytical data warehouse has not been initialized.")
        if st.button("Initialize Analytical Pipeline (50,000 Records)"):
            with st.spinner("Acquiring and engineering NYC 311 Interpreter records..."):
                try:
                    res = run_full_pipeline(max_records=50000)
                    st.cache_data.clear()
                    st.success("Warehouse initialized successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Initialization error: {e}")
        return

    # Global BI Slicers & Filters (PRD Section 14)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Global Slicers & Filters")

    # Date slicer
    min_date = df["call_time"].dt.date.min()
    max_date = df["call_time"].dt.date.max()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter calls by connection timestamp."
    )

    # Language slicer
    all_languages = sorted(df["language"].dropna().unique().tolist())
    selected_languages = st.sidebar.multiselect(
        "Requested Language(s)",
        options=all_languages,
        default=[],
        help="Filter by specific language cohorts. Defaults to all observed languages."
    )

    # Time of Day slicer
    time_periods = ["All Periods"] + sorted(df["time_period"].dropna().unique().tolist())
    selected_period = st.sidebar.selectbox("Operating Window", options=time_periods)

    # Day of Week slicer
    dow_options = ["All Days", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected_dow = st.sidebar.selectbox("Day of Week", options=dow_options)

    # Apply Filters to dataset
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

    # Save filtered slice in session state
    st.session_state["raw_df"] = df
    st.session_state["filtered_df"] = filtered_df
    st.session_state["all_languages"] = all_languages

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Active Slice:** `{len(filtered_df):,}` / `{len(df):,}` calls ({len(filtered_df)/len(df)*100:.1f}%)")
    if st.sidebar.button("Reset Slicers"):
        st.rerun()

    # Check for empty filter slice
    if filtered_df.empty:
        render_banner(
            "Beyond the Average: Municipal Interpreter BI Platform",
            "A Policy-Aware, Distribution-Sensitive Analysis of NYC 311 Multilingual Public-Service Waiting Times",
            badge="0 Calls Matching Filter"
        )
        st.warning("⚠️ No call records match the current slicer filter selection. Please expand your date range or reset language filters in the sidebar.")
        return

    # Executive Banner
    render_banner(
        "Beyond the Average: Municipal Interpreter BI Platform",
        "A Policy-Aware, Distribution-Sensitive Analysis of NYC 311 Multilingual Public-Service Waiting Times",
        badge=f"{len(filtered_df):,} Calls Loaded"
    )

    # Executive BI KPI Grid
    stats = calculate_descriptive_stats(filtered_df["connect_time_sec"])
    k1, k2, k3, k4, k5 = st.columns(5)

    mean_v = stats.get("mean")
    median_v = stats.get("median")
    p95_v = stats.get("p95")

    div_subtext = f"Divergence: +{mean_v - median_v:.1f}s" if (mean_v is not None and median_v is not None) else "No data"
    tail_subtext = f"{p95_v / max(1.0, median_v):.1f}x Median" if (p95_v is not None and median_v is not None) else "No data"

    with k1:
        render_kpi("Connected Calls", f"{stats['count']:,}", "100% of recorded cohort", "NYC 311", "info")
    with k2:
        render_kpi("Mean Wait Time", f"{mean_v}s" if mean_v is not None else "N/A", "Arithmetic Average", "Aggregate", "info")
    with k3:
        render_kpi("Median Wait (P50)", f"{median_v}s" if median_v is not None else "N/A", div_subtext, "Midpoint", "success")
    with k4:
        render_kpi("Tail Delay (P95)", f"{p95_v}s" if p95_v is not None else "N/A", tail_subtext, "Severe Tail", "danger")
    with k5:
        render_kpi("Calls ≥ 300s", f"{stats['long_wait_count']:,}", f"{stats['long_wait_percentage']}% of calls", "§23-310 Review", "danger" if stats['long_wait_percentage'] > 1.0 else "info")

    if mean_v is not None and median_v is not None and p95_v is not None:
        st.markdown(f"""
        <div class="bi-callout">
            <strong>Executive Analytical Finding:</strong> Relying solely on arithmetic mean waiting times conceals severe tail latency. While the typical caller connects in <strong>{median_v}s</strong> (median), upper-tail callers face delays of <strong>{p95_v}s</strong> (P95), with <strong>{stats['long_wait_count']:,} callers ({stats['long_wait_percentage']:.2f}%)</strong> crossing the statutory review threshold under NYC Administrative Code §23-310.
        </div>
        """, unsafe_allow_html=True)

    # BI Module Navigation Grid
    st.markdown("### 🧭 Executive BI Portals")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="bi-panel">
            <h4 style="margin: 0 0 8px 0; color: #1e293b;">📈 1. Executive Overview</h4>
            <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 12px;">High-level monthly trajectories, wait-time category distributions, and top requested language volume comparisons.</p>
            <span class="bi-badge-info">Page 1 in Sidebar</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="bi-panel">
            <h4 style="margin: 0 0 8px 0; color: #1e293b;">⚖️ 4. Distribution & Policy Scorecard</h4>
            <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 12px;">Mean vs. Median disparity, ECDF curves, OTI 30s Goal compliance, and §23-310 statutory review monitoring.</p>
            <span class="bi-badge-info">Page 4 in Sidebar</span>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="bi-panel">
            <h4 style="margin: 0 0 8px 0; color: #1e293b;">🌐 2. Language Cohort Analysis</h4>
            <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 12px;">Granular language comparisons, distribution boxplots, and non-parametric Kruskal-Wallis & Mann-Whitney inferential tests.</p>
            <span class="bi-badge-info">Page 2 in Sidebar</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="bi-panel">
            <h4 style="margin: 0 0 8px 0; color: #1e293b;">🛡️ 5. Data Governance & Audits</h4>
            <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 12px;">Data quality reports, IEEE literature review audit matrix, statutory definitions, and CSV/JSON export tools.</p>
            <span class="bi-badge-info">Page 5 in Sidebar</span>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="bi-panel">
            <h4 style="margin: 0 0 8px 0; color: #1e293b;">⏰ 3. Temporal Dynamics & Heatmaps</h4>
            <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 12px;">Diurnal 24-hour trends, day-of-week demand profiles, and interactive 2D Hour × Day-of-Week delay matrices.</p>
            <span class="bi-badge-info">Page 3 in Sidebar</span>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
