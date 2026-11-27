# Beyond the Average: Research Platform

> **A Policy-Aware, Distribution-Sensitive Analysis of Multilingual Public-Service Interpreter Waiting Times**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/pytest-20%20passed-brightgreen.svg)]()
[![Dataset](https://img.shields.io/badge/NYC%20Open%20Data-1.06M%20Records-orange.svg)](https://data.cityofnewyork.us/City-Government/311-Interpreter-Wait-Time/dzvt-6g3v)

---

## 1. Project Overview

**Beyond the Average** is a local research analytics platform investigating interpreter connection waiting times in multilingual municipal public services using the **New York City 311 Interpreter Wait Time dataset (`dzvt-6g3v`)**.

The platform moves beyond conventional aggregate (mean-only) reporting to uncover how waiting times are distributed across 50+ requested languages and temporal periods, whether aggregate metrics mask prolonged delays, and how observed performance compares against official municipal language-access policy benchmarks:
1. **NYC OTI 2024 Language Access Implementation Plan:** 30-second average connection goal for Spanish, Cantonese, Mandarin, and Russian.
2. **NYC Administrative Code §23-310:** 300-second statutory review threshold for language-identification protocol review.

---

## 2. Completed 90% Milestone Deliverables

This repository delivers the **90% milestone** (Phases 0–7 complete) of the complete project specification as mandated by the PRD:

- [x] **Phase 0–5 (Core Platform & Full Dataset):**
  - Complete **1,061,195** raw records (`1,061,097` validated, `112` languages, Jan 2023 – Oct 2026) ingested from NYC Open Data (`dzvt-6g3v`).
  - Full 5-page interactive Streamlit BI dashboard with DuckDB & Parquet warehouse.
- [x] **Phase 6: Research Comparison & Sensitivity Analysis:**
  - Mean-only vs. distribution-sensitive metric ranking shifts (`src/analytics/comparison_analysis.py`).
  - Empirical detection of similar-mean, divergent-tail language pairs (e.g., Turkish vs. Yiddish).
  - 95% confidence intervals (Normal/t, Bootstrap quantiles, Wilson score proportions).
  - Sample-size cutoff sensitivity (`30, 50, 100, 500, 1000`) & temporal year-by-year sensitivity (`2023–2026`).
- [x] **Phase 7: Documentation & Publication Preparation:**
  - Publication-ready CSV tables and PNG figures in `research/results/tables/` and `research/results/figures/`.
  - Complete empirical findings & RQ1–RQ4 discussion in `research/results/research_findings_and_discussion.md`.
  - IEEE-format manuscript draft in `research/results/ieee_paper_draft.md`.
  - Reproducibility metadata JSON & PNG/CSV exports integrated into the UI (`src/utils/exports.py`).
- [x] **Automated Test Suite:** 20 unit and integration tests passing in `tests/` (including offline fallback & export tests).

---

## 3. Quickstart & Installation

### Step 1: Activate Virtual Environment
```bash
source .venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Unit & Integration Tests
```bash
pytest tests/
```

### Step 4: Run the Ingestion Pipeline (Acquire Real NYC 311 Records)
```bash
PYTHONPATH=. python scripts/run_pipeline.py --max-records 50000
```

### Step 5: Launch the Interactive Research Application
```bash
streamlit run app.py
```

---

## 4. Project Directory Structure

```text
beyond-the-average/
├── app.py                     # Main Streamlit application and global filters
├── config/
│   ├── settings.yaml          # Dataset endpoint, paths, and batch configuration
│   ├── policy_thresholds.yaml # OTI 30s Goal & §23-310 Statutory Threshold specs
│   └── analysis_config.yaml   # Time period definitions and quantile settings
├── data/
│   ├── raw/                   # Immutable raw Parquet snapshots
│   ├── processed/             # Cleaned and feature-engineered Parquet dataset
│   ├── analytics/             # DuckDB analytical views
│   └── metadata/              # Ingestion metadata & data quality JSON reports
├── docs/
│   ├── architecture.md        # Architecture specification and data flow
│   ├── data_dictionary.md     # Raw and derived schema definitions
│   ├── methodology.md         # Statistical formulas and study design
│   └── limitations.md         # Epistemological scope and non-causal warnings
├── pages/
│   ├── 1_Overview.py          # Descriptive summary and monthly trajectories
│   ├── 2_Language_Analysis.py # Language comparisons and inferential tests
│   ├── 3_Temporal_Analysis.py # Diurnal, day-of-week, and heatmap dynamics
│   ├── 4_Distribution_and_Policy.py # Mean-vs-Median disparity and legal policy
│   └── 5_Data_Quality_and_Research.py # Data quality audit, literature, and exports
├── research/
│   └── literature_review/     # IEEE corpus audit and research gap analysis
├── scripts/
│   └── run_pipeline.py        # CLI pipeline runner
├── src/
│   ├── analytics/             # Descriptive, language, temporal, policy, & test engines
│   ├── ingestion/             # NYC Open Data API client, pagination, & refresh
│   ├── processing/            # Data cleaning and feature engineering
│   ├── storage/               # Parquet and DuckDB storage managers
│   ├── utils/                 # Logging and metadata tracking
│   └── validation/            # Schema validation and data quality checks
├── tests/                     # 15 automated pytest suites
├── requirements.txt
└── README.md
```

---

## 5. Policy Benchmarks Implemented

| Benchmark | Source Authority | Target Metric | Scope | Official Description |
|:---|:---|:---|:---|:---|
| **OTI Average Goal** | NYC OTI 2024 Language Access Plan | Mean $\le 30.0$ seconds | Spanish, Cantonese, Mandarin, Russian | Goal for average interpreter connection time across four major languages. Does not guarantee individual wait times. |
| **Statutory Review Threshold** | NYC Administrative Code §23-310 | Wait time $\ge 300.0$ seconds | All requested languages | Mandatory 311 review trigger to investigate whether language-identification protocol failure occurred. |

---

## 6. Research Limitations & Governance
1. **Connected Calls Only:** Dataset reflects successfully connected transactions; unrecorded abandoned calls may bias absolute delay estimates.
2. **Observational Bounds:** Differences in connection times across languages do not establish vendor intent or municipal discrimination without staffing and scheduling data.
3. **Statutory Labeling:** Records $\ge 300\text{s}$ must strictly be labeled as reaching the review threshold, not as confirmed protocol failures.
