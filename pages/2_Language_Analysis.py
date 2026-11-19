"""Page 2: Language Analysis & Inferential Testing (PRD Section 13.2)."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.analytics.language_analysis import compute_language_summary, compare_languages
from src.analytics.statistical_tests import run_kruskal_wallis_test, run_pairwise_mann_whitney
from src.storage.parquet_manager import load_processed_parquet
from src.utils.ui import apply_bi_theme, render_kpi, render_banner

st.set_page_config(page_title="Language Analysis | Beyond the Average", layout="wide")
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
    "2. Language Cohort Analysis",
    "Investigating Disparities in Typical and Prolonged Connection Delays across Requested Languages",
    badge="Comparative Analytics"
)

# Filter controls
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    search_lang = st.text_input("🔍 Search Language:", placeholder="e.g. Spanish, Mandarin, Russian, Arabic...")
with c2:
    min_sample = st.number_input(
        "Min. Sample Threshold:",
        min_value=1, max_value=5000, value=100, step=10,
        help="Languages with sample sizes below this threshold are flagged as having limited statistical support."
    )
with c3:
    sort_by_metric = st.selectbox(
        "Sort By Metric:",
        options=["count", "mean", "median", "p95", "pct_ge_300s"],
        format_func=lambda m: {
            "count": "Total Volume (Count)",
            "mean": "Mean Wait Time",
            "median": "Median Wait Time",
            "p95": "95th Percentile Tail",
            "pct_ge_300s": "Review Rate (% ≥ 300s)"
        }.get(m, m)
    )

summary_df = compute_language_summary(df, min_sample_size=min_sample, sort_by=sort_by_metric, ascending=False)

if search_lang:
    summary_df = summary_df[summary_df["language"].str.contains(search_lang, case=False, na=False)]

st.subheader("Language Metrics Ranking Table")
if not summary_df.empty:
    st.dataframe(
        summary_df[[
            "language", "count", "mean", "median", "p90", "p95", "std", "iqr", "calls_ge_300s", "pct_ge_300s", "has_sufficient_sample"
        ]].rename(columns={
            "language": "Language",
            "count": "Total Calls",
            "mean": "Mean (s)",
            "median": "Median (s)",
            "p90": "P90 (s)",
            "p95": "P95 (s)",
            "std": "Std Dev (s)",
            "iqr": "IQR (s)",
            "calls_ge_300s": "Calls ≥ 300s",
            "pct_ge_300s": "Review Rate (%)",
            "has_sufficient_sample": "Sufficient Sample",
        }),
        use_container_width=True
    )
else:
    st.info("No languages match the specified criteria.")

st.markdown("---")

# Visual Drill-down
st.subheader("Comparative Distribution Box Plots")
st.caption("Visualizing the spread, median, quartiles, and upper tail across selected language cohorts.")

available_langs = sorted(df["language"].dropna().unique().tolist())
top_default = summary_df.head(6)["language"].tolist() if not summary_df.empty else available_langs[:6]
compare_sel = st.multiselect("Select Languages to Drill Down:", options=available_langs, default=top_default)

if compare_sel:
    sub_df = df[df["language"].isin(compare_sel)]

    fig_box = px.box(
        sub_df,
        x="language",
        y="connect_time_sec",
        color="language",
        points=False,
        labels={"connect_time_sec": "Waiting Time (Seconds)", "language": "Language"}
    )
    fig_box.add_hline(y=300.0, line_dash="dash", line_color="#ef4444", annotation_text="300s Statutory Threshold (§23-310)")
    fig_box.add_hline(y=30.0, line_dash="dot", line_color="#10b981", annotation_text="30s OTI Goal")
    fig_box.update_layout(
        template="plotly_white",
        yaxis_title="Waiting Time (Seconds)",
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Inferential Testing Section
    st.markdown("---")
    st.subheader("Non-Parametric Inferential Hypothesis Testing")
    st.caption("Testing whether observed differences across language distributions are statistically significant (PRD Section 8.7).")

    test_tab1, test_tab2 = st.tabs(["Kruskal-Wallis Multi-Group Test", "Pairwise Mann-Whitney U Test"])

    with test_tab1:
        kw_res = run_kruskal_wallis_test(df, compare_sel, min_sample=10)
        if kw_res["status"] == "success":
            st.markdown(f"""
            <div class="bi-panel">
                <h4 style="margin: 0 0 10px 0; color: #1e293b;">Kruskal-Wallis Multi-Group Comparison</h4>
                <div style="display: flex; gap: 24px; margin-bottom: 12px;">
                    <div><strong>Test Statistic (H):</strong> <code>{kw_res['test_statistic_H']}</code></div>
                    <div><strong>p-value:</strong> <code>{kw_res['p_value']:.2e}</code></div>
                    <div><strong>Effect Size (ε²):</strong> <code>{kw_res['effect_size_epsilon_squared']}</code></div>
                </div>
                <p style="margin-bottom: 6px;"><strong>Result:</strong> {kw_res['interpretation']}</p>
                <span class="bi-badge-info">ℹ️ {kw_res['practical_note']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(kw_res["message"])

    with test_tab2:
        if len(compare_sel) >= 2:
            p_c1, p_c2 = st.columns(2)
            with p_c1:
                lang1 = st.selectbox("Language A:", options=compare_sel, index=0)
            with p_c2:
                lang2 = st.selectbox("Language B:", options=compare_sel, index=min(1, len(compare_sel)-1))

            if lang1 != lang2:
                mw_res = run_pairwise_mann_whitney(df, lang1, lang2)
                if mw_res.get("status") != "error":
                    st.markdown(f"""
                    <div class="bi-panel">
                        <h4 style="margin: 0 0 10px 0; color: #1e293b;">Mann-Whitney U Pairwise Comparison: {lang1} vs. {lang2}</h4>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 14px;">
                            <div><span style="font-size: 0.75rem; color: #64748b;">N ({lang1}):</span><br><strong>{mw_res['n_a']:,}</strong></div>
                            <div><span style="font-size: 0.75rem; color: #64748b;">Median ({lang1}):</span><br><strong>{mw_res['median_a']}s</strong></div>
                            <div><span style="font-size: 0.75rem; color: #64748b;">N ({lang2}):</span><br><strong>{mw_res['n_b']:,}</strong></div>
                            <div><span style="font-size: 0.75rem; color: #64748b;">Median ({lang2}):</span><br><strong>{mw_res['median_b']}s</strong></div>
                        </div>
                        <div style="display: flex; gap: 24px; margin-bottom: 10px;">
                            <div><strong>U Statistic:</strong> <code>{mw_res['u_statistic']}</code></div>
                            <div><strong>Raw p-value:</strong> <code>{mw_res['raw_p_value']:.2e}</code></div>
                            <div><strong>Rank-Biserial Correlation (r):</strong> <code>{mw_res['rank_biserial_effect_size']}</code></div>
                        </div>
                        <p style="margin: 0;"><strong>Interpretation:</strong> {mw_res['interpretation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning(mw_res["message"])
            else:
                st.info("Select two different languages for pairwise comparison.")

st.markdown("""
<div class="bi-callout">
    <strong>Observational Methodology Note:</strong> Observed differences across requested languages reflect queue connection latency under operational conditions. In the absence of third-party staffing logs, shift rotations, or translator pool depths, these empirical variations cannot be interpreted as intentional discrimination or provider bias (PRD Section 18).
</div>
""", unsafe_allow_html=True)
