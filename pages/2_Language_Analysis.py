"""Page 2: Language Analysis (PRD Section 13.2)."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.analytics.language_analysis import compute_language_summary, compare_languages
from src.analytics.statistical_tests import run_kruskal_wallis_test, run_pairwise_mann_whitney
from src.storage.parquet_manager import load_processed_parquet

st.set_page_config(page_title="Language Analysis | Beyond the Average", layout="wide")

df = st.session_state.get("filtered_df")
if df is None:
    raw = load_processed_parquet()
    if raw is not None:
        df = raw
    else:
        st.warning("Dataset not loaded. Please return to the Home page to load data.")
        st.stop()

st.title("2. Language-Specific Waiting-Time Analysis")
st.markdown("### Investigating Disparities in Typical and Prolonged Connection Delays across Requested Languages")

# Controls
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    search_lang = st.text_input("Filter table by language name:", placeholder="e.g. Spanish, Mandarin, Arabic...")
with c2:
    min_sample = st.number_input("Minimum Sample Size Threshold:", min_value=1, max_value=5000, value=100, step=10, help="Languages with fewer records than this threshold are flagged as having limited statistical support.")
with c3:
    sort_by_metric = st.selectbox("Sort Table By:", options=["count", "mean", "median", "p95", "pct_ge_300s"], index=0)

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
            "calls_ge_300s": "Calls >= 300s",
            "pct_ge_300s": "Share >= 300s (%)",
            "has_sufficient_sample": "Sufficient Sample (>= Min)",
        }),
        use_container_width=True
    )
else:
    st.info("No languages match the specified criteria.")

st.markdown("---")

# Comparative Visualization
st.subheader("Comparative Waiting-Time Distributions (Selected Languages)")
available_langs = sorted(df["language"].dropna().unique().tolist())
top_default = summary_df.head(5)["language"].tolist() if not summary_df.empty else available_langs[:5]

compare_sel = st.multiselect("Select Languages to Compare Directly:", options=available_langs, default=top_default)

if compare_sel:
    sub_df = df[df["language"].isin(compare_sel)]

    # Box Plot comparison
    fig_box = px.box(
        sub_df,
        x="language",
        y="connect_time_sec",
        color="language",
        points=False,
        title="Waiting Time Distribution (Box Plot: Median, Quartiles, and Whiskers)",
        labels={"connect_time_sec": "Waiting Time (Seconds)", "language": "Language"}
    )
    fig_box.add_hline(y=300.0, line_dash="dash", line_color="red", annotation_text="300s Statutory Threshold (§23-310)")
    fig_box.add_hline(y=30.0, line_dash="dot", line_color="green", annotation_text="30s OTI Goal")
    st.plotly_chart(fig_box, use_container_width=True)

    # Inferential Statistical Testing Section
    st.markdown("---")
    st.subheader("Inferential Statistical Testing")
    st.caption("Testing non-parametric differences across language distributions (PRD Section 8.7).")

    test_tab1, test_tab2 = st.tabs(["Kruskal-Wallis Multi-Group Test", "Pairwise Mann-Whitney U Test"])

    with test_tab1:
        kw_res = run_kruskal_wallis_test(df, compare_sel, min_sample=10)
        if kw_res["status"] == "success":
            st.markdown(f"**Test Statistic ($H$):** `{kw_res['test_statistic_H']}` | **p-value:** `{kw_res['p_value']:.2e}`")
            st.markdown(f"**Effect Size ($\epsilon^2$):** `{kw_res['effect_size_epsilon_squared']}`")
            st.markdown(f"**Result:** {kw_res['interpretation']}")
            st.caption(f"ℹ️ {kw_res['practical_note']}")
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
                    st.markdown(f"**Comparing:** {lang1} ($N={mw_res['n_a']:,}$) vs {lang2} ($N={mw_res['n_b']:,}$)")
                    st.markdown(f"**Medians:** {lang1}: `{mw_res['median_a']}s` | {lang2}: `{mw_res['median_b']}s`")
                    st.markdown(f"**Means:** {lang1}: `{mw_res['mean_a']}s` | {lang2}: `{mw_res['mean_b']}s`")
                    st.markdown(f"**Mann-Whitney $U$ Statistic:** `{mw_res['u_statistic']}` | **p-value:** `{mw_res['raw_p_value']:.2e}`")
                    st.markdown(f"**Rank-Biserial Effect Size ($r$):** `{mw_res['rank_biserial_effect_size']}`")
                    st.markdown(f"**Status:** {mw_res['interpretation']}")
                else:
                    st.warning(mw_res["message"])
            else:
                st.info("Select two different languages for pairwise comparison.")
        else:
            st.info("Select at least 2 languages above to run pairwise comparisons.")

st.info("⚠️ **Observational Limitation:** Differences in connection waiting times represent observed queue latency. Without data on interpreter shift schedules or call volumes, differences must not be interpreted as evidence of intentional discrimination or provider bias (PRD Section 18).")
