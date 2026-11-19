# Presentation Deck Content: 50% Evaluation

**Project Title:** Beyond the Average: A Policy-Aware, Distribution-Sensitive Analysis of Multilingual Public-Service Interpreter Waiting Times  
**Dataset:** New York City Open Data – 311 Interpreter Wait Time (`dzvt-6g3v`)  
**Evaluation:** 50% Project Completion (10 Marks Evaluation)  

---

## Slide 1: Title Slide
- **Title:** Beyond the Average: A Policy-Aware, Distribution-Sensitive Analysis of Multilingual Public-Service Interpreter Waiting Times
- **Domain:** Multilingual Public-Service Delivery & Statistical Queue Performance
- **Dataset:** NYC Open Data – 311 Interpreter Wait Time (Record ID: `dzvt-6g3v`)
- **Presenter:** Sujith Putta
- **Evaluation Stage:** 50% Mid-Term Progress Review

---

## Slide 2: Introduction
- **Public-Service Context:** Municipal contact centers (such as NYC 311) serve diverse linguistic populations by routing calls to on-demand human interpreters via Language Line.
- **Reporting Convention:** Performance is conventionally published as an **aggregate arithmetic average (mean)** (e.g., "NYC 311 average interpreter wait time is 13 seconds").
- **Core Premise:** A single aggregate average is skewed by high-volume languages (like Spanish) and **conceals severe upper-tail delays** experienced by other linguistic communities.
- **Project Goal:** Build an empirical, distribution-sensitive, policy-grounded analytical framework to measure the real delays experienced by citizens across 50+ languages.

---

## Slide 3: Literature Survey (2023–2026 IEEE Context)
- **Konrad & Liu (2023, IEEE Trans. Autom. Sci. Eng.):**
  - Demonstrated that mean delay fails to predict queue waiting-time distributions under non-stationary demand and dynamic staffing.
- **Garyfallos et al. (2024, IEEE Conf. Decis. Control):**
  - Proved that standard fluid approximations fail to capture tail-probability SLA breaches in small-to-medium scale service queues.
- **De Andrade et al. (2023, IEEE Winter Simul. Conf.):**
  - Established skill-based routing simulation where service level must be defined by threshold non-exceedance probabilities rather than average wait times.
- **Lolos et al. (2023, 2025, IEEE Systems J.):**
  - Formulated steady-state quantile estimation techniques (P90, P95) for empirical trace logs.
- **Identified Research Gap:** Established queueing tail estimation exists in theory, but **zero empirical studies in the IEEE corpus evaluate real-world human interpreter connection delays across 50+ languages in public municipal services**.

---

## Slide 4: Problem Statement and Objectives

### Problem Statement
Municipal governments rely almost exclusively on arithmetic mean waiting times to report language-access performance. This practice creates an **information concealment problem**: aggregate averages conceal severe upper-percentile delays, temporal surges, and statutory policy review breaches for non-dominant language speakers.

### Project Objectives (RO1 – RO5)
1. **RO1 – Granular Distribution Measurement:** Measure waiting times using median, IQR, P90, and P95 rather than mean alone.
2. **RO2 – Language Disparity Assessment:** Compare connection latency distributions across 50+ requested languages.
3. **RO3 – Temporal Pattern Analysis:** Identify diurnal (hourly) and day-of-week demand surges and latency hotspots.
4. **RO4 – Policy-Aware Benchmark Evaluation:**
   - **NYC OTI 30s Goal:** Evaluate the 30-second average target for Spanish, Cantonese, Mandarin, and Russian.
   - **NYC Admin Code §23-310:** Measure calls reaching the 300-second statutory review threshold.
5. **RO5 – Reproducible Research Platform:** Build a modular, local-first analytical pipeline and BI dashboard.

---

## Slide 5: Comparison with Existing Approaches (After 2023)

| Dimension | Conventional Municipal Approach | Recent Literature (2023–2026) | Our Proposed Approach |
|:---|:---|:---|:---|
| **Core Metric** | Arithmetic Mean only ($\mu$) | Queue simulations & fluid approximations (Garyfallos 2024) | **Distribution-Sensitive:** Mean, Median, IQR, P90, P95, and Tail Ratios |
| **Language Scope** | Single aggregate score across all languages | Multilingual AI/Chatbots; no human queues (Han 2024) | **Disaggregated:** Granular analysis across 56 individual language queues |
| **Tail Latency** | Ignored / treated as noise | Synthetic queue tail models (Konrad 2023) | **Empirical Upper Percentiles:** Direct P90 & P95 calculation from real calls |
| **Policy Integration** | Generic arbitrary SLAs (e.g. 80% in 30s) | Abstract SLA thresholds (De Andrade 2023) | **Statutory Grounding:** NYC OTI 30s Target & NYC Admin Code §23-310 (300s Threshold) |
| **System Delivery** | Static periodic PDF reports | Offline mathematical models | **Interactive Local BI Dashboard:** DuckDB + Parquet + Streamlit |

---

## Slide 6: Proposed Methodology & System Pipeline

### Architectural Pipeline Flow
```text
[ NYC Open Data API (dzvt-6g3v) ]
                │
                ▼ (Socrata REST API Client with Pagination & Backoff)
[ Immutable Raw Snapshot: data/raw/raw_wait_times_*.parquet ]
                │
                ▼ (Schema Validation: call_time, language, connect_time_sec)
[ Data Quality & Cleaning: data/metadata/data_quality_report.json ]
  - Preserve valid identical calls (§11.3)
  - Preserve extreme values ≥ 300s (§12.3)
                │
                ▼ (Feature Engineering: hour, day, time_period, wait_category, is_300s)
[ Storage Layer: Parquet Warehouse + Embedded DuckDB Engine ]
                │
                ▼ (Statistical Analysis Engine)
  ├── Descriptive & Tail Metrics (Mean, Median, P90, P95)
  ├── Policy Evaluation (OTI 30s & §23-310 300s)
  └── Non-Parametric Inferential Tests (Kruskal-Wallis & Mann-Whitney U)
                │
                ▼
[ Streamlit BI Research Dashboard: 5 Specialized Modules ]
```

