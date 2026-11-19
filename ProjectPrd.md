# PRODUCT REQUIREMENTS DOCUMENT (PRD)

# Beyond the Average
## A Policy-Aware, Distribution-Sensitive Analysis of Multilingual Public-Service Interpreter Waiting Times

**Version:** 1.0 – Final PRD  
**Document Type:** Research Project and Software Product Specification  
**Research Domain:** Multilingual Public-Service Delivery, Interpreter Services, Waiting-Time Analysis  
**Primary Dataset:** NYC Open Data – 311 Interpreter Wait Time  
**Application Type:** Local Research Analytics Platform  
**Target:** Final-Year Undergraduate Research Project and Potential Academic Publication

---

# 1. Executive Summary

## 1.1 Project Overview

Beyond the Average is a data-driven research project that investigates interpreter connection waiting times in multilingual public-service environments.

The project uses the New York City 311 Interpreter Wait Time dataset to examine how waiting times vary across requested languages and temporal periods, whether average-based reporting conceals prolonged delays, and how observed waiting times relate to relevant public-service language-access policy benchmarks.

The project will combine statistical analysis, distribution-sensitive measurement, temporal comparisons, and policy-aware assessment into a reproducible research workflow.

An interactive local application will support data exploration and communicate the research findings. However, the application's dashboard is not the primary research contribution. The central contribution is the empirical investigation of multilingual interpreter waiting-time patterns using established analytical methods in a specific public-service context.

## 1.2 Problem Statement

Public-service interpreter waiting times are commonly summarized using aggregate performance measurements. However, averages alone may conceal differences in waiting-time distributions, prolonged delays, and temporal variations across requested languages.

There is a need to investigate multilingual interpreter connection waiting times using distribution-sensitive and policy-aware measurements to understand patterns that may not be visible through average-based reporting.

## 1.3 Proposed Solution

Develop a reproducible analytical framework that:

1. Collects and validates public interpreter waiting-time records.
2. Measures waiting-time distributions across requested languages.
3. Examines temporal variations in interpreter waiting times.
4. Identifies prolonged waiting-time patterns.
5. Compares average waiting times against applicable policy goals.
6. Measures the frequency of records reaching policy-defined review thresholds.
7. Examines the additional information revealed by distribution-sensitive metrics compared with average-only reporting.
8. Presents the findings through a locally running interactive research application.

---

# 2. Research Background and Motivation

## 2.1 Research Context

The project's initial literature survey covers research published between 2023 and 2026 and identifies three closely related research areas:

- Queueing and service-delay analysis.
- Multilingual communication and language-access systems.
- Public-service performance measurement.

The preliminary survey indicates that waiting-time distribution analysis, percentile estimation, service-level measurement, and temporal queue analysis are established methodological areas.

However, the reviewed literature appears to contain limited direct empirical work on human interpreter connection waiting times in multilingual public-service telephone systems.

This creates a potential research opportunity: applying established waiting-time measurement methods to a public-service interpreter dataset and examining language-specific and temporal patterns.

**Literature-review qualification:** The uploaded Consensus survey is a starting point, not a final verified IEEE-only evidence corpus. Some of its references are published outside IEEE, and its reported search totals do not reconcile clearly with its displayed bibliography. Before making publication claims, the references must be checked individually against IEEE Xplore. The project must not claim that no previous research exists until this verification is complete.

## 2.2 Research Motivation

Averages can hide meaningful differences in service performance.

Consider two hypothetical language groups:

| Measurement | Language A | Language B |
|---|---:|---:|
| Mean waiting time | 25 sec | 25 sec |
| Median waiting time | 20 sec | 12 sec |
| P90 waiting time | 38 sec | 95 sec |
| P95 waiting time | 45 sec | 180 sec |

Both groups have the same average, but their upper-tail waiting-time patterns differ considerably.

The example is illustrative, not an actual result from the NYC dataset.

This project investigates whether similar differences exist in the real data and whether conventional average-based reporting conceals important patterns.

## 2.3 Potential Research Contribution

The proposed contribution is a reproducible empirical analysis combining:

- Language-specific waiting-time distributions.
- Temporal waiting-time variations.
- Upper-percentile and prolonged-wait measurements.
- Policy-aware assessment.
- Comparison of average-only and distribution-sensitive reporting.

The contribution should be described as an application and empirical investigation of established analytical methods in a specific domain unless the verified literature review establishes a stronger form of novelty.

---

# 3. Research Objectives

The project must accomplish the following objectives.

**RO1 – Measure interpreter waiting times**

Analyze individual interpreter connection waiting-time records using descriptive and distribution-sensitive statistics.

**RO2 – Investigate language-wise differences**

Compare waiting-time distributions across requested languages and identify differences in typical and prolonged waiting times.

**RO3 – Investigate temporal patterns**

Examine variations across hours, weekdays, months, and other meaningful temporal groupings.

**RO4 – Examine hidden waiting-time behaviour**

Determine how much information is concealed when service performance is represented only through average waiting times.

**RO5 – Incorporate policy context**

Evaluate observed average waiting times against relevant language-access goals and identify records reaching statutory review thresholds.

**RO6 – Ensure reproducibility**

Build a transparent data-ingestion, cleaning, analysis, and reporting workflow that allows the research to be reproduced.

**RO7 – Communicate research findings**

Provide an interactive local application to explore results without presenting visualization itself as the primary scientific contribution.

---

# 4. Research Questions

The following research questions define the analytical scope.

### RQ1 – Language-wise waiting-time differences

How do interpreter waiting-time distributions differ across requested languages, and how do those differences change across temporal periods?

**Measurements:** Mean, median, P90, P95, standard deviation, IQR, and prolonged-wait frequency.

