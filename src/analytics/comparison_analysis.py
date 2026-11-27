"""Mean-only vs. distribution-sensitive comparison and confidence intervals (PRD Section 8.7, 9, & Phase 6)."""
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from scipy import stats

from src.analytics.language_analysis import compute_language_summary


def compute_metric_ranking_shifts(df: pd.DataFrame, min_sample_size: int = 100) -> pd.DataFrame:
    """
    Compares language rankings under conventional mean-only reporting vs.
    distribution-sensitive metrics (Median, P90, P95, and >=300s review rate).
    Rank 1 = lowest (fastest) waiting time or lowest review rate.
    """
    summary = compute_language_summary(df, min_sample_size=min_sample_size, sort_by="count", ascending=False)
    if summary.empty:
        return pd.DataFrame()

    sufficient = summary[summary["has_sufficient_sample"]].copy()
    if sufficient.empty:
        return pd.DataFrame()

    sufficient["rank_mean"] = sufficient["mean"].rank(method="min", ascending=True).astype(int)
    sufficient["rank_median"] = sufficient["median"].rank(method="min", ascending=True).astype(int)
    sufficient["rank_p90"] = sufficient["p90"].rank(method="min", ascending=True).astype(int)
    sufficient["rank_p95"] = sufficient["p95"].rank(method="min", ascending=True).astype(int)
    sufficient["rank_pct_300s"] = sufficient["pct_ge_300s"].rank(method="min", ascending=True).astype(int)

    # Positive shift = ranks worse in P95 tail than in Mean (concealed tail delay)
    sufficient["shift_mean_to_p95"] = sufficient["rank_p95"] - sufficient["rank_mean"]
    sufficient["abs_shift_mean_to_p95"] = sufficient["shift_mean_to_p95"].abs()

    return sufficient.sort_values(by=["abs_shift_mean_to_p95", "count"], ascending=[False, False]).reset_index(drop=True)


def find_similar_mean_divergent_tail_pairs(
    df: pd.DataFrame,
    min_sample_size: int = 100,
    mean_tolerance_sec: float = 5.0,
    min_p95_gap_sec: float = 30.0,
) -> pd.DataFrame:
    """
    Identifies pairs of sufficiently represented languages with similar arithmetic means
    (|mean_A - mean_B| <= mean_tolerance_sec) but divergent P95 tail waiting times
    (|p95_A - p95_B| >= min_p95_gap_sec) (PRD Section 9.3).
    """
    summary = compute_language_summary(df, min_sample_size=min_sample_size)
    if summary.empty:
        return pd.DataFrame()

    elig = summary[summary["has_sufficient_sample"]].reset_index(drop=True)
    if len(elig) < 2:
        return pd.DataFrame()

    pairs: List[Dict[str, Any]] = []
    n_langs = len(elig)
    for i in range(n_langs):
        row_a = elig.iloc[i]
        for j in range(i + 1, n_langs):
            row_b = elig.iloc[j]
            mean_diff = abs(float(row_a["mean"]) - float(row_b["mean"]))
            p95_diff = abs(float(row_a["p95"]) - float(row_b["p95"]))
            if mean_diff <= mean_tolerance_sec and p95_diff >= min_p95_gap_sec:
                pairs.append({
                    "language_a": row_a["language"],
                    "n_a": int(row_a["count"]),
                    "mean_a": float(row_a["mean"]),
                    "median_a": float(row_a["median"]),
                    "p95_a": float(row_a["p95"]),
                    "pct_300s_a": float(row_a["pct_ge_300s"]),
                    "language_b": row_b["language"],
                    "n_b": int(row_b["count"]),
                    "mean_b": float(row_b["mean"]),
                    "median_b": float(row_b["median"]),
                    "p95_b": float(row_b["p95"]),
                    "pct_300s_b": float(row_b["pct_ge_300s"]),
                    "mean_diff_sec": round(mean_diff, 2),
                    "p95_diff_sec": round(p95_diff, 2),
                })

    if not pairs:
        return pd.DataFrame()
    return pd.DataFrame(pairs).sort_values(by="p95_diff_sec", ascending=False).reset_index(drop=True)


def _wilson_ci(successes: int, total: int, z: float = 1.959964) -> tuple[float, float]:
    """Computes Wilson score confidence interval for proportions (in percent)."""
    if total == 0:
        return 0.0, 0.0
    p = successes / total
    denom = 1.0 + (z ** 2) / total
    center = (p + (z ** 2) / (2.0 * total)) / denom
    half_width = (z * np.sqrt((p * (1.0 - p) + (z ** 2) / (4.0 * total)) / total)) / denom
    low = max(0.0, (center - half_width) * 100.0)
    high = min(100.0, (center + half_width) * 100.0)
    return round(float(low), 3), round(float(high), 3)


def compute_confidence_intervals(
    series: pd.Series,
    confidence: float = 0.95,
    n_bootstrap: int = 300,
    max_subsample: int = 50000,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Computes confidence intervals for Mean (normal/t), Median, P90, P95 (bootstrap),
    and >=300s proportion (Wilson score) per PRD Section 8.7 & 17.2.
    """
    clean = pd.Series(series).dropna().to_numpy(dtype=float)
    n = len(clean)
    if n == 0:
        return {"count": 0}

    z = float(stats.norm.ppf(1.0 - (1.0 - confidence) / 2.0))
    mean_val = float(np.mean(clean))
    se_mean = float(np.std(clean, ddof=1) / np.sqrt(n)) if n > 1 else 0.0
    mean_ci = (round(mean_val - z * se_mean, 2), round(mean_val + z * se_mean, 2))

    # Subsample for fast bootstrap if N is very large
    rng = np.random.default_rng(random_state)
    boot_source = clean if n <= max_subsample else rng.choice(clean, size=max_subsample, replace=False)
    m = len(boot_source)

    medians = np.empty(n_bootstrap)
    p90s = np.empty(n_bootstrap)
    p95s = np.empty(n_bootstrap)
    for b in range(n_bootstrap):
        sample = rng.choice(boot_source, size=m, replace=True)
        q = np.quantile(sample, [0.50, 0.90, 0.95])
        medians[b], p90s[b], p95s[b] = q[0], q[1], q[2]

    alpha_low = ((1.0 - confidence) / 2.0) * 100.0
    alpha_high = (1.0 - (1.0 - confidence) / 2.0) * 100.0

    long_count = int(np.sum(clean >= 300.0))
    prop_pct = round((long_count / n) * 100.0, 3)
    prop_ci = _wilson_ci(long_count, n, z=z)

    return {
        "count": n,
        "confidence_level": confidence,
        "mean": round(mean_val, 2),
        "mean_ci": mean_ci,
        "median": round(float(np.quantile(clean, 0.50)), 2),
        "median_ci": (round(float(np.percentile(medians, alpha_low)), 2), round(float(np.percentile(medians, alpha_high)), 2)),
        "p90": round(float(np.quantile(clean, 0.90)), 2),
        "p90_ci": (round(float(np.percentile(p90s, alpha_low)), 2), round(float(np.percentile(p90s, alpha_high)), 2)),
        "p95": round(float(np.quantile(clean, 0.95)), 2),
        "p95_ci": (round(float(np.percentile(p95s, alpha_low)), 2), round(float(np.percentile(p95s, alpha_high)), 2)),
        "pct_ge_300s": prop_pct,
        "pct_ge_300s_ci": prop_ci,
    }
