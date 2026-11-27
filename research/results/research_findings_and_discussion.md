# Empirical Research Findings and Discussion (Phase 6 & 7)

**Study:** Beyond the Average: A Policy-Aware, Distribution-Sensitive Analysis of Multilingual Public-Service Interpreter Waiting Times  
**Dataset:** NYC Open Data – 311 Interpreter Wait Time (`dzvt-6g3v`)  
**Coverage:** January 1, 2023 – October 31, 2026 (`N = 1,061,097` validated connected calls; `98` null-field exclusions tracked; `112` distinct languages)

---

## 1. Overall Descriptive & Distribution Summary

Across all 1,061,097 valid connected calls:
- **Arithmetic Mean:** `8.78s` (95% CI: `[8.73, 8.84]`)
- **Median (P50):** `3.0s` (95% CI: `[3.0, 3.0]`)
- **Interquartile Range (IQR):** `2.0s`
- **90th Percentile (P90):** `9.0s` (95% CI: `[9.0, 10.0]`)
- **95th Percentile (P95):** `25.0s` (95% CI: `[25.0, 26.0]`)
- **Maximum Observed Wait:** `2,278.0s` (37.97 minutes)
- **300-Second Statutory Review Threshold (§23-310):** `1,652` calls (`0.156%`, 95% CI: `[0.148%, 0.163%]`)

---

## 2. Findings Mapped to Research Questions (RQ1–RQ4)

### RQ1 – Language-Wise Waiting-Time Differences
*How do interpreter waiting-time distributions differ across requested languages?*

- **Volume Concentration:** Spanish accounts for `739,417` calls (`69.68%` of all validated records) with a mean of `4.32s`, median of `3.0s`, P95 of `8.0s`, and `0.03%` (`219` calls) reaching 300s.
- **Disparities in High-Volume Non-Spanish Queues:**
  - **Mandarin** (`N = 124,123`): Mean `20.92s`, Median `3.0s`, P90 `57.0s`, P95 `150.0s`, `266` calls $\ge 300\text{s}$ (`0.21%`).
  - **Russian** (`N = 81,992`): Mean `19.12s`, Median `3.0s`, P90 `30.0s`, P95 `98.0s`, `467` calls $\ge 300\text{s}$ (`0.57%`).
  - **Haitian Creole** (`N = 17,972`): Mean `27.95s`, Median `8.0s`, P90 `66.0s`, P95 `163.0s`, `54` calls $\ge 300\text{s}$ (`0.30%`).
  - **Korean** (`N = 9,204`): Mean `23.98s`, Median `3.0s`, P90 `64.0s`, P95 `153.0s`, `84` calls $\ge 300\text{s}$ (`0.91%`).
- **Inferential Verification:** A Kruskal-Wallis $H$-test across the top 10 languages (`N = 1,044,697`) confirms statistically significant distributional differences ($H = 65,444.25$, $p < 0.0001$, $\epsilon^2 = 0.0626$).

### RQ2 – Temporal Variations & Year-by-Year Sensitivity
*What temporal patterns can be observed across years, months, weekdays, and hours?*

Multi-year sensitivity analysis (`2023–2026`) demonstrates substantial operational evolution:
- **2023 (`N = 395,298`):** Overall Mean `8.98s`, P95 `28.0s`, `652` calls $\ge 300\text{s}$ (`0.16%`). Notably, **Russian averaged `34.19s`** (exceeding the 30s OTI goal) and **Mandarin averaged `29.61s`**.
- **2024 (`N = 311,927`):** Overall Mean `9.84s`, P95 `38.0s`, `392` calls $\ge 300\text{s}$ (`0.13%`). Russian improved to `16.31s`.
- **2025 (`N = 212,764`):** Overall Mean `6.75s`, P95 `13.0s`, `286` calls $\ge 300\text{s}$ (`0.13%`). Mandarin dropped to `11.22s` and Russian to `7.69s`.
- **2026 YTD (`N = 141,108`):** Overall Mean `8.98s`, P95 `24.0s`, while the `>= 300s` review-threshold rate rose to **`0.23%`** (`322` calls).