### RQ2 – Temporal variations

What temporal patterns can be observed in interpreter waiting times across different hours, weekdays, and months?

**Measurements:** Hourly and weekday distributions, monthly trends, temporal percentile changes, and long-wait frequencies.

### RQ3 – Limitations of average-based reporting

To what extent does mean-only reporting conceal differences in upper-percentile waiting times and prolonged delays across languages and temporal periods?

**Measurements:** Differences between mean and median, P90/P95 comparisons, and the percentage of calls reaching 300 seconds or more.

### RQ4 – Policy-aware service assessment

How do observed average interpreter waiting times compare with NYC's stated language-access goal, and how frequently do observed calls reach the statutory 300-second review threshold?

**Measurements:** Language-specific average waiting times for the four languages covered by the stated goal, together with counts and proportions of records at or above 300 seconds.

### Research Question Constraints

- All questions must be answerable using the available dataset.
- No causal conclusions should be made without additional explanatory variables.
- Language differences must not automatically be interpreted as discrimination.
- Statistical significance must be accompanied by effect sizes and practical interpretation.
- The final questions may be refined after the literature review and dataset validation.

---

# 5. Data Source and Dataset Specification

## 5.1 Primary Dataset

**Dataset:** NYC Open Data – 311 Interpreter Wait Time

Official source:

https://data.cityofnewyork.us/City-Government/311-Interpreter-Wait-Time/dzvt-6g3v

**Dataset ID:** `dzvt-6g3v`

**API endpoint:**

`https://data.cityofnewyork.us/resource/dzvt-6g3v.json`

The dataset contains interpreter waiting-time records from people requesting language interpretation during calls to NYC 311.

The currently available dataset metadata reports approximately 1.05 million records and three columns. Its stated update frequency is monthly, generally around the middle of the month for the previous month's data.

Each row represents a unique 311 call that connects to a Language Line interpreter.

## 5.2 Confirmed Dataset Fields

| Field | Type | Description |
|---|---|---|
| `call_time` | Floating timestamp | Date and time associated with the 311 interpreter call record |
| `language` | Text | Requested interpretation language |
| `connect_time_sec` | Number | Waiting time in seconds for connection to a Language Line interpreter |

These are the three documented API field names.

The development team must inspect the latest data dictionary and API metadata before implementing timestamp interpretation, filtering, or transformations.

## 5.3 Important Dataset Characteristics

1. The dataset is available at the individual connected-call record level.
2. The dataset covers interpreter calls that successfully connected to Language Line.
3. It does not provide a complete record of unsuccessful or abandoned interpretation requests.
4. It does not provide caller demographics or a direct explanation for delays.
5. It does not provide interpreter availability, staffing levels, or queue capacity.
6. It does not establish why a particular call experienced a long waiting time.

The analysis must therefore be framed as an investigation of observed connected-call waiting times, not a complete assessment of every interpreter request.

## 5.4 Dataset Validation Requirements

Before full implementation:

- Confirm the latest API schema.
- Download and inspect the official data dictionary.
- Confirm timestamp semantics and timezone interpretation.
- Confirm the meaning and numeric range of `connect_time_sec`.
- Inspect language labels and variations.
- Check missing and invalid values.
- Confirm date coverage.
- Record the source's last-updated metadata.
- Verify whether historical records can change between monthly releases.

The actual date range and record count must be calculated from the downloaded data. They must never be hardcoded.

## 5.5 Timestamp Handling

The `call_time` field is documented as a floating timestamp.

The application must not automatically assume it is UTC or New York local time.

The source data dictionary and metadata must determine the appropriate interpretation.

Until that is confirmed:

- Preserve the raw timestamp.
- Avoid inappropriate timezone conversion.
- Do not make unsupported local-time claims.
- Document the selected interpretation in the processing metadata.

Once validated, use a consistent timezone configuration for all temporal analysis.

---

# 6. Policy and Benchmark Integration

Policy context is an important part of the research and must be implemented accurately.

Two separate policy references are relevant.

## 6.1 The 30-Second Average Interpreter Goal

The NYC Office of Technology and Innovation's 2024 Language Access Implementation Plan states a goal of ensuring that the average time to obtain a telephonic interpreter is 30 seconds or less for:

- Spanish
- Cantonese
- Mandarin
- Russian

This is an average waiting-time goal for the four specified languages.

It is not a guarantee that every individual call will connect within 30 seconds.

### Implementation

For these four languages:

- Calculate average waiting time.
- Display the 30-second reference goal.
- Show the difference between the observed average and the reference goal.
- Show the selected analysis period.
- Show the number of records included.
- Allow comparisons across temporal periods.

For other languages, do not apply the four-language goal as though it were a universal target.

The application must describe the comparison as an observed-data comparison against a stated policy goal, not an official compliance certification.

**Important distinction:** NYC's separate requirement to answer 80% of all 311 calls within 30 seconds is not the interpreter waiting-time goal. These metrics must never be combined.

## 6.2 The 300-Second Statutory Review Threshold

NYC Administrative Code §23-310 specifies that when an interpreter-request call has a waiting time of 300 seconds or longer, 311 must review the call to determine whether the delay resulted from a failure of its language-identification protocol.

### Implementation

Calculate:

- Number of calls with waiting time greater than or equal to 300 seconds.
- Percentage of observed connected calls with waiting time greater than or equal to 300 seconds.
- Language-wise counts and percentages.
- Temporal distribution of these records.
- Waiting-time distributions for records below and at or above the threshold.

Use the label:

**300-Second Statutory Review Threshold**

Never label these records automatically as:

- Protocol failures.
- Confirmed service violations.
- Discrimination incidents.
- Interpreter errors.

The dataset does not contain the outcome of the legally required review or the reason for the delay.

## 6.3 Policy Source References

- NYC Administrative Code §23-308: https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCadmin/0-0-0-155381
- NYC Administrative Code §23-310: https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCadmin/0-0-0-155398
- NYC OTI 2024 Language Access Implementation Plan: https://www.nyc.gov/assets/oti/downloads/pdf/about/oti-311-language-access-plan-2024.pdf

All policy values must be configurable through a documented policy configuration file rather than embedded repeatedly in chart code.

---

# 7. Scope and Non-Goals

## 7.1 In Scope

- NYC 311 interpreter waiting-time analysis.
- Data ingestion through the official public dataset.
- Local storage and incremental refresh.
- Data cleaning and quality validation.
- Language-wise descriptive analysis.
- Temporal waiting-time analysis.
- Distribution-sensitive statistical analysis.
- Upper-percentile and prolonged-wait assessment.
- Policy benchmark comparison.
- Research-oriented interactive application.
- Reproducible reports and exports.
- Documentation supporting academic research.

## 7.2 Out of Scope

The following are not part of the core project:

- Predicting individual interpreter waiting times.
- Forecasting future interpreter demand.
- Building an actual interpreter booking or routing platform.
- Changing NYC 311 infrastructure.
- Determining the cause of a delay without supporting data.
- Measuring interpreter quality or translation accuracy.
- Identifying individual callers.
- Proving discriminatory treatment.
- Estimating abandoned-call rates from connected-call records.
- Recommending interpreter staffing levels without staffing and demand information.
- Building a cloud-hosted commercial analytics platform.
- Presenting sophisticated machine-learning models as research contributions without a justified research need.

Machine learning and anomaly-detection extensions should only be considered after the core statistical analysis is complete and the literature review demonstrates a genuine need.

---

# 8. Research Methodology and Analytical Framework

The project will follow a retrospective, observational, quantitative research design.

## 8.1 Unit of Analysis

One successfully connected interpreter call recorded in the NYC 311 dataset.

Each observation contains a timestamp, requested language, and interpreter connection waiting time.

## 8.2 Data Processing Workflow

The analytical pipeline must follow this sequence:

1. Retrieve source data.
2. Preserve an unmodified raw snapshot.
3. Validate the source schema.
4. Inspect data quality.
5. Clean and normalize fields.
6. Derive temporal attributes.
7. Generate analytical datasets.
8. Calculate statistical measurements.
9. Perform language and temporal comparisons.
10. Generate policy-related measurements.
11. Produce reproducible analysis outputs.

## 8.3 Core Statistical Measures

Calculate the following:

| Metric | Purpose |
|---|---|
| Count | Number of observed calls |
| Mean | Arithmetic average waiting time |
| Median | Typical midpoint waiting time |
| Minimum | Shortest observed waiting time |
| Maximum | Longest observed waiting time |
| Standard deviation | Variation in waiting times |
| IQR | Spread of the central 50% |
| P90 | Waiting time below which 90% of observations fall |
| P95 | Waiting time below which 95% of observations fall |
| Long-wait count | Number of calls at or above 300 seconds |
| Long-wait percentage | Share of calls at or above 300 seconds |

All metrics must be calculated from the filtered observations and displayed with their corresponding sample counts.

## 8.4 Language-Wise Analysis

For each sufficiently represented language, calculate:

- Call volume.
- Mean waiting time.
- Median waiting time.
- P90.
- P95.
- Standard deviation.
- IQR.
- Percentage of calls at or above 300 seconds.

The application should support comparison between selected languages.

Language rankings must be metric-specific. A language with a lower average is not automatically the language with the lowest P95 or lowest prolonged-wait percentage.

Groups with insufficient sample sizes must be marked as having limited statistical support rather than being ranked confidently.

## 8.5 Temporal Analysis

Extract the following fields after validating timestamp semantics:

- Year.
- Month.
- Date.
- Hour.
- Day of week.
- Week of year, if useful.
- Configurable time-of-day category.

Analyze:

- Hourly waiting-time variations.
- Day-of-week variations.
- Monthly trends.
- Language-wise temporal patterns.
- Changes in upper-percentile waiting times.
- Changes in prolonged-wait frequency.

Temporal comparisons must include sample sizes to prevent periods with low record counts from being misinterpreted.

Time-of-day groupings are analytical categories defined by the project, not official NYC policy categories. Their boundaries must be documented and configurable.

## 8.6 Distribution-Sensitive Analysis

The mean must not be used as the only measurement of interpreter service performance.

Implement:

- Mean versus median comparison.
- P90 and P95 comparisons.
- Histograms.
- Box plots.
- Empirical cumulative distribution functions (ECDF).
- Long-tail distribution inspection.
- Prolonged-wait frequency analysis.

The aim is to identify whether two language groups or periods with similar means have meaningfully different waiting-time distributions.

## 8.7 Inferential Analysis

Where appropriate, conduct statistical comparisons.

Potential methods include:

- Kruskal–Wallis test for multi-language distribution comparisons.
- Appropriate post-hoc pairwise comparisons with multiple-testing correction.
- Mann–Whitney U tests for selected two-group comparisons.
- Confidence intervals for means, medians, percentiles, and threshold proportions.
- Effect-size reporting.
- Sensitivity analysis across time periods and minimum sample sizes.

Method selection must follow data characteristics and research design.

Do not rely on p-values alone. Large datasets can produce statistically significant results for differences that are not practically meaningful.

Report:

