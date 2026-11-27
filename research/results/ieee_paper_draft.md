# Beyond the Average: A Policy-Aware, Distribution-Sensitive Analysis of Multilingual Public-Service Interpreter Waiting Times

**Author:** Sujith Putta  
**Target Format:** IEEE Conference / Journal Manuscript Draft (Phase 7)

---

## Abstract
Municipal telephone services rely heavily on aggregate arithmetic mean waiting times to report language-access performance. However, in multilingual public-service contact centers, high-volume language queues can mask prolonged upper-tail delays in less-requested languages. This paper presents *Beyond the Average*, a reproducible, policy-aware empirical investigation of `1,061,097` connected interpreter call records across `112` languages from New York City's 311 system (`2023–2026`). Combining distribution-sensitive metrics (median, P90, P95, confidence intervals), non-parametric hypothesis testing, and municipal legal benchmarks—the NYC Office of Technology and Innovation (OTI) 30-second average goal and NYC Administrative Code §23-310's 300-second statutory review threshold—we demonstrate that aggregate reporting conceals substantial tail disparities. While the citywide mean wait is `8.78s` (95% CI: `[8.73, 8.84]`) and median wait is `3.0s`, languages with nearly identical means (e.g., Turkish `24.26s` vs. Yiddish `20.23s`) exhibit a `109.0s` divergence at the 95th percentile (`169.0s` vs. `60.0s`). Furthermore, longitudinal sensitivity analysis shows that aggregate multi-year compliance with the 30-second goal masked 2023 non-compliance in Russian (`34.19s` mean) and ongoing upper-tail delays (`1,652` calls reaching $\ge 300\text{s}$).

---

## I. Introduction
Public-service telephone systems such as New York City 311 serve linguistically diverse populations by connecting callers to live human interpreters. Operational performance is conventionally summarized using aggregate mean waiting times. Prior queueing literature establishes that arithmetic means fail to capture tail probabilities and service-level breaches in non-stationary queues [1], [2]. Yet, empirical studies examining real-world human interpreter connection delays across dozens of languages in municipal government remain absent from the 2023–2026 IEEE corpus.

This study addresses four research questions using NYC Open Data (`dzvt-6g3v`):
- **RQ1:** How do waiting-time distributions differ across requested languages?
- **RQ2:** What temporal patterns emerge across years, months, weekdays, and hours?
- **RQ3:** To what extent does mean-only reporting conceal upper-percentile delays?
- **RQ4:** How do observed waiting times compare against the NYC OTI 30s goal and §23-310 300s review threshold?

---

## II. Related Work
Recent IEEE literature (2023–2026) demonstrates the inadequacy of mean-only queue reporting. Konrad and Liu [1] developed real-time waiting-time distribution estimation for time-varying queues, showing sensitivity to staffing dynamics. Garyfallos et al. [2] proved that fluid approximations fail to capture upper-tail service-level breaches. De Andrade et al. [3] modeled skill-based routing using threshold non-exceedance probabilities, and Lolos et al. [4] established fixed-sample quantile confidence interval estimation (P90, P95). While Han et al. [5] examined LLM-assisted digital government services, none of these studies empirically analyze human interpreter connection latency across `100+` languages in municipal 311 operations.

---

## III. Methodology & Data Pipeline
We designed a reproducible, local-first pipeline acquiring `1,061,195` raw records from NYC Open Data (`dzvt-6g3v`, Jan 2023 – Oct 2026). After schema validation and exclusion of `98` records with missing `language` or `call_time` fields, `1,061,097` validated records were retained. Following strict data integrity rules, `13,160` identical `(call_time, language, connect_time_sec)` triplet rows (legitimate concurrent calls) and all `1,652` extreme delays ($\ge 300\text{s}$, max `2,278.0s`) were preserved without deletion or winsorization.

Records are persisted in Snappy-compressed Parquet and queried via DuckDB. Distribution metrics include Mean, Median, IQR, P90, P95, 95% confidence intervals (Normal/t for means, bootstrap for quantiles, Wilson score for proportions), Kruskal-Wallis $H$-tests with $\epsilon^2$ effect sizes, and sensitivity analyses across sample-size cutoffs ($k \in \{30, 50, 100, 500, 1000\}$) and calendar years (`2023–2026`).

---

## IV. Empirical Results