### RQ3 – Limitations of Average-Based Reporting
*To what extent does mean-only reporting conceal upper-percentile waiting times and prolonged delays?*

1. **Median vs. Tail Divergence:** Across all 10 top languages except Haitian Creole (`8.0s`), the **median wait is uniformly `3.0s`**, yet **P95 ranges from `8.0s` (Spanish) to `163.0s` (Haitian Creole) and `153.0s` (Korean)**.
2. **Similar-Mean, Divergent-Tail Pairs (`N >= 100`):**
   - **Turkish** (`N = 1,281`, Mean `24.26s`, P95 `169.0s`) vs. **Yiddish** (`N = 240`, Mean `20.23s`, P95 `60.0s`): Mean difference of only `4.03s`, but a **`109.0s` P95 gap**.
   - **Mandarin** (`N = 124,123`, Mean `20.92s`, P95 `150.0s`) vs. **Dari** (`N = 113`, Mean `16.87s`, P95 `57.4s`): Mean difference of `4.05s`, but a **`92.6s` P95 gap**.
   - **Hindi** (`N = 1,016`, Mean `28.37s`, P95 `196.0s`) vs. **Romanian** (`N = 170`, Mean `23.97s`, P95 `104.3s`): Mean difference of `4.40s`, but a **`91.7s` P95 gap**.
3. **Metric-Specific Ranking Shifts:** Languages such as **Sylheti** (`rank_mean = 32` vs. `rank_p95 = 22`, shift `-10`) and **Farsi** (`rank_mean = 8` vs. `rank_p95 = 14`, shift `+6`) demonstrate that language rankings depend heavily on whether mean or upper-tail metrics are used.

### RQ4 – Policy-Aware Service Assessment
*How do observed waiting times compare against the NYC OTI 30s Goal and §23-310 300s Statutory Review Threshold?*

1. **NYC OTI 30-Second Average Goal (2023–2026 Aggregate):**
   - **Spanish:** `4.32s` (`-25.68s` vs. goal) — Satisfies aggregate goal.
   - **Cantonese:** `9.38s` (`-20.62s` vs. goal) — Satisfies aggregate goal.
   - **Russian:** `19.12s` (`-10.88s` vs. goal) — Satisfies 4-year aggregate, but **failed in 2023 (`34.19s`)**.
   - **Mandarin:** `20.92s` (`-9.08s` vs. goal) — Satisfies 4-year aggregate, yet 5% of Mandarin calls wait **`>= 150.0s`**.
2. **NYC Administrative Code §23-310 (300-Second Statutory Review Threshold):**
   - `1,652` calls (`0.16%`) reached $\ge 300\text{s}$. While standard calls (`< 300s`, `N = 1,059,445`) have a mean of `8.14s`, review-threshold calls (`N = 1,652`) have a mean of `420.48s` (median `367.0s`, P90 `568.0s`).
   - Russian (`467` calls) and Mandarin (`266` calls) account for `44.4%` of all statutory review triggers despite representing `19.4%` of call volume.

---

## 3. Sample-Size Cutoff Sensitivity

Evaluating minimum sample thresholds $k \in \{30, 50, 100, 500, 1000\}$:
- At $k = 30$: `54` languages qualify (`99.95%` of calls); highest mean is Fulani (`144.36s`, P95 `548.7s`).
- At $k = 100$ (baseline): `40` languages qualify (`99.88%` of calls); highest mean is Moroccan Arabic (`78.5s`, P95 `415.6s`).
- At $k = 1,000$: `15` languages qualify (`99.05%` of calls); highest mean is Uzbek (`33.63s`, P95 `217.6s`).

This confirms that retaining a $k = 100$ cutoff preserves `99.88%` of total call volume while preventing small-sample volatility from distorting language rankings.

---

## 4. Limitations (Per PRD Section 18)
All findings reflect observed connected calls only (`dzvt-6g3v`). Unsuccessful/abandoned calls, interpreter staffing schedules, and §23-310 review outcomes are unobserved; therefore, no causal or discrimination claims are made.