- Test used.
- Null hypothesis.
- Sample size.
- Test statistic.
- p-value.
- Effect size where appropriate.
- Confidence interval where available.
- Practical interpretation.

Multiple-comparison procedures must be applied when conducting numerous pairwise tests.

If adjusted regression or quantile regression is added, it must be justified by the research questions and validated against model assumptions.

## 8.8 Call Volume and Demand Interpretation

Call counts may be calculated by language and temporal group.

However, observed connected-call volume is not a complete measure of interpreter demand.

The dataset does not capture all failed or abandoned requests, interpreter staffing, or queue capacity.

Therefore:

- Call volume may be used as a descriptive variable.
- Temporal call volume may be explored alongside waiting times.
- Volume must not be treated as a direct measurement of actual queue load.
- Associations must not be interpreted as causal evidence.
- Resource-allocation recommendations are outside the dataset's evidentiary scope.

---

# 9. Mean-Only Versus Distribution-Sensitive Comparison

This is an important component of the research.

The analysis must directly examine what is visible through average-based reporting and what becomes visible when distribution-sensitive measurements are introduced.

## 9.1 Baseline Method

The baseline represents conventional average-based reporting using:

- Total calls.
- Mean waiting time.
- Mean waiting time by language.
- Mean waiting time by month.
- Mean waiting time by time period.

## 9.2 Proposed Analytical Method

The proposed method adds:

- Median waiting time.
- P90 and P95.
- IQR and standard deviation.
- Long-wait counts and percentages.
- Temporal distribution comparisons.
- Language-wise upper-tail analysis.
- Policy reference measurements.

## 9.3 Comparison Outputs

The research must identify:

1. Languages with similar mean waiting times but different P90/P95 values.
2. Periods where the average appears stable but prolonged waits change.
3. Groups whose ranking changes depending on the selected metric.
4. Differences between overall and language-specific measurements.
5. Policy-relevant patterns that are not visible through averages alone.

This comparison must use actual observations rather than invented demonstrations.

An optional user-based evaluation of dashboard interpretation may be conducted later, subject to institutional approval and participant consent. It is not a prerequisite for the core empirical analysis.

---

# 10. System Architecture

## 10.1 Architecture Principles

The application must be:

- Local-first.
- Modular.
- Reproducible.
- Easy to maintain.
- Independent of cloud infrastructure.
- Separated into ingestion, processing, analysis, and presentation layers.

## 10.2 Recommended Technology Stack

| Layer | Technology | Responsibility |
|---|---|---|
| Programming language | Python | Entire analytical pipeline |
| Application interface | Streamlit | Local interactive application |
| Visualization | Plotly | Interactive statistical charts |
| Data processing | Pandas | Cleaning and transformation |
| Analytical storage | DuckDB | Local analytical queries |
| File storage | Parquet | Efficient processed data storage |
| Statistical analysis | SciPy | Statistical tests and measurements |
| Optional modelling | Statsmodels | Justified regression analysis |
| Testing | Pytest | Unit and integration testing |
| Environment management | Virtual environment and pinned dependencies | Reproducibility |

Do not introduce React, Node.js, cloud databases, or external hosted services unless a future requirement clearly justifies them.

## 10.3 High-Level Data Flow

```text
          NYC Open Data API
                  |
                  v
           Data Ingestion
                  |
                  v
          Raw Data Snapshots
                  |
                  v
        Schema and Data Validation
                  |
                  v
       Cleaning and Transformation
                  |
                  v
          Parquet / DuckDB
                  |
                  v
       Statistical Analysis Engine
                  |
          +-------+-------+
          |               |
          v               v
     Research Metrics   Policy Metrics
          |               |
          +-------+-------+
                  |
                  v
          Streamlit Application
                  |
                  v
       Research Findings and Exports
```

## 10.4 Recommended Project Structure

```text
beyond-the-average/
│
├── app.py
│
├── config/
│   ├── settings.yaml
│   ├── policy_thresholds.yaml
│   └── analysis_config.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── analytics/
│   └── metadata/
│
├── src/
│   ├── ingestion/
│   │   ├── api_client.py
│   │   ├── pagination.py
│   │   └── refresh.py
│   │
│   ├── validation/
│   │   ├── schema.py
│   │   └── quality_checks.py
│   │
│   ├── processing/
│   │   ├── cleaning.py
│   │   └── features.py
│   │
│   ├── analytics/
│   │   ├── descriptive.py
│   │   ├── language_analysis.py
│   │   ├── temporal_analysis.py
│   │   ├── distribution_analysis.py
│   │   ├── statistical_tests.py
│   │   └── policy_analysis.py
│   │
│   ├── storage/
│   │   ├── duckdb_manager.py
│   │   └── parquet_manager.py
│   │
│   └── utils/
│       ├── logging.py
│       └── metadata.py
│
├── pages/
│   ├── 1_Overview.py
│   ├── 2_Language_Analysis.py
│   ├── 3_Temporal_Analysis.py
│   ├── 4_Distribution_and_Policy.py
│   └── 5_Data_Quality_and_Research.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_validation.py
│   ├── test_processing.py
│   ├── test_statistics.py
│   └── test_policy_metrics.py
│
├── research/
│   ├── literature_review/
│   ├── methodology/
│   ├── results/
│   └── references/
│
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── methodology.md
│   └── limitations.md
│
├── requirements.txt
├── README.md
└── .gitignore
```

The implementation agent may adjust the structure if the existing repository already has a suitable architecture. Avoid unnecessary restructuring.

---

# 11. Data Ingestion and Refresh Requirements

## 11.1 Initial Data Acquisition

The first successful execution must:

1. Connect to the official NYC Open Data API.
2. Retrieve the complete available dataset.
3. Handle pagination.
4. Save the raw records locally.
5. Store source metadata.
6. Validate the retrieved record count.
7. Record the download timestamp.
8. Continue to processing only after successful validation.

Use a configurable batch size and implement retries, request timeouts, and error handling.

A full initial download must never be silently replaced by a partial response.

## 11.2 Incremental Refresh

The dataset is updated monthly, but source data may also be corrected.

The refresh workflow must:

- Check available dataset metadata.
- Compare the source version or last-updated information with the local snapshot.
- Skip unnecessary downloads when the source has not changed.
- Refresh affected recent periods when an update is detected.
- Use a documented overlap window for monthly reconciliation.
- Periodically support a complete snapshot refresh.
- Validate the new data before replacing previously valid data.

Do not assume that only the latest month can change.

## 11.3 Duplicate Handling

The documented dataset has three fields and no separate unique record identifier in its published schema.

Identical values across all three fields may represent distinct calls.

Therefore:

- Never remove records simply because their three fields match.
- Preserve the original row count.
- Use snapshot or partition reconciliation for refreshes.
- Document the chosen refresh strategy.
- Do not manufacture unique identifiers and treat them as source-provided IDs.

## 11.4 Offline Behaviour

When the API is unavailable:

- Load the last valid local dataset.
- Display a stale-data notification.
- Preserve the last successful snapshot.
- Log the failed refresh attempt.
- Do not delete or overwrite valid cached records.
- Allow the analytical application to operate offline.

## 11.5 Manual Refresh

Provide a manual **Refresh Dataset** control.

During refresh, display:

- Connection status.
- Download progress where available.
- Source update metadata.
- Validation status.
- Last successful refresh timestamp.
- Failure details when applicable.

Never show a successful refresh status before data has passed validation.

---

# 12. Data Cleaning and Quality Assurance

## 12.1 Schema Validation

Verify that the expected source fields exist:

- `call_time`
- `language`
- `connect_time_sec`

Unexpected schema changes must stop the processing workflow and produce a useful error message.

Do not silently rename arbitrary fields or infer a replacement schema.

## 12.2 Cleaning Rules

- Parse timestamps using the verified source semantics.
- Convert waiting times to a numeric representation.
- Normalize leading/trailing whitespace in language labels.
- Preserve the original language value.
- Identify missing timestamps.
- Identify missing language labels.
- Identify missing waiting-time values.
- Identify non-numeric waiting-time values.
- Flag negative waiting times.
- Inspect unusually large waiting-time values without automatically excluding them.

## 12.3 Outlier Handling

Large waiting times may be important to this research.

Do not delete or winsorize them automatically.

Outlier detection may be used for diagnostic purposes, but every removal must be justified and documented.

Primary research results must retain valid extreme waiting-time observations.

## 12.4 Derived Fields

Create the following analytical fields where supported:

- `year`
- `month`
- `date`
- `hour`
- `day_of_week`
- `week_of_year`
- `time_period`
- `wait_category`
- `is_300s_or_more`

The original source columns must remain available.

`time_period` must use documented project-defined boundaries.

`wait_category` must not imply an official service classification unless supported by a source.

## 12.5 Data Quality Report

Generate a report containing:

- Original record count.
- Valid record count.
- Invalid record count.
- Missing values by field.
- Negative waiting-time records.
- Invalid timestamps.
- Invalid language values.
- Duplicate-value observations without automatic deletion.
- Observed date range.
- Distinct observed languages.
- Minimum and maximum waiting times.
- Source update metadata.
- Processing timestamp.
- Exclusion counts and reasons.

Every exclusion must be traceable.

---

# 13. Application Features and Pages

The application is a research support tool. Its interface should prioritize analytical clarity rather than decorative visualization.

## 13.1 Page 1 – Research Overview

Purpose: Provide an overview of the selected dataset and its measured waiting-time characteristics.

Display:

- Dataset source and refresh status.
- Selected date range.
- Total connected calls.
- Number of observed languages.
- Mean waiting time.
- Median waiting time.
- P90.
- P95.
- Percentage of calls at or above 300 seconds.

Charts:

- Monthly waiting-time trend.
- Language-wise average comparison.
- Distribution summary.
- Long-wait trend.

The overview should make the difference between typical waiting times and prolonged waits immediately understandable.

## 13.2 Page 2 – Language Analysis

Purpose: Investigate differences between requested languages.

Features:

- Language selector.
- Multi-language comparison.
- Call count.
- Mean and median.
- P90 and P95.
- Standard deviation and IQR.
- Long-wait frequency.
- Language-wise distribution comparison.
- Selected-language temporal comparison.

Display sample counts with every comparison.

Avoid definitive rankings for insufficiently represented languages.

## 13.3 Page 3 – Temporal Analysis

Purpose: Understand how waiting times vary over time.

Features:

- Hourly waiting-time analysis.
- Day-of-week comparisons.
- Monthly trends.
- Hour-by-weekday heatmap.
- Language-specific temporal patterns.
- Metric selector for mean, median, P90, and prolonged-wait percentage.

All temporal analysis must use validated timestamp semantics.

## 13.4 Page 4 – Distribution and Policy Analysis

Purpose: Examine hidden waiting-time patterns and relevant policy references.

Include:

- Mean versus median comparison.
- P90 and P95.
- Histograms.
- Box plots.
- ECDF.
- Percentage of calls at or above 300 seconds.
- Number of review-threshold records.
- 30-second average-goal comparison for the four specified languages.

Policy measurements must display the exact benchmark definition, scope, and selected data period.

## 13.5 Page 5 – Data Quality and Research Methodology

Purpose: Make the study transparent and reproducible.

Include:

- Dataset source.
- Source update date.
- Download timestamp.
- Record count.
- Data coverage.
- Schema information.
- Cleaning steps.
- Exclusion report.
- Statistical methodology.
- Policy definitions.
- Known limitations.
- Processing configuration.
- Research question mapping.

This page must explain how displayed results were produced.

---

# 14. Global Filters and Interactions

All analytical pages should share consistent filters.

Required filters:

- Date range.
- Language.
- Day of week.
- Hour or time period.
- Minimum sample count.
- Selected measurement.

Requirements:

- Changes to filters must update dependent metrics and charts.
- Provide a reset-filters option.
- Display the active analysis period.
- Display sample counts.
- Prevent empty filters from producing misleading values.
- Provide clear empty-state messages.
- Allow the user to select multiple languages where relevant.

The selected analysis configuration must be exportable for reproducibility.

---

# 15. Research Findings and Reporting

## 15.1 Evidence-Based Findings

The application may generate concise descriptive observations, but each finding must be supported by actual analytical results.

A finding should contain:

- Observation.
- Language or time period.
- Measurement.
- Sample count.
- Comparison baseline.
- Relevant statistical evidence.
- Interpretation.
- Limitation.

Example format:

"Language A recorded a higher P95 waiting time than Language B over the selected period. The comparison contains N observations for Language A and M observations for Language B. This describes an observed difference and does not establish its cause."

The example is a template, not an actual finding.

## 15.2 Export Capabilities

Allow users to export:

- Filtered records.
- Aggregated statistics.
- Language comparison tables.
- Temporal comparison tables.
- Policy-threshold summaries.
- Data-quality reports.
- Statistical-test results.
- Research figures as PNG.
- Tables as CSV.
- Analysis metadata.

Exports must include the selected date range and relevant measurement definitions.

---

# 16. Non-Functional Requirements

## 16.1 Performance

- The application must handle approximately one million source records.
- Filtering and aggregation should use DuckDB or efficient Pandas workflows.
- Avoid loading and reprocessing raw records unnecessarily.
- Cache reusable analytical results.
- Use Parquet for efficient local storage.
- Keep chart rendering responsive for typical grouped summaries.

## 16.2 Reliability

- Failed downloads must not destroy valid local data.
- Invalid schemas must stop processing.
- Statistical calculations must be tested.
- The application must recover using the last validated dataset.
- Every refresh must be logged.

## 16.3 Reproducibility

Every research output must be associated with:

- Dataset source.
- Source snapshot or last-updated metadata.
- Data retrieval timestamp.
- Processing configuration.
- Analysis configuration.
- Software versions.
- Filter settings.
- Statistical method.
- Relevant code version.

## 16.4 Maintainability

Separate business logic, data processing, statistical analysis, and user-interface code.

Avoid hardcoded analytical results.

All metrics must be calculated from the dataset.

All policy values and analysis boundaries must be configurable.

## 16.5 Accessibility and Usability

- Provide readable chart labels.
- Use clear units, especially seconds.
- Avoid relying on color alone.
- Use consistent language and metric definitions.
- Display explanatory tooltips for statistical measurements.
- Maintain consistent page navigation.
- Make the interface usable on standard desktop screens.

---

# 17. Research Validation and Testing

Validation is required at both the software and research levels.

## 17.1 Software Testing

Test:

- API connectivity.
- Pagination completeness.
- Schema validation.
- Data-type conversion.
- Missing-value detection.
- Invalid waiting-time detection.
- Duplicate-preservation behaviour.
- Timestamp feature extraction.
- Statistical calculations.
- Policy calculations.
- Filter behaviour.
- Export correctness.
- Offline operation.
- Refresh failure handling.

Use synthetic fixtures only for software tests. Never mix synthetic records with the real research dataset.

## 17.2 Statistical Validation

Cross-check core metrics using independent calculations on selected subsets.

Validate that:

- Mean and median are correct.
- Percentiles use a documented calculation convention.
- Group counts reconcile with source records.
- Threshold proportions use the correct denominator.
- Filters do not alter unrelated groups.
- Missing-value exclusions are documented.
- Confidence intervals use an appropriate method.

## 17.3 Research Validation

The research report must document:

- How the dataset was acquired.
- What observations were excluded.
- How metrics were calculated.
- Why particular tests were selected.
- How temporal effects were examined.
- What the policy comparisons mean.
- What the data cannot establish.

The mean-only and distribution-sensitive approaches must be compared on the same observations and the same analysis periods.

Do not claim that the proposed framework is more effective without evidence.

If a user study is later undertaken, define its protocol, participants, tasks, consent, and evaluation metrics separately.

---

# 18. Limitations and Research Ethics

These limitations must be documented in the application and research paper.

1. **Connected-call selection:** The dataset covers calls that successfully connected to an interpreter, not all attempts or abandoned requests.

2. **Limited explanatory variables:** The dataset does not contain interpreter staffing, availability, queue capacity, or operational events.

3. **No caller-level attributes:** The project cannot examine individual caller demographics or personal circumstances.

4. **No causal identification:** Differences in waiting times do not establish why those differences occurred.

5. **No direct discrimination measurement:** Language-wise differences alone do not prove discrimination or unequal treatment.

6. **No review outcomes:** The dataset does not show whether a 300-second threshold record was investigated or what that review concluded.

7. **Timestamp interpretation:** Time-based findings depend on correctly interpreting the source timestamp and its timezone.

8. **Single-city context:** NYC 311 findings should not automatically be generalized to all government interpreter systems.

9. **Missing unsuccessful requests:** Observed call counts are not necessarily the total interpreter-service demand.

No personally identifying information should be inferred or combined with external caller-level data.

