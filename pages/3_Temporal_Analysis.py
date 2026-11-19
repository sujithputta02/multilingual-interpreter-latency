"""Page 3: Temporal Dynamics & Heatmaps (PRD Section 13.3)."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.analytics.temporal_analysis import (
    compute_hourly_summary,
    compute_day_of_week_summary,
    compute_hour_weekday_heatmap_matrix,
)
from src.storage.parquet_manager import load_processed_parquet
from src.utils.ui import apply_bi_theme, render_kpi, render_banner

st.set_page_config(page_title="Temporal Analysis | Beyond the Average", layout="wide")
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
    "3. Temporal Latency Dynamics",
    "Investigating Diurnal, Day-of-Week, and Operational Period Variations in Interpreter Wait Times",
    badge="Temporal Slicing"
)

tab1, tab2, tab3 = st.tabs(["🕒 Diurnal (Hourly) Trends", "📅 Day-of-Week Patterns", "🔥 Hour × Weekday Heatmap Matrix"])

with tab1:
    st.subheader("Diurnal Waiting Time Curve (00:00 - 23:00)")
    st.caption("Tracking how connection waiting times and tail percentiles vary by hour of the day.")
    hourly_df = compute_hourly_summary(df)

    if not hourly_df.empty:
        fig_hour = go.Figure()
        fig_hour.add_trace(go.Scatter(
            x=hourly_df["hour"], y=hourly_df["mean"], mode="lines+markers",
            name="Mean Wait (s)", line=dict(color="#2563eb", width=3)
        ))
        fig_hour.add_trace(go.Scatter(
            x=hourly_df["hour"], y=hourly_df["median"], mode="lines+markers",
            name="Median Wait (s)", line=dict(color="#10b981", width=2, dash="dash")
        ))
        fig_hour.add_trace(go.Scatter(
            x=hourly_df["hour"], y=hourly_df["p90"], mode="lines+markers",
            name="P90 Tail Delay (s)", line=dict(color="#f59e0b", width=2, dash="dot")
        ))
        fig_hour.add_hline(
            y=30.0, line_dash="dash", line_color="#ef4444",
            annotation_text="NYC OTI 30s Target", annotation_position="top right"
        )
        fig_hour.update_layout(
            template="plotly_white",
            xaxis=dict(tickmode="linear", tick0=0, dtick=1, title="Hour of Day (24-Hour Military Time)"),
            yaxis_title="Waiting Time (Seconds)",
            hovermode="x unified",
            legend=dict(orientation="h", y=1.12, x=0),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_hour, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### Hourly Call Volume (Sample Count)")
            fig_vol = px.bar(
                hourly_df, x="hour", y="count",
                labels={"hour": "Hour of Day", "count": "Connected Calls"},
                color_discrete_sequence=["#93c5fd"]
            )
            fig_vol.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_vol, use_container_width=True)
        with col_b:
            st.markdown("#### Hourly Statutory Review Rate (% ≥ 300s)")
            fig_prop = px.bar(
                hourly_df, x="hour", y="pct_ge_300s",
                labels={"hour": "Hour of Day", "pct_ge_300s": "Review Trigger Share (%)"},
                color_discrete_sequence=["#f87171"]
            )
            fig_prop.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_prop, use_container_width=True)

with tab2:
    st.subheader("Day-of-Week Operational Comparison")
    st.caption("Examining weekday vs. weekend queue latency performance.")
    dow_df = compute_day_of_week_summary(df)

    if not dow_df.empty:
        fig_dow = go.Figure()
        fig_dow.add_trace(go.Bar(x=dow_df["day_of_week"], y=dow_df["mean"], name="Mean Wait (s)", marker_color="#2563eb"))
        fig_dow.add_trace(go.Bar(x=dow_df["day_of_week"], y=dow_df["median"], name="Median Wait (s)", marker_color="#10b981"))
        fig_dow.add_trace(go.Bar(x=dow_df["day_of_week"], y=dow_df["p95"], name="P95 Tail (s)", marker_color="#ef4444"))
        fig_dow.update_layout(
            template="plotly_white",
            barmode="group",
            xaxis_title="Day of Week",
            yaxis_title="Seconds",
            legend=dict(orientation="h", y=1.12, x=0),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_dow, use_container_width=True)

        st.dataframe(dow_df.rename(columns={
            "day_of_week": "Day", "count": "Calls", "mean": "Mean (s)", "median": "Median (s)", "p90": "P90 (s)", "p95": "P95 (s)", "calls_ge_300s": "Calls ≥ 300s", "pct_ge_300s": "Review Rate (%)"
        }), use_container_width=True)

with tab3:
    st.subheader("Hour × Day of Week Heatmap Matrix")
    st.caption("Identify temporal hotspots where delays or statutory review threshold rates spike.")

    metric_choice = st.selectbox(
        "Select Heatmap Metric:",
        options=["mean", "median", "p90", "pct_ge_300s"],
        format_func=lambda m: {
            "mean": "Mean Waiting Time (s)",
            "median": "Median Waiting Time (s)",
            "p90": "90th Percentile Tail Wait (s)",
            "pct_ge_300s": "Proportion Reaching Statutory Review Threshold (≥ 300s %)"
        }.get(m, m)
    )

    heatmap_df = compute_hour_weekday_heatmap_matrix(df, metric=metric_choice)
    if not heatmap_df.empty:
        fig_hm = px.imshow(
            heatmap_df,
            labels=dict(x="Day of Week", y="Hour of Day", color="Value"),
            x=heatmap_df.columns,
            y=heatmap_df.index,
            aspect="auto",
            color_continuous_scale="YlOrRd" if "300" in metric_choice or "p90" in metric_choice else "Blues"
        )
        fig_hm.update_layout(
            template="plotly_white",
            yaxis=dict(tickmode="linear", tick0=0, dtick=1),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_hm, use_container_width=True)
    else:
        st.info("Insufficient data to generate temporal heatmap.")
