"""Inferential statistical testing (PRD Section 8.7)."""
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from scipy import stats


def run_kruskal_wallis_test(df: pd.DataFrame, languages: List[str], min_sample: int = 50) -> Dict[str, Any]:
    """
    Performs Kruskal-Wallis H-test for non-parametric multi-language distribution comparison.
    Computes test statistic, p-value, sample sizes, and epsilon-squared effect size.
    """
    groups = []
    valid_langs = []
    sample_sizes = {}

    for lang in languages:
        series = df[df["language"] == lang]["connect_time_sec"].dropna()
        if len(series) >= min_sample:
            groups.append(series.values)
            valid_langs.append(lang)
            sample_sizes[lang] = len(series)

    if len(groups) < 2:
        return {
            "test_name": "Kruskal-Wallis H-Test",
            "status": "error",
            "message": "At least 2 languages with sufficient sample size are required.",
        }

    stat, p_val = stats.kruskal(*groups)
    total_n = sum(sample_sizes.values())
    k = len(groups)

    # Epsilon-squared effect size: (H - k + 1) / (n - k)
    epsilon_sq = (stat - k + 1) / (total_n - k) if total_n > k else 0.0
    epsilon_sq = max(0.0, min(1.0, float(epsilon_sq)))

    return {
        "test_name": "Kruskal-Wallis H-Test",
        "status": "success",
        "null_hypothesis": "Waiting time distributions across selected languages are identical.",
        "languages_tested": valid_langs,
        "sample_sizes": sample_sizes,
        "total_observations": total_n,
        "test_statistic_H": round(float(stat), 4),
        "p_value": float(p_val),
        "is_statistically_significant": bool(p_val < 0.05),
        "effect_size_epsilon_squared": round(epsilon_sq, 4),
        "interpretation": (
            "Statistically significant difference across language distributions (p < 0.05)."
            if p_val < 0.05 else "No statistically significant difference detected (p >= 0.05)."
        ),
        "practical_note": "In large sample sizes, low p-values may occur even for minor practical differences. Observe effect size and percentile differences."
    }


def run_pairwise_mann_whitney(
    df: pd.DataFrame,
    lang_a: str,
    lang_b: str,
    alpha: float = 0.05,
    num_comparisons: int = 1
) -> Dict[str, Any]:
    """
    Performs pairwise Mann-Whitney U test between two languages with Bonferroni adjustment.
    """
    series_a = df[df["language"] == lang_a]["connect_time_sec"].dropna()
    series_b = df[df["language"] == lang_b]["connect_time_sec"].dropna()

    n_a = len(series_a)
    n_b = len(series_b)

    if n_a < 10 or n_b < 10:
        return {
            "status": "error",
            "message": f"Insufficient observations: {lang_a} (N={n_a}), {lang_b} (N={n_b})."
        }

    u_stat, p_val = stats.mannwhitneyu(series_a, series_b, alternative="two-sided")

    # Bonferroni corrected threshold
    adjusted_alpha = alpha / max(1, num_comparisons)

    # Rank-biserial correlation effect size: 1 - (2U / (n1 * n2))
    rank_biserial = 1.0 - (2.0 * float(u_stat) / (n_a * n_b))

    return {
        "test_name": "Mann-Whitney U Test (Pairwise)",
        "language_a": lang_a,
        "language_b": lang_b,
        "n_a": n_a,
        "n_b": n_b,
        "median_a": round(float(series_a.median()), 2),
        "median_b": round(float(series_b.median()), 2),
        "mean_a": round(float(series_a.mean()), 2),
        "mean_b": round(float(series_b.mean()), 2),
        "u_statistic": float(u_stat),
        "raw_p_value": float(p_val),
        "adjusted_alpha": float(adjusted_alpha),
        "is_significant": bool(p_val < adjusted_alpha),
        "rank_biserial_effect_size": round(float(rank_biserial), 4),
        "interpretation": (
            f"Statistically significant difference between {lang_a} and {lang_b} at Bonferroni-adjusted alpha={adjusted_alpha:.4f}."
            if p_val < adjusted_alpha else f"Difference between {lang_a} and {lang_b} is not statistically significant."
        )
    }