### A. Overall & Language-Wise Distributions (RQ1)
Citywide, the mean wait is `8.78s` (95% CI: `[8.73, 8.84]`), median is `3.0s`, P90 is `9.0s`, and P95 is `25.0s`. However, Spanish represents `69.68%` of all calls (`N = 739,417`, Mean `4.32s`, P95 `8.0s`), heavily skewing citywide averages. In contrast, Mandarin (`N = 124,123`, Mean `20.92s`, P95 `150.0s`), Russian (`N = 81,992`, Mean `19.12s`, P95 `98.0s`), Haitian Creole (`N = 17,972`, Mean `27.95s`, P95 `163.0s`), and Korean (`N = 9,204`, Mean `23.98s`, P95 `153.0s`) exhibit pronounced upper tails. A Kruskal-Wallis test across the top 10 languages (`N = 1,044,697`) confirms significant distributional differences ($H = 65,444.25$, $p < 0.0001$, $\epsilon^2 = 0.0626$).

### B. Concealment Under Mean-Only Reporting (RQ3)
Comparing languages with similar means ($\Delta \mu \le 5.0\text{s}$, $N \ge 100$) reveals substantial upper-tail divergence:
- **Turkish vs. Yiddish:** Mean `24.26s` vs. `20.23s` ($\Delta = 4.03\text{s}$), but P95 `169.0s` vs. `60.0s` ($\Delta = 109.0\text{s}$).
- **Mandarin vs. Dari:** Mean `20.92s` vs. `16.87s` ($\Delta = 4.05\text{s}$), but P95 `150.0s` vs. `57.4s` ($\Delta = 92.6\text{s}$).
- **Hindi vs. Romanian:** Mean `28.37s` vs. `23.97s` ($\Delta = 4.40\text{s}$), but P95 `196.0s` vs. `104.3s` ($\Delta = 91.7\text{s}$).

### C. Temporal Sensitivity & Policy Benchmarks (RQ2, RQ4)
Over the full 2023–2026 period, all four OTI-designated languages meet the 30s average target (Spanish `4.32s`, Cantonese `9.38s`, Russian `19.12s`, Mandarin `20.92s`). However, year-by-year disaggregation shows Russian exceeded the target in 2023 (`34.19s` mean) before improving in 2024–2026 (`16.31s`, `7.69s`, `12.09s`). Meanwhile, `1,652` calls (`0.16%`) reached the §23-310 300-second statutory review threshold (mean `420.48s` within the threshold cohort), with Russian (`467` calls) and Mandarin (`266` calls) accounting for `44.4%` of all review triggers.

---

## V. Limitations & Conclusion
This observational study analyzes connected calls only; abandoned attempts, staffing levels, and §23-310 review outcomes are not present in the public dataset, precluding causal or discrimination claims. By moving beyond aggregate averages to distribution-sensitive and policy-aware metrics, municipal agencies can identify hidden tail latency and improve equitable language-access monitoring.

---

## References
[1] K. Konrad and Y. Liu, "Real-Time Estimations for the Waiting-Time Distribution in Time-Varying Queues," in *Proc. 2023 Winter Simulation Conference (WSC)*, pp. 315–326, Dec. 2023. DOI: `10.1109/wsc60868.2023.10407204`  
[2] S. Garyfallos, Y. Liu, P. Barlet-Ros, and A. Cabellos-Aparicio, "Service Level Prediction in Non-Markovian Nonstationary Queues: A Simulation-Based Deep Learning Approach," in *Proc. 2024 Winter Simulation Conference (WSC)*, pp. 2655–2666, Dec. 2024. DOI: `10.1109/wsc63780.2024.10838828`  
[3] R. C. De Andrade, P. T. Grogan, and S. Moazeni, "Simulation Assessment of Data-Driven Channel Allocation and Contact Routing in Customer Support Systems," *IEEE Open Journal of Systems Engineering*, vol. 1, pp. 50–59, 2023. DOI: `10.1109/ojse.2023.3265435`  
[4] A. Lolos, C. Alexopoulos, D. M. Goldsman, K. D. Dingeç, A. C. Mokashi, and J. R. Wilson, "A Fixed-Sample-Size Method for Estimating Steady-State Quantiles," in *Proc. 2023 Winter Simulation Conference (WSC)*, pp. 457–468, Dec. 2023. DOI: `10.1109/wsc60868.2023.10407872`  
[5] J. Han, J. Lu, Y. Xu, J. You, and B. Wu, "Intelligent Practices of Large Language Models in Digital Government Services," *IEEE Access*, vol. 12, pp. 8633–8640, 2024. DOI: `10.1109/access.2024.3349969`
