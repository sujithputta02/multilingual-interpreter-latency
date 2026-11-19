"""Page 4: Distribution and Policy Analysis (PRD Section 13.4)."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.analytics.distribution_analysis import compute_mean_median_disparity, compute_ecdf
from src.analytics.policy_analysis import evaluate_oti_average_goal, evaluate_statutory_review_threshold
from src.storage.parquet_manager import load_processed_parquet

st.set_page_config(page_title="Distribution & Policy | Beyond the Average", layout="wide")

df = st.session_state.get("filtered_df")
if df is None:
    raw = load_processed_parquet()
    if raw is not None:
        df = raw
    else:
        st.warning("Dataset not loaded. Please return to the Home page to load data.")
        st.stop()

st.title("4. Distribution-Sensitive & Policy Analysis")
st.markdown("### Exposing Hidden Latency Patterns & Grounding Data in Municipal Legal Benchmarks")

tab_dist, tab_policy = st.tabs(["Distribution Sensitivity (Mean vs. Median)", "Municipal Policy Benchmarks"])

with tab_dist:
    st.subheader("The Limits of Aggregate Reporting: Mean vs. Median Disparity")
    st.markdown("""
    When waiting-time distributions have prolonged positive tails, the arithmetic **mean** is pulled upward,
    while simultaneously concealing severe delays experienced by callers in the 90th and 95th percentiles.
    Conversely, a cohort with an acceptable mean can harbor substantial upper-tail delays.
    """)

    disparity_df = compute_mean_median_disparity(df, min_sample_size=50)

    if not disparity_df.empty:
        st.dataframe(
            disparity_df[[
                "language", "count", "mean", "median", "mean_minus_median", "p90", "p95", "p95_to_median_ratio", "pct_ge_300s"
            ]].rename(columns={
                "language": "Language",
                "count": "Total Calls",
                "mean": "Mean (s)",
                "median": "Median (s)",
                "mean_minus_median": "Disparity (Mean - Median)",
                "p90": "P90 (s)",
                "p95": "P95 (s)",
                "p95_to_median_ratio": "Tail Ratio (P95 / Median)",
                "pct_ge_300s": "Share >= 300s (%)",
            }),
            use_container_width=True
        )

        # Disparity Scatter Plot
        fig_disp = px.scatter(
            disparity_df.head(25),
            x="mean",
            y="p95",
            size="count",
            color="mean_minus_median",
            text="language",
            labels={
                "mean": "Observed Mean Waiting Time (s)",
                "p95": "95th Percentile Tail Delay (P95, s)",
                "mean_minus_median": "Disparity (s)",
                "count": "Sample Volume"
            },
            title="Mean vs. 95th Percentile Waiting Time by Language (Size = Call Volume)",
            color_continuous_scale="Reds"
        )
        fig_disp.add_hline(y=300.0, line_dash="dash", line_color="red", annotation_text="300s Statutory Threshold")
        fig_disp.add_vline(x=30.0, line_dash="dash", line_color="green", annotation_text="30s OTI Goal")
        fig_disp.update_traces(textposition="top center")
        st.plotly_chart(fig_disp, use_container_width=True)

    # ECDF Curves
    st.subheader("Empirical Cumulative Distribution Functions (ECDF)")
    ecdf_langs = st.multiselect(
        "Select Languages for ECDF Plot:",
        options=sorted(df["language"].dropna().unique().tolist()),
        default=disparity_df.head(4)["language"].tolist() if not disparity_df.empty else []
    )

    if ecdf_langs:
        fig_ecdf = go.Figure()
        for l in ecdf_langs:
            sub_s = df[df["language"] == l]["connect_time_sec"]
            x_vals, y_vals = compute_ecdf(sub_s)
            fig_ecdf.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name=l))

        fig_ecdf.add_vline(x=30.0, line_dash="dot", line_color="green", annotation_text="30s Goal")
        fig_ecdf.add_vline(x=300.0, line_dash="dash", line_color="red", annotation_text="300s Review Threshold")
        fig_ecdf.update_layout(
            xaxis=dict(title="Waiting Time in Seconds (Log Scale)", type="log"),
            yaxis=dict(title="Cumulative Probability F(x)", tickformat=".0%"),
            hovermode="x unified"
        )
        st.plotly_chart(fig_ecdf, use_container_width=True)

with tab_policy:
    st.subheader("Benchmark 1: NYC OTI 30-Second Average Goal")
    st.caption("NYC Office of Technology and Innovation (OTI) 2024 Language Access Implementation Plan.")
    st.markdown("""
    The OTI Language Access Plan establishes a specific goal: ensuring that the **average** time
    to obtain a telephonic interpreter is **30 seconds or less** for four designated languages:
    **Spanish, Cantonese, Mandarin, and Russian**.
    """)

    oti_df = evaluate_oti_average_goal(df)
    if not oti_df.empty:
        st.dataframe(
            oti_df[[
                "language", "record_count", "observed_mean_sec", "reference_goal_sec", "delta_from_goal_sec", "satisfies_average_goal", "observed_median_sec", "observed_p95_sec", "pct_ge_300s"
            ]].rename(columns={
                "language": "Covered Language",
                "record_count": "Sample Calls",
                "observed_mean_sec": "Observed Mean (s)",
                "reference_goal_sec": "Target Goal (s)",
                "delta_from_goal_sec": "Difference (Delta)",
                "satisfies_average_goal": "Satisfies <= 30s Target",
                "observed_median_sec": "Observed Median (s)",
                "observed_p95_sec": "Observed P95 (s)",
                "pct_ge_300s": "Share >= 300s (%)",
            }),
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("Benchmark 2: 300-Second Statutory Review Threshold (§23-310)")
    st.caption("NYC Administrative Code §23-310: Language identification protocol review requirement.")
    st.markdown("""
    Under **NYC Administrative Code §23-310**, when an interpreter-request call has a waiting time of
    **300 seconds or longer**, 311 is required to review the call to determine whether delay resulted
    from a failure of its language-identification protocol.
    """)

    stat_res = evaluate_statutory_review_threshold(df)
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Total Calls Observed", f"{stat_res['total_calls']:,}")
    sc2.metric("Calls >= 300s (Eligible for Review)", f"{stat_res['threshold_calls_count']:,}")
    sc3.metric("Review Threshold Rate", f"{stat_res['threshold_percentage']}%")

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown("#### Languages with Highest Frequency of >= 300s Calls")
        if not stat_res["language_breakdown"].empty:
            st.dataframe(
                stat_res["language_breakdown"].head(10).rename(columns={
                    "language": "Language",
                    "total_calls": "Total Calls",
                    "threshold_calls": "Calls >= 300s",
                    "threshold_percentage": "Rate (%)"
                }),
                use_container_width=True
            )
    with col_l2:
        st.markdown("#### Distribution Comparison: Standard vs. Review-Threshold Calls")
        dist_comp = stat_res["distribution_comparison"]
        comp_table = pd.DataFrame([
            {
                "Cohort": "Standard Calls (< 300s)",
                "Calls": f"{dist_comp['standard_calls']['count']:,}",
                "Mean (s)": dist_comp['standard_calls']['mean'],
                "Median (s)": dist_comp['standard_calls']['median'],
                "P90 (s)": dist_comp['standard_calls']['p90'],
            },
            {
                "Cohort": "Statutory Review Calls (>= 300s)",
                "Calls": f"{dist_comp['review_threshold_calls']['count']:,}",
                "Mean (s)": dist_comp['review_threshold_calls']['mean'],
                "Median (s)": dist_comp['review_threshold_calls']['median'],
                "P90 (s)": dist_comp['review_threshold_calls']['p90'],
            }
        ])
        st.dataframe(comp_table, use_container_width=True)

    st.warning("""
    ⚖️ **Mandatory Legal Context (PRD Section 6.2):**
    A waiting time of 300 seconds or greater establishes eligibility for internal review under §23-310.
    It must **never** be labeled as a 'protocol failure', 'service violation', or 'discrimination incident',
    as the public dataset does not disclose the outcome or conclusion of any legal review.
    """)
