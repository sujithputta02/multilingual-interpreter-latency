"""Beyond the Average: Main Streamlit Research Application & BI Dashboard."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.ingestion.refresh import run_full_pipeline
from src.analytics.descriptive import calculate_descriptive_stats
from src.analytics.language_analysis import compute_language_summary
from src.analytics.policy_analysis import evaluate_oti_average_goal
from src.utils.filters import render_global_slicers
from src.utils.ui import apply_bi_theme, render_kpi, render_banner, render_active_filter_strip

st.set_page_config(
    page_title="Beyond the Average | BI Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_bi_theme()


def main():
    df, filtered_df = render_global_slicers()

    if df.empty:
        render_banner("Beyond the Average", "Research & BI Platform for Municipal Multilingual Services")
        st.info("The local analytical data warehouse has not been initialized.")
        if st.button("Initialize Analytical Pipeline"):
            with st.spinner("Acquiring and engineering NYC 311 Interpreter records..."):
                try:
                    run_full_pipeline(max_records=None)
                    st.cache_data.clear()
                    st.success("Warehouse initialized successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Initialization error: {e}")
        return

    if filtered_df.empty:
        render_banner(
            "Beyond the Average: Municipal Interpreter BI Platform",
            "Policy-Aware, Distribution-Sensitive Analysis of NYC 311 Multilingual Waiting Times",
            badge="0 Calls Matching Filter"
        )
        render_active_filter_strip(0, len(df))
        st.warning("⚠️ No call records match the current slicer selection. Click **Reset All** in the sidebar.")
        return

    render_banner(
        "Beyond the Average: Municipal Interpreter BI Suite",
        "Policy-Aware, Distribution-Sensitive Analysis of NYC 311 Multilingual Public-Service Waiting Times",
        badge=f"{len(filtered_df):,} Active Calls"
    )
    render_active_filter_strip(len(filtered_df), len(df))

    # Interactive Quick BI Actions Bar
    act1, act2, act3, act4, act5 = st.columns(5)
    if act1.button("📈 Open Full Overview", use_container_width=True):
        st.switch_page("pages/1_Overview.py")
    if act2.button("🌐 Compare Languages", use_container_width=True):
        st.switch_page("pages/2_Language_Analysis.py")
    if act3.button("🔥 Temporal Heatmaps", use_container_width=True):
        st.switch_page("pages/3_Temporal_Analysis.py")
    if act4.button("⚖️ Policy & Sensitivity", use_container_width=True):
        st.switch_page("pages/4_Distribution_and_Policy.py")
    if act5.button("🚨 Focus ≥300s Delays", use_container_width=True):
        st.session_state["slicer_tier"] = "Statutory Review (≥300s)"
        st.rerun()

    # Executive BI KPI Grid
    stats = calculate_descriptive_stats(filtered_df["connect_time_sec"])
    mean_v = stats.get("mean")
    median_v = stats.get("median")
    p95_v = stats.get("p95")
    div_subtext = f"Divergence: +{mean_v - median_v:.1f}s" if (mean_v is not None and median_v is not None) else "No data"
    tail_subtext = f"{p95_v / max(1.0, median_v):.1f}x Median" if (p95_v is not None and median_v is not None) else "No data"

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        render_kpi("Connected Calls", f"{stats['count']:,}", f"{filtered_df['language'].nunique()} languages", "NYC 311", "info")
    with k2:
        render_kpi("Mean Wait Time", f"{mean_v}s" if mean_v is not None else "N/A", "Arithmetic Average", "Mean", "info")
    with k3:
        render_kpi("Median Wait (P50)", f"{median_v}s" if median_v is not None else "N/A", div_subtext, "Midpoint", "success")
    with k4:
        render_kpi("Tail Delay (P95)", f"{p95_v}s" if p95_v is not None else "N/A", tail_subtext, "Upper Tail", "danger")
    with k5:
        render_kpi("Calls ≥ 300s", f"{stats['long_wait_count']:,}", f"{stats['long_wait_percentage']}% of slice", "§23-310", "danger" if stats["long_wait_percentage"] > 0.2 else "warning")

    # 2-Column Live BI Visual Preview with Tableau-Style Click Actions
    col_l, col_r = st.columns([3, 2])
    with col_l:
        with st.container(border=True):
            st.subheader("Top Languages: Mean vs. P95 Tail Latency")
            st.caption("💡 Tap any language bar to filter the entire dashboard to that language (tap again or Reset All to clear).")
            lang_sum = compute_language_summary(filtered_df, min_sample_size=10, sort_by="count", ascending=False).head(7)
            if not lang_sum.empty:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["mean"], name="Mean (s)", marker_color="#2563eb"))
                fig.add_trace(go.Bar(x=lang_sum["language"], y=lang_sum["p95"], name="P95 Tail (s)", marker_color="#ef4444"))
                fig.add_hline(y=30.0, line_dash="dash", line_color="#10b981", annotation_text="OTI 30s Goal")
                fig.update_layout(
                    template="plotly_white", paper_bgcolor="white", plot_bgcolor="white",
                    font=dict(color="#0f172a"), barmode="group", clickmode="event+select",
                    height=320, margin=dict(l=15, r=15, t=25, b=15), legend=dict(orientation="h", y=1.12)
                )
                sel = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="home_lang_bar")
                if sel and sel.get("selection") and sel["selection"].get("points"):
                    clicked = sel["selection"]["points"][0].get("x")
                    if clicked:
                        cur = st.session_state.get("slicer_langs", [])
                        if cur == [clicked]:
                            st.session_state["slicer_langs"] = []
                        else:
                            st.session_state["slicer_langs"] = [clicked]
                        st.rerun()

    with col_r:
        with st.container(border=True):
            st.subheader("OTI 30s Target Scorecard")
            oti_df = evaluate_oti_average_goal(filtered_df)
            if not oti_df.empty:
                for _, r in oti_df.iterrows():
                    m_val = r["observed_mean_sec"]
                    meets = r["satisfies_average_goal"]
                    badge = '<span class="bi-badge-success">PASS</span>' if meets else ('<span class="bi-badge-danger">FAIL</span>' if meets is False else '<span class="bi-badge-info">N/A</span>')
                    val_str = f"{m_val}s (P95: {r['observed_p95_sec']}s)" if m_val is not None else "No calls in slice"
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f1f5f9;">
                        <div><strong>{r['language']}</strong><br><span style="font-size:0.78rem; color:#64748b;">{r['record_count']:,} calls</span></div>
                        <div style="text-align:right;">{badge}<br><span style="font-size:0.8rem; color:#0f172a; font-weight:600;">{val_str}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

    if mean_v is not None and median_v is not None and p95_v is not None:
        st.markdown(f"""
        <div class="bi-callout">
            <strong>Live Analytical Insight:</strong> In the active slice, the typical caller connects in <strong>{median_v}s</strong> (median), while the arithmetic mean is <strong>{mean_v}s</strong> and upper-tail callers (P95) wait <strong>{p95_v}s</strong>. <strong>{stats['long_wait_count']:,} calls ({stats['long_wait_percentage']:.2f}%)</strong> reached the 300-second statutory review threshold.
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
