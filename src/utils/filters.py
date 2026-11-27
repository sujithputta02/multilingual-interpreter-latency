"""Shared persistent BI slicers, presets, and active-filter bar for all Streamlit pages."""
from typing import Tuple
import pandas as pd
import streamlit as st

from src.storage.parquet_manager import load_processed_parquet
from src.ingestion.refresh import run_full_pipeline
from src.utils.metadata import load_json

OTI_LANGUAGES = ["Spanish", "Cantonese", "Mandarin", "Russian"]


@st.cache_data(show_spinner="Connecting to analytical data warehouse...")
def load_warehouse_data() -> pd.DataFrame | None:
    """Loads processed 1.06M-row Parquet warehouse."""
    return load_processed_parquet()


def render_global_slicers() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Renders persistent BI slicers in the sidebar across every page and returns
    (full_df, filtered_df). Supports 1-click presets and reset actions.
    """
    st.sidebar.markdown("""
    <div style="padding: 6px 0 14px 0;">
        <h2 style="margin: 0; font-size: 1.3rem; font-weight: 700; color: #0f172a;">Beyond the Average</h2>
        <span style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; color: #2563eb; font-weight: 600;">Municipal Interpreter BI Suite</span>
    </div>
    """, unsafe_allow_html=True)

    meta = load_json("data/metadata/ingestion_metadata.json")
    if meta:
        retrieval_dt = meta.get("retrieval_timestamp_utc", "")[:16].replace("T", " ")
        st.sidebar.caption(f"Source: NYC 311 (`dzvt-6g3v`) · Synced `{retrieval_dt}` UTC")

    if st.sidebar.button("🔄 Sync Live Open Data", use_container_width=True, help="Refresh from NYC Open Data API"):
        with st.spinner("Syncing NYC Open Data..."):
            try:
                res = run_full_pipeline(max_records=None, force_download=True)
                st.cache_data.clear()
                st.sidebar.success(f"Synced {res['total_processed_records']:,} records!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Sync error: {e}")

    df = load_warehouse_data()
    if df is None or df.empty:
        return pd.DataFrame(), pd.DataFrame()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Global BI Slicers")

    # Quick Preset Actions
    st.sidebar.caption("Quick Presets")
    p_col1, p_col2 = st.sidebar.columns(2)
    if p_col1.button("OTI 4 Langs", use_container_width=True, help="Filter to Spanish, Cantonese, Mandarin, Russian"):
        st.session_state["slicer_langs"] = [l for l in OTI_LANGUAGES if l in df["language"].unique()]
        st.rerun()
    if p_col2.button("Reset All", use_container_width=True):
        st.session_state["slicer_year"] = "All Years"
        st.session_state["slicer_langs"] = []
        st.session_state["slicer_period"] = "All Periods"
        st.session_state["slicer_dow"] = "All Days"
        st.session_state["slicer_tier"] = "All Calls"
        st.session_state["action_month"] = None
        st.rerun()

    # Year slicer
    years = ["All Years"] + sorted(df["year"].dropna().unique().tolist())
    selected_year = st.sidebar.selectbox("Calendar Year", options=years, key="slicer_year")

    # Date range slicer
    min_date = df["call_time"].dt.date.min()
    max_date = df["call_time"].dt.date.max()
    date_range = st.sidebar.date_input(
        "Date Window",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Language multi-select
    all_languages = sorted(df["language"].dropna().unique().tolist())
    selected_languages = st.sidebar.multiselect(
        "Requested Language(s)",
        options=all_languages,
        key="slicer_langs",
        help="Leave empty to include all 112 languages.",
    )

    # Time Period slicer
    time_periods = ["All Periods"] + sorted(df["time_period"].dropna().unique().tolist())
    selected_period = st.sidebar.selectbox("Operating Window", options=time_periods, key="slicer_period")

    # Day of Week slicer
    dow_options = ["All Days", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected_dow = st.sidebar.selectbox("Day of Week", options=dow_options, key="slicer_dow")

    # Wait Tier slicer
    tier_options = ["All Calls", "Within 30s Goal (≤30s)", "Delayed (>30s)", "Statutory Review (≥300s)"]
    selected_tier = st.sidebar.selectbox("Wait Latency Tier", options=tier_options, key="slicer_tier")

    # Apply filters efficiently via boolean mask
    mask = pd.Series(True, index=df.index)
    if selected_year != "All Years":
        mask &= (df["year"] == selected_year)
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_d, end_d = date_range
        if start_d > min_date or end_d < max_date:
            dates = df["call_time"].dt.date
            mask &= (dates >= start_d) & (dates <= end_d)
    if selected_languages:
        mask &= df["language"].isin(selected_languages)
    if selected_period != "All Periods":
        mask &= (df["time_period"] == selected_period)
    if selected_dow != "All Days":
        mask &= (df["day_of_week"] == selected_dow)
    if selected_tier == "Within 30s Goal (≤30s)":
        mask &= (df["connect_time_sec"] <= 30.0)
    elif selected_tier == "Delayed (>30s)":
        mask &= (df["connect_time_sec"] > 30.0)
    elif selected_tier == "Statutory Review (≥300s)":
        mask &= (df["connect_time_sec"] >= 300.0)
    action_month = st.session_state.get("action_month")
    if action_month:
        mask &= (df["year_month"] == action_month)

    filtered_df = df[mask]

    st.session_state["raw_df"] = df
    st.session_state["filtered_df"] = filtered_df
    st.session_state["all_languages"] = all_languages

    pct_active = (len(filtered_df) / len(df)) * 100.0 if len(df) > 0 else 0.0
    st.sidebar.markdown("---")
    st.sidebar.metric("Active Slice", f"{len(filtered_df):,}", f"{pct_active:.1f}% of {len(df):,} calls")

    return df, filtered_df
