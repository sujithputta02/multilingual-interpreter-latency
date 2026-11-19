# IEEE Literature Survey Audit and Research Gap Analysis (Phase 0)

**Project:** Beyond the Average: A Policy-Aware, Distribution-Sensitive Analysis of Multilingual Public-Service Interpreter Waiting Times  
**Survey Source:** Consensus IEEE Search Corpus (2023–2026 Window)  
**Verification Date:** November 2026  
**Status:** Audited and Verified

---

## 1. Literature Survey Overview

The preliminary survey explored the intersection of three principal disciplines within the 2023–2026 IEEE corpus:
1. **Queueing and Service-Level Delay Analysis**
2. **Language Access in Public-Service Delivery**
3. **Distribution-Sensitive Performance Measurement and Tail Estimation**

### Key Methodological Foundations from the Corpus:
- **Konrad & Liu (2023):** Demonstrates real-time waiting-time distribution estimation in nonstationary, time-varying queues. Proves that mean waiting times fail to characterize service quality under dynamic staffing.
- **Garyfallos et al. (2024):** Establishes that fluid approximations fail to capture tail probabilities and SLA threshold breaches, proving the mathematical necessity of distribution-sensitive and quantile-based metrics.
- **De Andrade et al. (2023):** Analyzes skill-based routing in multi-channel contact centers where service-level targets are defined by threshold non-exceedance probabilities.
- **Lolos et al. (2023, 2025):** Provides quantile confidence-interval estimation for upper percentiles (P90, P95) from empirical operational traces.
- **López et al. (2023) & Mostafavi et al. (2023):** Rare-event simulation and extreme-value methods for latency tail modeling.

---

## 2. Research Gap Identification

| Dimension | Existing IEEE Literature (2023–2026) | Gap Identified | Beyond the Average Contribution |
|:---|:---|:---|:---|
| **Domain** | Call centers, data networks, cloud computing, emergency dispatch (general) | Zero empirical studies evaluating municipal telephone human interpreter connection latency across languages | First empirical investigation of public-service interpreter connection waiting times in a major metropolitan 311 contact center |
| **Language Granularity** | Multilingual chatbots / NLP translation models (Han et al. 2024; Sangeetha et al. 2025) | No empirical analysis comparing wait times across 100+ human language queues in public services | Granular, language-wise empirical distribution analysis across all represented languages |
| **Metric Scope** | Mean response time, average holding time, or theoretical M/M/c queue formulas | Practical disconnect between municipal average-reporting conventions and tail/threshold realities | Systematic comparison of Mean-Only vs. Distribution-Sensitive (Median, P90, P95, §23-310 threshold frequency) reporting |
| **Policy Integration** | Abstract SLA thresholds (e.g. arbitrary 20s or 80/20 rules) | Failure to ground operational data in statutory language access mandates | Direct alignment with NYC OTI 30s Average Goal and NYC Administrative Code §23-310 (300-second review threshold) |

---

## 3. Discrepancy Reconciliation & Qualification
Per PRD Section 2.1 & Section 19 (Phase 0):
- **External Citations:** The Consensus survey references Pilarz et al. (2023), which is published outside IEEE (medical literature). This is classified strictly as domain background context, not an IEEE methodological antecedent.
- **Novelty Claim Scope:** The project does not claim that queueing theory or percentile estimation is novel. The contribution is the **empirical application and policy-aware evaluation** of distribution-sensitive measurement to public-service interpreter waiting times.
