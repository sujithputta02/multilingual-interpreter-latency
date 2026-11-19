"""Page 5: Data Quality, Methodology, and Reproducibility (PRD Section 13.5)."""
import json
import streamlit as st
import pandas as pd
from src.utils.metadata import load_json
from src.analytics.language_analysis import compute_language_summary
from src.storage.parquet_manager import load_processed_parquet

st.set_page_config(page_title="Data Quality & Methodology | Beyond the Average", layout="wide")

df = st.session_state.get("filtered_df")
if df is None:
    raw = load_processed_parquet()
    if raw is not None:
        df = raw
    else:
        st.warning("Dataset not loaded. Please return to the Home page to load data.")
        st.stop()

st.title("5. Data Quality, Methodology & Reproducibility")
st.markdown("### Transparent Audit Trail, Literature Evidence Base, and Research Governance")

tab_quality, tab_lit, tab_dict, tab_export = st.tabs([
    "Data Quality Audit",
    "IEEE Literature Survey & Research Gaps",
    "Data Dictionary & Policy Citations",
    "Data & Findings Export"
])

with tab_quality:
    st.subheader("Data Quality Report (PRD Section 12.5)")
    quality_report = load_json("data/metadata/data_quality_report.json")
    ingest_meta = load_json("data/metadata/ingestion_metadata.json")

    if quality_report:
        st.markdown(f"**Report Generated (UTC):** `{quality_report.get('report_generated_utc')}`")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Original Records", f"{quality_report.get('original_record_count', 0):,}")
        c2.metric("Valid Records", f"{quality_report.get('valid_record_count', 0):,}")
        c3.metric("Excluded Records", f"{quality_report.get('invalid_record_count', 0):,}")
        c4.metric("Distinct Languages", f"{quality_report.get('coverage', {}).get('distinct_languages_observed', 0)}")

        st.markdown("#### Quality Audit Breakdown")
        q_breakdown = pd.DataFrame([
            {"Metric": "Missing Call Timestamps", "Count": quality_report.get("missing_values", {}).get("call_time", 0)},
            {"Metric": "Missing Language Labels", "Count": quality_report.get("missing_values", {}).get("language", 0)},
            {"Metric": "Missing Waiting Times", "Count": quality_report.get("missing_values", {}).get("connect_time_sec", 0)},
            {"Metric": "Negative Waiting Times (Excluded)", "Count": quality_report.get("anomalies", {}).get("negative_connect_time", 0)},
            {"Metric": "Unparseable Timestamps (Excluded)", "Count": quality_report.get("anomalies", {}).get("invalid_timestamps", 0)},
            {"Metric": "Identical Triplet Records Preserved (§11.3)", "Count": quality_report.get("anomalies", {}).get("identical_triplet_records_preserved", 0)},
            {"Metric": "Calls >= 300s Preserved (§12.3)", "Count": quality_report.get("extreme_values_retained", {}).get("statutory_threshold_300s_or_more", 0)},
            {"Metric": "Maximum Observed Waiting Time (s)", "Count": quality_report.get("extreme_values_retained", {}).get("max_connect_time_sec", 0)},
        ])
        st.dataframe(q_breakdown, use_container_width=True)

        st.info(f"**Exclusion Justification:** {quality_report.get('exclusions', {}).get('justification')}")
    else:
        st.warning("No generated Data Quality Report found in `data/metadata/`.")

with tab_lit:
    st.subheader("IEEE Literature Survey Audit (Phase 0 Foundation)")
    st.markdown("""
    As established by the literature audit of 2023–2026 IEEE publications:
    - **Queueing Theory Antecedents:** Konrad & Liu (2023), Garyfallos et al. (2024), and De Andrade et al. (2023)
      establish that mean delays fail to characterize upper tails or SLA non-exceedance probabilities in non-stationary queues.
    - **Quantile Confidence Intervals:** Lolos et al. (2023, 2025) confirm methods for steady-state quantiles (P90, P95).
    - **Identified Research Gap:** No empirical study in the IEEE corpus has applied distribution-sensitive
      queueing metrics to municipal human interpreter telephone connection times across 100+ languages.
    """)

    st.markdown("#### Research Objectives (RO1 - RO7) & Questions (RQ1 - RQ4) Matrix")
    matrix_df = pd.DataFrame([
        {"Objective": "RO1 - Measure Waiting Times", "Research Question": "RQ1", "Metric": "Mean, Median, P90, P95, Std Dev, IQR", "Implementation Status": "Completed"},
        {"Objective": "RO2 - Language Disparities", "Research Question": "RQ1", "Metric": "Language-wise distribution and ranking", "Implementation Status": "Completed"},
        {"Objective": "RO3 - Temporal Patterns", "Research Question": "RQ2", "Metric": "Hourly, Day-of-Week, Monthly heatmaps", "Implementation Status": "Completed"},
        {"Objective": "RO4 - Hidden Delays", "Research Question": "RQ3", "Metric": "Mean vs. Median Disparity, Tail Ratios", "Implementation Status": "Completed"},
        {"Objective": "RO5 - Policy Benchmarks", "Research Question": "RQ4", "Metric": "OTI 30s Goal & §23-310 300s Review Threshold", "Implementation Status": "Completed"},
        {"Objective": "RO6 - Reproducibility", "Research Question": "N/A", "Metric": "Parquet snapshots, DuckDB, JSON metadata", "Implementation Status": "Completed"},
        {"Objective": "RO7 - Research Interface", "Research Question": "N/A", "Metric": "Interactive local Streamlit application", "Implementation Status": "Completed"},
    ])
    st.dataframe(matrix_df, use_container_width=True)

with tab_dict:
    st.subheader("Dataset Dictionary and Legal Authority")
    st.markdown("""
    ### Primary Dataset: NYC 311 Interpreter Wait Time (`dzvt-6g3v`)
    - **`call_time`:** Floating timestamp of interpreter request call.
    - **`language`:** Plain text requested interpretation language.
    - **`connect_time_sec`:** Number of seconds waited for Language Line interpreter connection.

    ### Statutory Citations:
    1. **NYC Administrative Code §23-308:** Standards for language assistance services.
    2. **NYC Administrative Code §23-310:** Mandatory language-identification protocol review when waiting time is >= 300 seconds.
    3. **NYC OTI 2024 Language Access Implementation Plan:** Average interpreter connection time target of <= 30 seconds for Spanish, Cantonese, Mandarin, and Russian.
    """)

with tab_export:
    st.subheader("Research Data and Artifact Export (PRD Section 15.2)")
    st.markdown("Download active filtered data or computed analytical summaries for external reproduction or publication.")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("#### Export Active Filtered Sample (CSV)")
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Calls (CSV)",
            data=csv_data,
            file_name="filtered_interpreter_calls.csv",
            mime="text/csv"
        )
    with col_e2:
        st.markdown("#### Export Language Summary Statistics (CSV)")
        lang_stats = compute_language_summary(df, min_sample_size=1)
        lang_csv = lang_stats.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Language Summary (CSV)",
            data=lang_csv,
            file_name="language_summary_metrics.csv",
            mime="text/csv"
        )