The project must use careful language and avoid presenting observational results as causal or legal conclusions.

---

# 19. Implementation Roadmap

Development must proceed in the following phases.

## Phase 0 – Research and Dataset Validation

**Objective:** Lock the research foundation before software implementation.

Tasks:

1. Audit the existing literature survey.
2. Verify publication venue, year, DOI, and IEEE Xplore record for every paper.
3. Exclude non-IEEE sources from the IEEE-only evidence corpus.
4. Resolve inconsistencies between reported search totals and the bibliography.
5. Complete the comparison matrix.
6. Finalize evidence-supported research gaps.
7. Verify the NYC dataset schema.
8. Confirm timestamp semantics.
9. Validate the official policy definitions.
10. Finalize the research questions and statistical analysis plan.

**Exit criteria:** A verified literature-review corpus, validated dataset schema, and approved research methodology.

Do not claim a confirmed IEEE research gap before this phase passes.

## Phase 1 – Repository and Architecture Foundation

**Objective:** Establish the implementation foundation.

Tasks:

- Inspect the existing repository.
- Preserve useful existing code.
- Set up the Python environment.
- Create the modular application structure.
- Configure data directories.
- Add configuration management.
- Set up logging and testing.

**Exit criteria:** Application skeleton runs locally and project dependencies are documented.

## Phase 2 – Dataset Ingestion

**Objective:** Acquire the complete real dataset.

Tasks:

- Implement the NYC Open Data client.
- Implement pagination.
- Add retries and timeout handling.
- Download and preserve the raw dataset.
- Capture source metadata.
- Validate retrieval completeness.
- Add incremental refresh support.

**Exit criteria:** A complete validated raw snapshot is stored locally.

## Phase 3 – Cleaning and Feature Engineering

**Objective:** Prepare a trustworthy analytical dataset.

Tasks:

- Validate source columns.
- Convert data types.
- Handle missing values.
- Preserve valid extreme values.
- Normalize language labels while preserving originals.
- Validate timestamps.
- Derive temporal fields.
- Generate a quality report.

**Exit criteria:** Reproducible processed records and a complete quality report are available.

## Phase 4 – Statistical Analysis Engine

**Objective:** Implement the research methodology independently of the UI.

Tasks:

- Implement descriptive statistics.
- Implement language-wise analysis.
- Implement temporal analysis.
- Implement P90/P95.
- Implement distribution measurements.
- Implement long-wait measurements.
- Implement statistical comparisons.
- Implement policy calculations.
- Add statistical tests.

**Exit criteria:** All analytical calculations pass unit and validation tests.

## Phase 5 – Research Application

**Objective:** Expose the analytical results through the local interface.

Tasks:

- Implement Research Overview.
- Implement Language Analysis.
- Implement Temporal Analysis.
- Implement Distribution and Policy Analysis.
- Implement Data Quality and Research Methodology.
- Add global filters.
- Add exports.
- Implement clear loading and empty states.

**Exit criteria:** All pages display correctly calculated metrics and respond consistently to filters.

## Phase 6 – Research Comparison and Sensitivity Analysis

**Objective:** Establish what is gained by moving beyond mean-only reporting.

Tasks:

- Compare mean-based and distribution-sensitive summaries.
- Identify metric-specific ranking changes.
- Compare long-wait patterns.
- Examine sensitivity to date range and minimum sample size.
- Review findings against the research questions.
- Document statistical and practical significance.

**Exit criteria:** Reproducible results directly addressing the research questions are available.

## Phase 7 – Documentation and Publication Preparation

**Objective:** Prepare the academic research package.

Tasks:

- Finalize verified literature review.
- Document research methodology.
- Generate research tables and figures.
- Document statistical tests.
- Document dataset limitations.
- Write findings and discussion.
- Prepare IEEE-formatted references.
- Prepare reproducibility instructions.
- Draft the paper according to the selected conference or journal's requirements.

**Exit criteria:** The research package is independently understandable and reproducible.

## Phase 8 – Final Quality Assurance

**Objective:** Verify the complete product and research outputs.

Tasks:

- Execute the complete test suite.
- Test first-time data acquisition.
- Test refresh functionality.
- Test offline mode.
- Validate all metrics.
- Verify exports.
- Review all policy labels.
- Check all research claims against evidence.
- Resolve known critical defects.

**Exit criteria:** The application and research documentation satisfy the Definition of Done.

---

# 20. Functional Requirements Summary

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Retrieve complete NYC interpreter waiting-time data | Critical |
| FR-02 | Preserve raw source data | Critical |
| FR-03 | Validate source schema and data quality | Critical |
| FR-04 | Support monthly refresh and local caching | High |
| FR-05 | Calculate descriptive statistics | Critical |
| FR-06 | Compare languages | Critical |
| FR-07 | Analyze temporal patterns | Critical |
| FR-08 | Calculate P90/P95 and long-wait metrics | Critical |
| FR-09 | Implement policy-aware measurements | Critical |
| FR-10 | Perform justified statistical comparisons | High |
| FR-11 | Provide interactive local research pages | High |
| FR-12 | Support CSV and figure exports | High |
| FR-13 | Provide reproducibility metadata | Critical |
| FR-14 | Support offline operation | High |
| FR-15 | Generate data-quality reports | High |

---

