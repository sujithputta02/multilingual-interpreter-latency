"""Page 1: Research Overview (PRD Section 13.1)."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.analytics.descriptive import calculate_descriptive_stats
from src.analytics.temporal_analysis import compute_monthly_trend
from src.analytics.language_analysis import compute_language_summary
from src.storage.parquet_manager import load_processed_parquet

st.set_page_config(page_title="Overview | Beyond the Average", layout="wide")

df = st.session_state.get("filtered_df")
if df is None:
    raw = load_processed_parquet()
    if raw is not None:
        df = raw
    else:
        st.warning("Dataset not loaded. Please return to the Home page to load data.")
        st.stop()

st.title("1. Research Overview")
st.markdown("### Executive Summary of Observed Interpreter Connection Delays")

# Key Descriptive Statistics
stats = calculate_descriptive_stats(df["connect_time_sec"])
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
kpi1.metric("Total Connected Calls", f"{stats['count']:,}")
kpi2.metric("Mean Wait Time", f"{stats['mean']}s")
kpi3.metric("Median Wait Time", f"{stats['median']}s")
kpi4.metric("90th Percentile (P90)", f"{stats['p90']}s")
kpi5.metric("95th Percentile (P95)", f"{stats['p95']}s")
kpi6.metric("Calls >= 300s (§23-310)", f"{stats['long_wait_count']:,} ({stats['long_wait_percentage']}%)")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Monthly Waiting-Time Trajectory")
    monthly_df = compute_monthly_trend(df)
    if not monthly_df.empty:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=monthly_df["year_month"], y=monthly_df["mean"], mode="lines+markers", name="Mean Wait (s)", line=dict(color="#1f77b4", width=2)))
        fig_trend.add_trace(go.Scatter(x=monthly_df["year_month"], y=monthly_df["median"], mode="lines+markers", name="Median Wait (s)", line=dict(color="#2ca02c", dash="dash")))
        fig_trend.add_trace(go.Scatter(x=monthly_df["year_month"], y=monthly_df["p90"], mode="lines+markers", name="P90 Wait (s)", line=dict(color="#ff7f0e", dash="dot")))
        fig_trend.add_hline(y=30.0, line_dash="dash", line_color="gray", annotation_text="OTI 30s Goal", annotation_position="bottom right")
        fig_trend.update_layout(xaxis_title="Month", yaxis_title="Waiting Time (Seconds)", hovermode="x unified", legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Insufficient monthly data.")

with col_right:
    st.subheader("Wait Time Classification Distribution")
    cat_counts = df["wait_category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Calls"]
    fig_cat = px.pie(cat_counts, names="Category", values="Calls", hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
    fig_cat.update_layout(legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_cat, use_container_width=True)

st.markdown("---")

st.subheader("Highest Volume Requested Languages: Mean vs. P95 Divergence")
lang_sum = compute_language_summary(df, min_sample_size=50, sort_by="count", ascending=False).head(10)

if not lang_sum.empty:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["mean"], name="Mean Wait Time", marker_color="#4575b4"))
    fig_bar.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["median"], name="Median (P50)", marker_color="#91bfdb"))
    fig_bar.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["p95"], name="Tail Wait Time (P95)", marker_color="#d73027"))
    fig_bar.update_layout(barmode="group", xaxis_title="Requested Language", yaxis_title="Seconds", legend=dict(orientation="h", y=1.1, x=0))
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### Top Requested Languages Breakdown Table")
    st.dataframe(lang_sum[["language", "count", "mean", "median", "p90", "p95", "std", "calls_ge_300s", "pct_ge_300s"]].rename(columns={
        "language": "Language", "count": "Calls", "mean": "Mean (s)", "median": "Median (s)", "p90": "P90 (s)", "p95": "P95 (s)", "std": "Std Dev", "calls_ge_300s": "Calls >= 300s", "pct_ge_300s": "Share >= 300s (%)"
    }), use_container_width=True)
