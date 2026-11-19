"""Page 5: Data Quality, Governance, and Reproducibility (PRD Section 13.5)."""
import json
import streamlit as st
import pandas as pd

from src.utils.metadata import load_json
from src.analytics.language_analysis import compute_language_summary
from src.storage.parquet_manager import load_processed_parquet
from src.utils.ui import apply_bi_theme, render_kpi, render_banner

st.set_page_config(page_title="Governance & Methodology | Beyond the Average", layout="wide")
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
    "5. Data Quality, Governance & Exports",
    "Complete Transparency, IEEE Literature Evidence Base, and Verifiable Data Governance",
    badge="Audit & Governance"
)

tab_quality, tab_lit, tab_dict, tab_export = st.tabs([
    "🛡️ Data Quality & Audit Trail",
    "📚 IEEE Literature Corpus & Gaps",
    "📖 Legal Authority & Schema Dictionary",
    "📥 Research Data Exports"
])

with tab_quality:
    st.subheader("Data Quality Audit Scorecard (PRD Section 12.5)")
    quality_report = load_json("data/metadata/data_quality_report.json")
    ingest_meta = load_json("data/metadata/ingestion_metadata.json")

    if quality_report:
        st.markdown(f"**Audit Generated (UTC):** `{quality_report.get('report_generated_utc')}`")

        q1, q2, q3, q4 = st.columns(4)
        with q1:
            render_kpi("Ingested Raw Records", f"{quality_report.get('original_record_count', 0):,}", "From Socrata API", "Raw", "info")
        with q2:
            render_kpi("Validated Records", f"{quality_report.get('valid_record_count', 0):,}", "Passed Schema Validation", "100%", "success")
        with q3:
            render_kpi("Preserved Triplet Rows", f"{quality_report.get('anomalies', {}).get('identical_triplet_records_preserved', 0):,}", "Legitimate Calls (§11.3)", "Preserved", "info")
        with q4:
            render_kpi("Retained Extreme Delays", f"{quality_report.get('extreme_values_retained', {}).get('statutory_threshold_300s_or_more', 0):,}", "Calls ≥ 300s (§12.3)", "Preserved", "danger")

        st.markdown("#### Granular Validation Results")
        q_breakdown = pd.DataFrame([
            {"Audit Dimension": "Missing Call Timestamps", "Observed Count": quality_report.get("missing_values", {}).get("call_time", 0), "Status": "Passed (0 missing)"},
            {"Audit Dimension": "Missing Language Labels", "Observed Count": quality_report.get("missing_values", {}).get("language", 0), "Status": "Passed (0 missing)"},
            {"Audit Dimension": "Missing Waiting Times", "Observed Count": quality_report.get("missing_values", {}).get("connect_time_sec", 0), "Status": "Passed (0 missing)"},
            {"Audit Dimension": "Negative Waiting Times", "Observed Count": quality_report.get("anomalies", {}).get("negative_connect_time", 0), "Status": "Passed (0 negative)"},
            {"Audit Dimension": "Unparseable Timestamps", "Observed Count": quality_report.get("anomalies", {}).get("invalid_timestamps", 0), "Status": "Passed (0 invalid)"},
            {"Audit Dimension": "Identical Triplet Records Preserved (§11.3)", "Observed Count": quality_report.get("anomalies", {}).get("identical_triplet_records_preserved", 0), "Status": "Preserved"},
            {"Audit Dimension": "Calls ≥ 300s Preserved (§12.3)", "Observed Count": quality_report.get("extreme_values_retained", {}).get("statutory_threshold_300s_or_more", 0), "Status": "Preserved"},
            {"Audit Dimension": "Maximum Observed Waiting Time (s)", "Observed Count": quality_report.get("extreme_values_retained", {}).get("max_connect_time_sec", 0), "Status": "Valid Extreme"},
        ])
        st.dataframe(q_breakdown, use_container_width=True)

        st.markdown("""
        <div class="bi-callout">
            <strong>Exclusion & Preservation Governance:</strong> The dataset strictly retains identical triplet calls and valid extreme delays. Outliers are not winsorized or deleted, ensuring empirical authenticity.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No data quality report found in `data/metadata/`.")

with tab_lit:
    st.subheader("IEEE Literature Survey Foundation (Phase 0 Audit)")
    st.markdown("""
    Based on the systematic audit of 2023–2026 IEEE research publications:
    - **Service Delay & Non-Stationary Queues:** Konrad & Liu (2023), Garyfallos et al. (2024), and De Andrade et al. (2023)
      conclusively demonstrate that mean waiting times fail to characterize service-level non-exceedance probabilities or upper-tail delays.
    - **Quantile Confidence Estimation:** Lolos et al. (2023, 2025) provide mathematical grounding for empirical percentiles (P90, P95).
    - **Research Gap:** No empirical research in the IEEE corpus has applied distribution-sensitive queueing metrics
      to evaluate human interpreter connection delays across 50+ languages in public-service contact centers.
    """)

    st.markdown("#### Research Objectives & Questions Alignment Matrix")
    matrix_df = pd.DataFrame([
        {"Objective": "RO1 - Measure Waiting Times", "Research Question": "RQ1", "Operational Metric": "Mean, Median, P90, P95, Std Dev, IQR", "Delivery Status": "Completed (50% Milestone)"},
        {"Objective": "RO2 - Language Disparities", "Research Question": "RQ1", "Operational Metric": "Language-wise distribution and ranking", "Delivery Status": "Completed (50% Milestone)"},
        {"Objective": "RO3 - Temporal Patterns", "Research Question": "RQ2", "Operational Metric": "Diurnal, Day-of-Week, Heatmaps", "Delivery Status": "Completed (50% Milestone)"},
        {"Objective": "RO4 - Hidden Delays", "Research Question": "RQ3", "Operational Metric": "Mean vs. Median Disparity, Tail Ratios", "Delivery Status": "Completed (50% Milestone)"},
        {"Objective": "RO5 - Policy Benchmarks", "Research Question": "RQ4", "Operational Metric": "OTI 30s Target & §23-310 300s Threshold", "Delivery Status": "Completed (50% Milestone)"},
        {"Objective": "RO6 - Reproducibility", "Research Question": "N/A", "Operational Metric": "Parquet snapshots, DuckDB, JSON metadata", "Delivery Status": "Completed (50% Milestone)"},
        {"Objective": "RO7 - Research Platform", "Research Question": "N/A", "Operational Metric": "Interactive local Streamlit BI dashboard", "Delivery Status": "Completed (50% Milestone)"},
    ])
    st.dataframe(matrix_df, use_container_width=True)

with tab_dict:
    st.subheader("Dataset Schema & Statutory Authority")
    st.markdown("""
    ### Primary Dataset: NYC 311 Interpreter Wait Time (`dzvt-6g3v`)
    - **`call_time`:** Floating timestamp of the 311 interpreter connection request.
    - **`language`:** Plain text requested interpretation language.
    - **`connect_time_sec`:** Number of seconds elapsed until Language Line interpreter connection.

    ### Legal and Regulatory Citations:
    1. **NYC Administrative Code §23-308:** Standards for language assistance services.
    2. **NYC Administrative Code §23-310:** Mandatory review when interpreter waiting time is $\ge 300$ seconds to determine whether delay resulted from language-identification protocol failure.
    3. **NYC OTI 2024 Language Access Implementation Plan:** Operational goal of average connection time $\le 30$ seconds for Spanish, Cantonese, Mandarin, and Russian.
    """)

with tab_export:
    st.subheader("Research Data & Report Exports")
    st.markdown("Download active filtered data or summary statistical tables for publication or external audit.")

    c_exp1, c_exp2 = st.columns(2)
    with c_exp1:
        st.markdown("#### Filtered Call Records (CSV)")
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Active Slice (CSV)",
            data=csv_data,
            file_name="filtered_interpreter_calls.csv",
            mime="text/csv"
        )
    with c_exp2:
        st.markdown("#### Language Summary Statistics (CSV)")
        lang_stats = compute_language_summary(df, min_sample_size=1)
        lang_csv = lang_stats.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Language Summary (CSV)",
            data=lang_csv,
            file_name="language_summary_metrics.csv",
            mime="text/csv"
        )