# 21. Risks and Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Incorrect literature references | Invalid research-gap claims | Verify every IEEE reference individually |
| Dataset schema changes | Pipeline failure | Schema validation and explicit error handling |
| Timestamp ambiguity | Incorrect temporal conclusions | Verify data dictionary and preserve raw timestamps |
| API pagination failure | Incomplete dataset | Validate record counts and pagination |
| Incorrect duplicate removal | Loss of legitimate calls | Preserve identical source records |
| Extreme values removed | Underestimation of long waits | Preserve valid extreme observations |
| Small language samples | Unstable comparisons | Sample-size warnings and confidence intervals |
| Large sample sizes | Misleading significance | Report effect sizes and practical importance |
| Policy misinterpretation | Invalid conclusions | Separate average goals and statutory review thresholds |
| Overstated novelty | Weak publication defensibility | Complete an IEEE-only literature audit |
| Causal overinterpretation | Unsupported research claims | Restrict conclusions to observed associations |

---

# 22. Final Project Deliverables

The completed project must include:

### A. Research Deliverables

1. Verified 2023–2026 IEEE literature survey.
2. IEEE paper comparison matrix.
3. Evidence-supported research-gap analysis.
4. Final research problem statement.
5. Final research objectives and questions.
6. Statistical methodology.
7. Dataset assessment.
8. Research results.
9. Discussion and limitations.
10. IEEE-formatted reference list.

### B. Software Deliverables

1. Working local research application.
2. NYC Open Data ingestion pipeline.
3. Raw data snapshots.
4. Validated processed dataset.
5. DuckDB and Parquet storage.
6. Statistical analysis modules.
7. Policy measurement modules.
8. Interactive research pages.
9. Export functionality.
10. Unit and integration tests.

### C. Documentation Deliverables

1. README with setup instructions.
2. Architecture documentation.
3. Data dictionary.
4. Data-quality report.
5. Methodology documentation.
6. Reproducibility instructions.
7. Limitations document.
8. Implementation and testing report.

---

# 23. Definition of Done

The project is complete only when all of the following are satisfied.

## Research

- [ ] Literature corpus is verified against IEEE Xplore.
- [ ] Only eligible IEEE papers are counted in the IEEE-only review.
- [ ] Research gaps are supported by evidence.
- [ ] Research questions are measurable using the dataset.
- [ ] Dataset limitations are documented.
- [ ] Policy definitions are verified.
- [ ] The methodology is reproducible.

## Data

- [ ] Complete source data is acquired.
- [ ] Raw data is preserved.
- [ ] Schema validation works.
- [ ] Cleaning rules are documented.
- [ ] Valid extreme values are preserved.
- [ ] Duplicate-value observations are not incorrectly deleted.
- [ ] Timestamp interpretation is verified.
- [ ] Data-quality reporting works.

## Analytics

- [ ] Mean and median are correctly calculated.
- [ ] P90 and P95 are correctly calculated.
- [ ] Language comparisons work.
- [ ] Temporal comparisons work.
- [ ] Long-wait measurements work.
- [ ] Policy comparisons work.
- [ ] Statistical comparisons are validated.
- [ ] Mean-only and distribution-sensitive results can be compared.

## Application

- [ ] All five research pages work.
- [ ] Global filters behave consistently.
- [ ] Sample counts are displayed.
- [ ] Policy benchmarks are correctly labelled.
- [ ] Export functionality works.
- [ ] Offline mode works.
- [ ] Refresh errors do not destroy valid data.

## Publication Preparation

- [ ] Results address the research questions.
- [ ] Findings are backed by actual observations.
- [ ] Interpretations do not exceed what the dataset supports.
- [ ] Figures and tables are reproducible.
- [ ] Limitations are explicitly reported.
- [ ] The manuscript has verified references.

---

# 24. Instructions for AI Coding Agents

The PRD is the source of truth for implementation.

All agents must follow these rules:

1. Inspect the existing repository before changing anything.
2. Do not rewrite working components unnecessarily.
3. Follow the implementation phases in order.
4. Do not bypass Phase 0 research and data validation.
5. Use only the actual NYC Open Data source for research observations.
6. Never generate fake records or fabricated statistical results.
7. Keep raw data unchanged.
8. Do not remove exact duplicate-valued rows automatically.
9. Do not remove legitimate extreme waiting times.
10. Keep the ingestion, cleaning, analytical, storage, and UI layers separate.
11. Do not hardcode computed metrics.
12. Do not assume timestamp timezone semantics.
13. Keep policy definitions in configuration.
14. Use tests for analytical calculations.
15. Do not add machine-learning features without an approved research justification.
16. Do not build cloud infrastructure or external services unnecessarily.
17. Maintain local offline functionality.
18. Record every significant implementation decision.

### Agent Completion Report

At the end of each phase, report:

- Files created.
- Files modified.
- Features implemented.
- Tests executed.
- Test results.
- Data validation results.
- Outstanding issues.
- Known limitations.
- Phase exit-criteria status.

Do not report a phase as complete when critical acceptance criteria are unmet.

---

# 25. Final Research Direction

Beyond the Average is fundamentally a study of multilingual public-service interpreter waiting times.

The project does not attempt to invent new queueing theory or introduce visualization as the primary research contribution.

Instead, it aims to establish a reproducible empirical analysis that investigates whether waiting-time distributions, language-wise differences, temporal variations, and prolonged delays reveal information that conventional average-based reporting does not adequately communicate.

The NYC 311 dataset provides the real-world evidence. Established statistical techniques provide the analytical foundation. Policy definitions provide a relevant interpretation framework. The local application makes the findings accessible and reproducible.

**The central research question is:**

*Are multilingual public-service interpreter waiting times distributed differently across languages and temporal periods, and does relying on average waiting times conceal prolonged delays relevant to service-performance assessment?*

The final scientific contribution must be determined by the verified literature review and actual dataset results—not by assumptions made before the analysis.

**Final project principle: Research first. Evidence second. Analysis third. Application fourth. Publication backed by reproducible results.**