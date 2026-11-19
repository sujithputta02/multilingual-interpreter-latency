"""Page 1: Executive Overview & BI Summary (PRD Section 13.1)."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.analytics.descriptive import calculate_descriptive_stats
from src.analytics.temporal_analysis import compute_monthly_trend
from src.analytics.language_analysis import compute_language_summary
from src.storage.parquet_manager import load_processed_parquet
from src.utils.ui import apply_bi_theme, render_kpi, render_banner

st.set_page_config(page_title="Executive Overview | Beyond the Average", layout="wide")
apply_bi_theme()

df = st.session_state.get("filtered_df")
if df is None:
    raw = load_processed_parquet()
    if raw is not None:
        df = raw
    else:
        st.warning("Data warehouse not loaded. Please return to the Home page.")
        st.stop()

render_banner(
    "1. Executive Research Overview",
    "Comprehensive Performance Scorecard of Observed Multilingual Public-Service Interpreter Connection Waiting Times",
    badge="Executive BI View"
)

# Executive KPI Grid
stats = calculate_descriptive_stats(df["connect_time_sec"])
k1, k2, k3, k4, k5, k6 = st.columns(6)

mean_v = stats.get("mean")
median_v = stats.get("median")
p90_v = stats.get("p90")
p95_v = stats.get("p95")

div_subtext = f"Divergence: {mean_v - median_v:.1f}s" if (mean_v is not None and median_v is not None) else "No data"

with k1:
    render_kpi("Connected Calls", f"{stats['count']:,}", "Active Cohort", "Total", "info")
with k2:
    render_kpi("Mean Wait Time", f"{mean_v}s" if mean_v is not None else "N/A", "Arithmetic Average", "Mean", "info")
with k3:
    render_kpi("Median Wait (P50)", f"{median_v}s" if median_v is not None else "N/A", div_subtext, "Midpoint", "success")
with k4:
    render_kpi("90th Percentile (P90)", f"{p90_v}s" if p90_v is not None else "N/A", "Upper 10% Wait", "P90", "info")
with k5:
    render_kpi("95th Percentile (P95)", f"{p95_v}s" if p95_v is not None else "N/A", "Upper 5% Wait", "Tail", "danger")
with k6:
    render_kpi("Calls ≥ 300s", f"{stats['long_wait_count']:,}", f"{stats['long_wait_percentage']}% of calls", "§23-310 Trigger", "danger" if stats['long_wait_percentage'] > 1.0 else "info")

st.markdown("---")

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("Monthly Waiting-Time Trajectory")
    st.caption("Tracking Mean, Median, and P90 tail latency across months against the NYC OTI 30-Second Target.")
    monthly_df = compute_monthly_trend(df)
    if not monthly_df.empty:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_df["year_month"], y=monthly_df["mean"], mode="lines+markers",
            name="Mean Wait (s)", line=dict(color="#2563eb", width=3)
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_df["year_month"], y=monthly_df["median"], mode="lines+markers",
            name="Median Wait (s)", line=dict(color="#10b981", width=2, dash="dash")
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_df["year_month"], y=monthly_df["p90"], mode="lines+markers",
            name="P90 Tail Wait (s)", line=dict(color="#f59e0b", width=2, dash="dot")
        ))
        fig_trend.add_hline(
            y=30.0, line_dash="dash", line_color="#ef4444",
            annotation_text="NYC OTI 30s Target", annotation_position="bottom right"
        )
        fig_trend.update_layout(
            template="plotly_white",
            xaxis_title="Calendar Month",
            yaxis_title="Waiting Time (Seconds)",
            hovermode="x unified",
            legend=dict(orientation="h", y=1.12, x=0),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Insufficient longitudinal data for monthly trend.")

with col_right:
    st.subheader("Wait-Time Tier Distribution")
    st.caption("Proportion of calls categorized by connection duration tiers.")
    cat_counts = df["wait_category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Calls"]
    color_map = {
        "0-30s (Within Goal)": "#10b981",
        "31-60s": "#3b82f6",
        "61-120s": "#f59e0b",
        "121-299s": "#f97316",
        ">=300s (Statutory Review)": "#ef4444"
    }
    colors = [color_map.get(c, "#94a3b8") for c in cat_counts["Category"]]

    fig_cat = px.pie(
        cat_counts, names="Category", values="Calls", hole=0.55,
        color="Category", color_discrete_map=color_map
    )
    fig_cat.update_traces(textposition="inside", textinfo="percent+label")
    fig_cat.update_layout(
        template="plotly_white",
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_cat, use_container_width=True)

st.markdown("---")

st.subheader("Top Requested Languages: Mean vs. P95 Disparity")
st.caption("Visualizing the spread between arithmetic average and severe 95th percentile delays across high-volume languages.")
lang_sum = compute_language_summary(df, min_sample_size=50, sort_by="count", ascending=False).head(10)

if not lang_sum.empty:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["mean"], name="Mean Wait Time", marker_color="#3b82f6"))
    fig_bar.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["median"], name="Median (P50)", marker_color="#10b981"))
    fig_bar.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["p95"], name="Tail Latency (P95)", marker_color="#ef4444"))
    fig_bar.update_layout(
        template="plotly_white",
        barmode="group",
        xaxis_title="Requested Language",
        yaxis_title="Waiting Time (Seconds)",
        legend=dict(orientation="h", y=1.12, x=0),
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### High-Volume Language Breakdown")
    display_tbl = lang_sum[[
        "language", "count", "mean", "median", "p90", "p95", "std", "calls_ge_300s", "pct_ge_300s"
    ]].rename(columns={
        "language": "Language",
        "count": "Total Calls",
        "mean": "Mean (s)",
        "median": "Median (s)",
        "p90": "P90 (s)",
        "p95": "P95 (s)",
        "std": "Std Dev (s)",
        "calls_ge_300s": "Calls ≥ 300s",
        "pct_ge_300s": "Review Rate (%)"
    })
    st.dataframe(display_tbl, use_container_width=True)
