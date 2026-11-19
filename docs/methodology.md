# Analytical and Statistical Methodology

## 1. Study Design
This research employs a retrospective, observational, quantitative design examining granular connection-delay records from the NYC 311 municipal telephone system.

## 2. Statistical Metrics Formulation

Let $X = \{x_1, x_2, \dots, x_N\}$ represent observed connection waiting times in seconds for a specified cohort (language $L$ during temporal window $T$).

### Central Tendency & Spread
- **Mean ($\mu$):** $\bar{x} = \frac{1}{N}\sum_{i=1}^N x_i$
- **Median ($P_{50}$):** $\text{Quantile}(X, 0.50)$
- **Standard Deviation ($\sigma$):** $\sqrt{\frac{1}{N-1} \sum_{i=1}^N (x_i - \bar{x})^2}$
- **Interquartile Range ($IQR$):** $P_{75} - P_{25}$

### Distribution Tail & Prolonged Delay
- **P90:** $\text{Quantile}(X, 0.90)$
- **P95:** $\text{Quantile}(X, 0.95)$
- **Statutory Threshold Frequency ($F_{300}$):** $N_{300} = \sum_{i=1}^N \mathbb{I}(x_i \ge 300)$
- **Statutory Threshold Rate ($R_{300}$):** $\frac{N_{300}}{N} \times 100\%$

## 3. Policy-Aware Assessment

### Benchmark 1: NYC OTI Stated Goal (Four Major Languages)
For $l \in \{\text{Spanish}, \text{Cantonese}, \text{Mandarin}, \text{Russian}\}$:
$$\Delta_{\text{OTI}}(l) = \bar{x}_l - 30.0$$
If $\bar{x}_l \le 30.0$, the observed cohort average satisfies the stated operational target.

### Benchmark 2: §23-310 Review Proportion
For any cohort, calculate the absolute count $N_{300}$ and proportion $R_{300}$.
Distributions are partitioned into standard operations ($x < 300\text{s}$) versus review threshold records ($x \ge 300\text{s}$).

## 4. Inferential Testing Framework

### Non-Parametric Multi-Group Comparison
Given heavy positive skewness and long tails in queue waiting times, non-parametric procedures are prioritized:
- **Kruskal-Wallis $H$-Test:** Tests the null hypothesis that median waiting times across $k$ languages are identical.
- **Pairwise Mann-Whitney $U$ Tests:** With Bonferroni or False Discovery Rate (FDR) adjustments for post-hoc pairwise comparisons.
- **Effect Size:** Epsilon-squared ($\epsilon^2$) for Kruskal-Wallis, Rank Biserial Correlation ($r$) for Mann-Whitney $U$.
- **Sample Size Precondition:** Languages with $N < 100$ are flagged as low statistical power and excluded from ranking tables to prevent small-sample volatility.

## 5. Mean-Only vs. Distribution-Sensitive Comparative Evaluation
To evaluate information concealment under aggregate reporting:
1. Cohorts with comparable arithmetic means ($\Delta \mu \le 3\text{s}$) are paired.
2. Differences in tail percentiles ($|P_{95}^{(A)} - P_{95}^{(B)}|$) and threshold rates ($|R_{300}^{(A)} - R_{300}^{(B)}|$) are computed.
3. Language ranking displacement: Rank according to Mean vs Rank according to P95 and $R_{300}$.
