"""Page 4: Distribution Sensitivity & Policy Benchmark Scorecards (PRD Section 13.4)."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.analytics.distribution_analysis import compute_mean_median_disparity, compute_ecdf
from src.analytics.policy_analysis import evaluate_oti_average_goal, evaluate_statutory_review_threshold
from src.storage.parquet_manager import load_processed_parquet
from src.utils.ui import apply_bi_theme, render_kpi, render_banner

st.set_page_config(page_title="Distribution & Policy | Beyond the Average", layout="wide")
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
    "4. Distribution Sensitivity & Legal Benchmarks",
    "Exposing Information Concealed by Mean-Only Reporting & Evaluating Municipal Policy Targets",
    badge="Policy Scorecard"
)

tab_policy, tab_dist = st.tabs(["🏛️ Municipal Legal & Policy Benchmarks", "📊 Distribution Sensitivity (Mean vs. Median)"])

with tab_policy:
    st.subheader("Benchmark 1: NYC OTI 30-Second Average Target")
    st.caption("NYC Office of Technology and Innovation (OTI) 2024 Language Access Implementation Plan.")
    st.markdown("""
    The OTI Language Access Plan establishes an explicit aggregate performance goal:
    ensuring that the **average** time to obtain a telephonic interpreter is **30 seconds or less**
    specifically for **Spanish, Cantonese, Mandarin, and Russian**.
    """)

    oti_df = evaluate_oti_average_goal(df)
    if not oti_df.empty:
        # Display BI scorecard tiles for each of the 4 languages
        sc_cols = st.columns(4)
        for idx, row in oti_df.iterrows():
            with sc_cols[idx]:
                meets = row["satisfies_average_goal"]
                badge_t = "COMPLIANT" if meets else "ABOVE TARGET"
                b_type = "success" if meets else "danger"
                delta_str = f"{row['delta_from_goal_sec']:+.1f}s vs 30s target"
                render_kpi(
                    f"{row['language']} Queue",
                    f"{row['observed_mean_sec']}s",
                    delta_str,
                    badge_t,
                    b_type
                )

        st.markdown("#### Official Four-Language Scorecard Table")
        st.dataframe(
            oti_df[[
                "language", "record_count", "observed_mean_sec", "reference_goal_sec", "delta_from_goal_sec", "satisfies_average_goal", "observed_median_sec", "observed_p95_sec", "pct_ge_300s"
            ]].rename(columns={
                "language": "Covered Language",
                "record_count": "Calls Recorded",
                "observed_mean_sec": "Observed Mean (s)",
                "reference_goal_sec": "Policy Target (s)",
                "delta_from_goal_sec": "Delta (s)",
                "satisfies_average_goal": "Satisfies Target",
                "observed_median_sec": "Median (s)",
                "observed_p95_sec": "P95 Tail (s)",
                "pct_ge_300s": "Review Rate (%)",
            }),
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("Benchmark 2: 300-Second Statutory Review Threshold")
    st.caption("NYC Administrative Code §23-310: Mandatory language-identification protocol review trigger.")
    st.markdown("""
    Under **NYC Administrative Code §23-310**, when an interpreter-request call has a waiting time of
    **300 seconds or longer**, 311 is legally required to review the call to determine whether delay resulted
    from a failure of its language-identification protocol.
    """)

    stat_res = evaluate_statutory_review_threshold(df)
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        render_kpi("Total Calls Evaluated", f"{stat_res['total_calls']:,}", "Cohort Base", "Base", "info")
    with sc2:
        render_kpi("Calls ≥ 300s (Review Required)", f"{stat_res['threshold_calls_count']:,}", "Triggered §23-310", "Statutory Trigger", "danger")
    with sc3:
        render_kpi("Overall Review Trigger Rate", f"{stat_res['threshold_percentage']}%", "of all connected calls", "Review Rate", "danger" if stat_res['threshold_percentage'] > 1.0 else "info")

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown("#### Highest Review-Triggered Languages")
        if not stat_res["language_breakdown"].empty:
            st.dataframe(
                stat_res["language_breakdown"].head(10).rename(columns={
                    "language": "Language",
                    "total_calls": "Total Calls",
                    "threshold_calls": "Calls ≥ 300s",
                    "threshold_percentage": "Review Rate (%)"
                }),
                use_container_width=True
            )
    with col_l2:
        st.markdown("#### Cohort Partition: Standard (<300s) vs. Review (≥300s)")
        dist_comp = stat_res["distribution_comparison"]
        comp_table = pd.DataFrame([
            {
                "Operational Cohort": "Standard Operation (< 300s)",
                "Call Volume": f"{dist_comp['standard_calls']['count']:,}",
                "Mean (s)": dist_comp['standard_calls']['mean'],
                "Median (s)": dist_comp['standard_calls']['median'],
                "P90 (s)": dist_comp['standard_calls']['p90'],
            },
            {
                "Operational Cohort": "Statutory Review Cohort (≥ 300s)",
                "Call Volume": f"{dist_comp['review_threshold_calls']['count']:,}",
                "Mean (s)": dist_comp['review_threshold_calls']['mean'],
                "Median (s)": dist_comp['review_threshold_calls']['median'],
                "P90 (s)": dist_comp['review_threshold_calls']['p90'],
            }
        ])
        st.dataframe(comp_table, use_container_width=True)

    st.markdown("""
    <div class="bi-callout" style="border-left-color: #f59e0b; background-color: #fffbeb; color: #92400e;">
        <strong>Legal Citation & Strict Attribution Scope:</strong> A waiting time of 300 seconds or greater is an indicator of eligibility for review under NYC Administrative Code §23-310. It must <strong>never</strong> be reported as a confirmed 'protocol failure', 'service violation', or 'discrimination incident', because the published open dataset does not provide the outcome or conclusions of the mandated review (PRD Section 6.2).
    </div>
    """, unsafe_allow_html=True)

with tab_dist:
    st.subheader("The Limits of Aggregate Reporting: Mean vs. Median Disparity")
    st.markdown("""
    When waiting times follow heavily skewed queue distributions, arithmetic **averages mask prolonged delays**.
    A language queue can maintain an ostensibly acceptable mean while callers in the 95th percentile experience extreme wait times.
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
                "pct_ge_300s": "Review Rate (%)",
            }),
            use_container_width=True
        )

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
            title="Mean vs. 95th Percentile Tail Delay (Circle Size = Call Volume)",
            color_continuous_scale="Reds"
        )
        fig_disp.add_hline(y=300.0, line_dash="dash", line_color="#ef4444", annotation_text="300s Statutory Threshold")
        fig_disp.add_vline(x=30.0, line_dash="dash", line_color="#10b981", annotation_text="30s OTI Goal")
        fig_disp.update_traces(textposition="top center")
        fig_disp.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_disp, use_container_width=True)

    st.subheader("Empirical Cumulative Distribution Functions (ECDF)")
    st.caption("Cumulative probability F(x) of connecting within x seconds on a logarithmic time scale.")

    ecdf_langs = st.multiselect(
        "Select Languages for ECDF Curve Comparison:",
        options=sorted(df["language"].dropna().unique().tolist()),
        default=disparity_df.head(4)["language"].tolist() if not disparity_df.empty else []
    )

    if ecdf_langs:
        fig_ecdf = go.Figure()
        for l in ecdf_langs:
            sub_s = df[df["language"] == l]["connect_time_sec"]
            x_vals, y_vals = compute_ecdf(sub_s)
            fig_ecdf.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name=l, line=dict(width=2)))

        fig_ecdf.add_vline(x=30.0, line_dash="dot", line_color="#10b981", annotation_text="30s Goal")
        fig_ecdf.add_vline(x=300.0, line_dash="dash", line_color="#ef4444", annotation_text="300s Review Threshold")
        fig_ecdf.update_layout(
            template="plotly_white",
            xaxis=dict(title="Waiting Time in Seconds (Log Scale)", type="log"),
            yaxis=dict(title="Cumulative Probability F(x)", tickformat=".0%"),
            hovermode="x unified",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_ecdf, use_container_width=True)
