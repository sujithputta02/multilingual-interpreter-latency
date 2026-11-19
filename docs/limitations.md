# Research Limitations and Methodological Scope

As mandated by Section 18 and Section 24 of the PRD, the findings and interpretations of this research platform operate under strict epistemological and observational constraints.

---

## 1. Connected-Call Selection Effect
The dataset records exclusively calls that successfully connected to a Language Line interpreter. Calls that were abandoned during the hold time, disconnected due to technical failure, or where callers hung up before language identification was completed are not recorded in this dataset. Consequently:
- Observed waiting times represent surviving successful transactions.
- Waiting times do not measure total caller patience or system abandonment rates.

## 2. Unobserved System and Capacity Variables
The dataset contains three operational attributes (`call_time`, `language`, `connect_time_sec`). It does **not** contain:
- Interpreter staffing levels or shifts by language.
- Third-party vendor (Language Line Solutions) routing logic or concurrent queue depths.
- Total incoming call volume to NYC 311.
- Language Line contract tiers or priority rules.
Therefore, differences in observed connection waiting times **cannot be causally attributed** to vendor negligence, institutional discrimination, or specific staffing shortages without external operational data.

## 3. Absence of Caller-Level Demographics
No caller identification, location, socio-economic status, gender, age, or immigration status is recorded. No demographic inference may be made from language preference.

## 4. Legal & Policy Nuance: §23-310 Threshold
Under NYC Administrative Code §23-310, a waiting time of >= 300 seconds triggers a mandatory internal review by 311 to determine whether delay stemmed from language-identification protocol failure.
- A call >= 300 seconds is an **indicator of statutory review eligibility**, NOT proof of a protocol failure or service violation.
- The dataset does not contain the findings or conclusions of any subsequent review.
- Prohibited labels: "protocol failure", "discrimination incident", "service breach", "interpreter error".

## 5. Stated Benchmark Scope: OTI 30-Second Average Goal
The NYC Office of Technology and Innovation (OTI) 2024 Language Access Implementation Plan sets a target **mean** waiting time of 30 seconds or less specifically for:
- Spanish
- Cantonese
- Mandarin
- Russian
This target cannot be treated as an official legal mandate for all 100+ languages recorded, nor does an average of <= 30 seconds guarantee that individual callers did not experience severe delays.

## 6. Single-Jurisdiction Boundary
The empirical observations reflect the municipal operational environment of New York City's 311 service and its specific vendor contracts. Findings should not be uncritically generalized to emergency dispatch (911), federal agencies, or other municipal jurisdictions.
