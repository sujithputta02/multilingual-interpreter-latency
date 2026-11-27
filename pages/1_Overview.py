"""Page 1: Executive Overview & Interactive Cross-Filtering (PRD Section 13.1)."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.analytics.descriptive import calculate_descriptive_stats
from src.analytics.temporal_analysis import compute_monthly_trend
from src.analytics.language_analysis import compute_language_summary
from src.utils.filters import render_global_slicers
from src.utils.ui import apply_bi_theme, render_kpi, render_banner, render_active_filter_strip

st.set_page_config(page_title="Executive Overview | Beyond the Average", layout="wide")
apply_bi_theme()

raw_df, df = render_global_slicers()
if raw_df.empty:
    st.warning("Data warehouse not loaded. Please return to the Home page.")
    st.stop()

render_banner(
    "1. Executive Research Overview",
    "Interactive Performance Scorecard with Click-to-Filter Language Cross-Filtering",
    badge="Executive BI View"
)
render_active_filter_strip(len(df), len(raw_df))

if df.empty:
    st.warning("⚠️ No records match your active slicers.")
    st.stop()

# Interactive Language Cross-Filter Action
focus_lang = st.session_state.get("overview_focus_lang")
top_langs_list = df["language"].value_counts().head(8).index.tolist()

fc1, fc2 = st.columns([4, 1])
with fc1:
    chosen_focus = st.selectbox(
        "🎯 Cross-Filter Focus Language (or click any bar below):",
        options=["All Active Languages"] + top_langs_list,
        index=(["All Active Languages"] + top_langs_list).index(focus_lang) if focus_lang in top_langs_list else 0,
    )
    if chosen_focus == "All Active Languages":
        st.session_state["overview_focus_lang"] = None
        view_df = df
    else:
        st.session_state["overview_focus_lang"] = chosen_focus
        view_df = df[df["language"] == chosen_focus]
with fc2:
    st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True)
    if st.button("Clear Focus", use_container_width=True):
        st.session_state["overview_focus_lang"] = None
        st.rerun()

# Executive KPI Grid (dynamically reflects cross-filter!)
stats = calculate_descriptive_stats(view_df["connect_time_sec"])
k1, k2, k3, k4, k5, k6 = st.columns(6)

mean_v = stats.get("mean")
median_v = stats.get("median")
p90_v = stats.get("p90")
p95_v = stats.get("p95")
div_subtext = f"Divergence: {mean_v - median_v:.1f}s" if (mean_v is not None and median_v is not None) else "No data"

with k1:
    render_kpi("Connected Calls", f"{stats['count']:,}", st.session_state.get("overview_focus_lang") or "Active Slice", "Total", "info")
with k2:
    render_kpi("Mean Wait Time", f"{mean_v}s" if mean_v is not None else "N/A", "Arithmetic Average", "Mean", "info")
with k3:
    render_kpi("Median Wait (P50)", f"{median_v}s" if median_v is not None else "N/A", div_subtext, "Midpoint", "success")
with k4:
    render_kpi("90th Percentile (P90)", f"{p90_v}s" if p90_v is not None else "N/A", "Upper 10% Wait", "P90", "info")
with k5:
    render_kpi("95th Percentile (P95)", f"{p95_v}s" if p95_v is not None else "N/A", "Upper 5% Wait", "Tail", "danger")
with k6:
    render_kpi("Calls ≥ 300s", f"{stats['long_wait_count']:,}", f"{stats['long_wait_percentage']}% of calls", "§23-310", "danger" if stats["long_wait_percentage"] > 0.2 else "warning")

col_left, col_right = st.columns([3, 2])

with col_left:
    with st.container(border=True):
        st.subheader("Monthly Waiting-Time Trajectory")
        st.caption("Mean, Median, and P90 tail latency across months vs. the NYC OTI 30s Target.")
        monthly_df = compute_monthly_trend(view_df)
        if not monthly_df.empty:
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(x=monthly_df["year_month"], y=monthly_df["mean"], mode="lines+markers", name="Mean (s)", line=dict(color="#2563eb", width=3)))
            fig_trend.add_trace(go.Scatter(x=monthly_df["year_month"], y=monthly_df["median"], mode="lines+markers", name="Median (s)", line=dict(color="#10b981", width=2, dash="dash")))
            fig_trend.add_trace(go.Scatter(x=monthly_df["year_month"], y=monthly_df["p90"], mode="lines+markers", name="P90 Tail (s)", line=dict(color="#f59e0b", width=2, dash="dot")))
            fig_trend.add_hline(y=30.0, line_dash="dash", line_color="#ef4444", annotation_text="OTI 30s Target", annotation_position="bottom right")
            fig_trend.update_layout(template="plotly_white", xaxis_title="Month", yaxis_title="Seconds", hovermode="x unified", legend=dict(orientation="h", y=1.12, x=0), margin=dict(l=15, r=15, t=25, b=15))
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("Insufficient monthly data.")

with col_right:
    with st.container(border=True):
        st.subheader("Wait-Time Tier Distribution")
        st.caption("Call share categorized by connection duration tiers.")
        cat_counts = view_df["wait_category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Calls"]
        color_map = {
            "0-30s (Within Goal)": "#10b981",
            "31-60s": "#3b82f6",
            "61-120s": "#f59e0b",
            "121-299s": "#f97316",
            ">=300s (Statutory Review)": "#ef4444"
        }
        fig_cat = px.pie(cat_counts, names="Category", values="Calls", hole=0.55, color="Category", color_discrete_map=color_map)
        fig_cat.update_traces(textposition="inside", textinfo="percent+label")
        fig_cat.update_layout(template="plotly_white", showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_cat, use_container_width=True)

with st.container(border=True):
    st.subheader("Top Requested Languages: Click a Bar to Cross-Filter")
    lang_sum = compute_language_summary(df, min_sample_size=20, sort_by="count", ascending=False).head(10)
    if not lang_sum.empty:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["mean"], name="Mean Wait", marker_color="#2563eb"))
        fig_bar.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["median"], name="Median (P50)", marker_color="#10b981"))
        fig_bar.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["p95"], name="Tail Latency (P95)", marker_color="#ef4444"))
        fig_bar.update_layout(template="plotly_white", barmode="group", clickmode="event+select", xaxis_title="Language", yaxis_title="Seconds", legend=dict(orientation="h", y=1.12, x=0), margin=dict(l=15, r=15, t=25, b=15))

        selection = st.plotly_chart(fig_bar, use_container_width=True, on_select="rerun", key="overview_bar_select")
        if selection and selection.get("selection") and selection["selection"].get("points"):
            clicked_lang = selection["selection"]["points"][0].get("x")
            if clicked_lang and clicked_lang != st.session_state.get("overview_focus_lang"):
                st.session_state["overview_focus_lang"] = clicked_lang
                st.rerun()

        display_tbl = lang_sum[[
            "language", "count", "mean", "median", "p90", "p95", "std", "calls_ge_300s", "pct_ge_300s"
        ]].rename(columns={
            "language": "Language", "count": "Total Calls", "mean": "Mean (s)", "median": "Median (s)",
            "p90": "P90 (s)", "p95": "P95 (s)", "std": "Std Dev (s)", "calls_ge_300s": "Calls ≥ 300s", "pct_ge_300s": "Review Rate (%)"
        })
        st.dataframe(display_tbl, use_container_width=True)
