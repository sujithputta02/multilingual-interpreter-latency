# Data Dictionary: NYC 311 Interpreter Wait Time

**Source Dataset:** NYC Open Data – 311 Interpreter Wait Time  
**Dataset Identifier:** `dzvt-6g3v`  
**Endpoint:** `https://data.cityofnewyork.us/resource/dzvt-6g3v.json`  
**Update Frequency:** Monthly (records from preceding month published mid-month)  
**Unit of Analysis:** One successfully connected 311 interpreter call record.

---

## 1. Raw Source Schema

As published by NYC Open Data and documented in the official data dictionary:

| Field Name | Source Data Type | Description | Permitted Nulls | Range / Constraints |
|:---|:---|:---|:---|:---|
| `call_time` | Floating Timestamp | Timestamp associated with the 311 interpreter call record. Format: `YYYY-MM-DDTHH:MM:SS.000` | No | Historical date range of NYC 311 dataset |
| `language` | Plain Text | Requested interpretation language (e.g., 'Spanish', 'Cantonese', 'Russian') | No | Free-text language label |
| `connect_time_sec` | Number (Float/Int) | Waiting time in seconds for connection to a Language Line interpreter | No | >= 0 seconds (observed values can range up to hours) |

### Important Semantic Notes:
1. **Timestamp Semantics:** Floating timestamp. The PRD mandates preserving raw timestamps without premature or speculative timezone shift. In analytics, consistent New York Eastern Time (US/Eastern) or UTC representation is documented transparently.
2. **Duplicate Rows:** The dataset contains no row-level UUID. Multiple distinct calls can occur at the same second with the same language and duration. Per PRD Section 11.3, identical rows must NOT be deleted.
3. **Outliers and Extreme Values:** Waiting times above 300 seconds are legally significant under NYC Administrative Code §23-310 and must be preserved, not winsorized or removed.

---

## 2. Derived Analytical Schema

The feature engineering pipeline derives the following analytical attributes:

| Field Name | Data Type | Derivation Logic | Purpose |
|:---|:---|:---|:---|
| `call_time` | Timestamp (ns) | Parsed from raw `call_time` string | Chronological indexing and filtering |
| `raw_language` | String | Preserved original string from API | Auditability |
| `language` | String | Stripped whitespace, title-cased standard label | Grouping and ranking |
| `connect_time_sec` | Float64 | Numeric waiting time in seconds | Core measurement metric |
| `year` | Int32 | `call_time.year` | Long-term trend analysis |
| `month` | Int32 | `call_time.month` (1-12) | Monthly seasonality |
| `year_month` | String | `YYYY-MM` | Time-series charting |
| `date` | Date | `call_time.date` | Daily aggregation |
| `hour` | Int32 | `call_time.hour` (0-23) | Diurnal pattern analysis |
| `day_of_week` | String | Monday through Sunday | Day-of-week demand analysis |
| `day_of_week_num` | Int32 | 0 (Monday) through 6 (Sunday) | Sorting and heatmaps |
| `week_of_year` | Int32 | ISO calendar week (1-53) | Weekly trends |
| `time_period` | String | Configurable: Night (00-06), Morning (06-12), Afternoon (12-18), Evening (18-24) | High-level temporal grouping |
| `is_300s_or_more` | Boolean | `connect_time_sec >= 300.0` | Statutory review threshold indicator (§23-310) |
| `wait_category` | String | Binned: '0-30s', '31-60s', '61-120s', '121-299s', '>=300s' | Distribution visualization |
| `is_oti_language` | Boolean | `language in ['Spanish', 'Cantonese', 'Mandarin', 'Russian']` | NYC OTI 30s policy benchmark flag |