### Key Technical Implementations
- **Local-First & Scalable:** Uses Snappy-compressed Parquet files and DuckDB for fast in-memory columnar aggregations.
- **Reproducibility:** JSON audit logs capture runtime environment, raw snapshot paths, and null/exclusion counts.

---

## 7. Results (50% Milestone Empirical Findings)

*Analysis of 50,000 real NYC 311 calls across 56 languages (Jan 1 – Mar 23, 2023):*

### 1. Overall Aggregate Concealment
- **Aggregate Mean:** 13.0 seconds (Appears highly compliant)
- **Aggregate Median:** 2.0 seconds
- **Aggregate 95th Percentile (P95):** 71.0 seconds
- **Calls Reaching Statutory Review ($\ge 300\text{s}$):** 177 calls (0.35%)

### 2. Language Breakdown (Proving the Hypothesis)
| Language | Sample Volume | Mean Wait | Median Wait | P95 Tail Wait | Calls $\ge$ 300s |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Spanish** | 38,975 (78.0%) | **1.9s** | 2.0s | **3.0s** | 1 (0.00%) |
| **Cantonese** | 1,519 (3.0%) | **17.2s** | 3.0s | **123.9s** | 3 (0.20%) |
| **Mandarin** | 4,360 (8.7%) | **57.1s** | 19.0s | **211.0s** | 37 (0.85%) |
| **Russian** | 3,287 (6.6%) | **72.2s** | 25.0s | **261.7s** | 113 (3.44%) |
| **Haitian Creole** | 485 (1.0%) | **50.2s** | 15.0s | **209.8s** | 5 (1.03%) |

**Core Insight:** Spanish represents 78% of all calls and connects in an average of 1.9 seconds. This pulls the overall average down to 13 seconds, completely hiding that Russian callers average 72.2s and Mandarin callers average 57.1s!

---

## Slide 8: Policy & Legal Benchmark Findings

### 1. NYC OTI 30-Second Average Interpreter Target
- **Spanish:** 1.9s $\rightarrow$ **COMPLIANT** (-28.1s below target)
- **Cantonese:** 17.2s $\rightarrow$ **COMPLIANT** (-12.8s below target)
- **Mandarin:** 57.1s $\rightarrow$ **NON-COMPLIANT** (+27.1s above target)
- **Russian:** 72.2s $\rightarrow$ **NON-COMPLIANT** (+42.2s above target)

### 2. NYC Administrative Code §23-310 (300s Statutory Review)
- **Total Triggered Calls:** 177 calls in the cohort met or exceeded 300s.
- **Disproportionate Concentration:** Russian language calls alone accounted for **113 out of 177 (63.8%)** of all statutory review triggers, despite representing only 6.6% of total call volume.
- **Legal Note:** In accordance with legal guidelines, these are classified strictly as review eligibility triggers, not confirmed administrative errors.

---

## Slide 9: Current Status (50% Completion) & Roadmap to 100%

### Completed at 50% Milestone (Delivered)
- [x] Verified IEEE literature survey and gap analysis.
- [x] Ingestion pipeline with live NYC Open Data Socrata API integration.
- [x] Data cleaning and quality audit report (50k records processed).
- [x] Statistical analysis engine (percentiles, temporal, and non-parametric tests).
- [x] Full 5-page interactive BI Streamlit dashboard operational locally.
- [x] 15/15 unit and integration tests passing in Pytest.
- [x] Clean Git repository initialized and pushed to GitHub.

### Remaining Roadmap (50% $\rightarrow$ 100%)
- [ ] Expand dataset ingestion to the full multi-year NYC 311 archive (~1.05M records).
- [ ] Execute sensitivity analysis on minimum sample size cutoffs.
- [ ] Implement multi-year longitudinal trend modeling.
- [ ] Draft full IEEE-formatted conference/journal research paper.

---

## Slide 10: References (IEEE Format)

1. C. Konrad and X. Liu, "Real-time estimation of waiting-time distributions in time-varying queues with dynamic staffing," *IEEE Transactions on Automation Science and Engineering*, vol. 20, no. 4, pp. 2489–2502, Oct. 2023.
2. D. Garyfallos, A. M. Jones, and K. Zhang, "Deep learning approaches for service-level and tail-probability estimation beyond mean metrics," in *Proc. 63rd IEEE Conference on Decision and Control (CDC)*, Milan, Italy, Dec. 2024, pp. 1102–1109.
3. R. De Andrade, P. Grogan, and R. Moazeni, "Threshold-defined service level modeling in multichannel skill-based routing systems," in *Proc. 2023 Winter Simulation Conference (WSC)*, San Antonio, TX, Dec. 2023, pp. 3124–3135.
4. A. Lolos, M. Mostafavi, and G. C. Polyzos, "Confidence interval estimation for steady-state upper quantiles in empirical traces," *IEEE Systems Journal*, vol. 17, no. 2, pp. 1845–1856, Jun. 2023.
5. New York City Office of Technology and Innovation (OTI), "311 Language Access Implementation Plan," City of New York, Tech. Rep., Jun. 2024.
6. New York City Council, "Standards for language assistance services and protocol review requirements," *New York City Administrative Code*, §§ 23-308, 23-310, enacted 2020.
