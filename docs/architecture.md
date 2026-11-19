# Beyond the Average: System Architecture

## 1. Architectural Principles
The Beyond the Average platform implements a local-first, modular, reproducible analytical architecture adhering to PRD Section 10:
- **Local-First & Cloud-Independent:** Operates entirely locally with DuckDB and Parquet storage; requires zero cloud databases or external hosting.
- **Strict Layer Decoupling:** Ingestion, schema validation, data quality auditing, feature engineering, statistical analysis, and Streamlit presentation layers are strictly separated.
- **Reproducibility by Design:** Every dataset acquisition snapshots raw data, preserves exact records (including identical triplet occurrences and extreme delays), and documents environment parameters.

## 2. Component Pipeline Diagram

```
           NYC Open Data API (dzvt-6g3v)
                         │
                         ▼
             [src/ingestion/api_client.py]
             [src/ingestion/pagination.py]
                         │
                         ▼
            data/raw/raw_wait_times_*.parquet (Unmodified Snapshot)
                         │
                         ▼
             [src/validation/schema.py]
             [src/validation/quality_checks.py]
                   │                   │
                   ▼                   ▼
    data/metadata/quality_report.json  [src/processing/cleaning.py]
                                       [src/processing/features.py]
                                                 │
                         ┌───────────────────────┴───────────────────────┐
                         ▼                                               ▼
         data/processed/interpreter_wait_times.parquet       data/analytics/interpreter_analytics.duckdb
                         │                                               │
                         └───────────────────────┬───────────────────────┘
                                                 ▼
                                     Statistical Analysis Engine
                                     ├── src/analytics/descriptive.py
                                     ├── src/analytics/language_analysis.py
                                     ├── src/analytics/temporal_analysis.py
                                     ├── src/analytics/distribution_analysis.py
                                     ├── src/analytics/policy_analysis.py
                                     └── src/analytics/statistical_tests.py
                                                 │
                                                 ▼
                                       Streamlit Presentation
                                     ├── app.py (Global Filters)
                                     ├── pages/1_Overview.py
                                     ├── pages/2_Language_Analysis.py
                                     ├── pages/3_Temporal_Analysis.py
                                     ├── pages/4_Distribution_and_Policy.py
                                     └── pages/5_Data_Quality_and_Research.py
```

## 3. Storage Architecture
- **Raw Layer (`data/raw/`):** Immutable, timestamped Parquet snapshots of raw API outputs.
- **Processed Layer (`data/processed/`):** Cleaned, normalized, and feature-enriched Parquet tables compressed with Snappy.
- **Analytical Layer (`data/analytics/`):** Embedded DuckDB database providing SQL-backed analytical caching and querying.
- **Metadata Layer (`data/metadata/`):** JSON audit logs tracking environment versions, data quality, and retrieval timestamps.
