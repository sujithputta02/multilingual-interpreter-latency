"""Reproducible Phase 6 & Phase 7 research output generator."""
import json
from pathlib import Path
import pandas as pd

from src.storage.parquet_manager import load_processed_parquet
from src.analytics.descriptive import calculate_descriptive_stats
from src.analytics.language_analysis import compute_language_summary
from src.analytics.temporal_analysis import compute_monthly_trend, compute_hourly_summary, compute_day_of_week_summary
from src.analytics.policy_analysis import evaluate_oti_average_goal, evaluate_statutory_review_threshold
from src.analytics.comparison_analysis import (
    compute_metric_ranking_shifts,
    find_similar_mean_divergent_tail_pairs,
    compute_confidence_intervals,
)
from src.analytics.sensitivity_analysis import sample_size_sensitivity, temporal_period_sensitivity
from src.analytics.statistical_tests import run_kruskal_wallis_test
from src.utils.exports import render_language_comparison_png, render_monthly_trend_png
from src.utils.metadata import load_json, save_json


def main():
    df = load_processed_parquet()
    if df is None or df.empty:
        raise RuntimeError("Processed dataset not found.")

    tables_dir = Path("research/results/tables")
    figures_dir = Path("research/results/figures")
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # 1. Overall descriptive + 95% CIs
    overall = calculate_descriptive_stats(df["connect_time_sec"])
    overall_ci = compute_confidence_intervals(df["connect_time_sec"])

    # 2. Language summary & ranking shifts
    lang_summary = compute_language_summary(df, min_sample_size=100, sort_by="count", ascending=False)
    lang_summary.to_csv(tables_dir / "language_summary_all.csv", index=False)

    ranking_shifts = compute_metric_ranking_shifts(df, min_sample_size=100)
    ranking_shifts.to_csv(tables_dir / "metric_ranking_shifts.csv", index=False)

    divergent_pairs = find_similar_mean_divergent_tail_pairs(df, min_sample_size=100, mean_tolerance_sec=5.0, min_p95_gap_sec=30.0)
    divergent_pairs.to_csv(tables_dir / "similar_mean_divergent_tail_pairs.csv", index=False)

    # 3. Temporal summaries
    monthly = compute_monthly_trend(df)
    monthly.to_csv(tables_dir / "monthly_trend.csv", index=False)
    hourly = compute_hourly_summary(df)
    hourly.to_csv(tables_dir / "hourly_summary.csv", index=False)
    dow = compute_day_of_week_summary(df)
    dow.to_csv(tables_dir / "day_of_week_summary.csv", index=False)

    # 4. Policy benchmarks
    oti_df = evaluate_oti_average_goal(df)
    oti_df.to_csv(tables_dir / "oti_30s_goal_evaluation.csv", index=False)
    stat_res = evaluate_statutory_review_threshold(df)
    if not stat_res["language_breakdown"].empty:
        stat_res["language_breakdown"].to_csv(tables_dir / "statutory_300s_by_language.csv", index=False)

    # 5. Sensitivity analyses
    sample_sens = sample_size_sensitivity(df)
    sample_sens.to_csv(tables_dir / "sample_size_sensitivity.csv", index=False)
    year_sens = temporal_period_sensitivity(df)
    year_sens.to_csv(tables_dir / "temporal_year_sensitivity.csv", index=False)

    # 6. Inferential test (Kruskal-Wallis across top 10 languages)
    top10_langs = lang_summary.head(10)["language"].tolist()
    kw_res = run_kruskal_wallis_test(df, top10_langs, min_sample=100)

    # 7. Figures (PNG)
    (figures_dir / "language_comparison_top10.png").write_bytes(
        render_language_comparison_png(lang_summary, top_n=10, title_suffix=" (Full NYC 311 Dataset)")
    )
    (figures_dir / "monthly_trajectory.png").write_bytes(
        render_monthly_trend_png(monthly)
    )

    # 8. Summary JSON for exact citation
    summary_payload = {
        "overall": overall,
        "overall_ci": overall_ci,
        "kruskal_wallis_top10": kw_res,
        "statutory_300s": {
            "total_calls": stat_res["total_calls"],
            "threshold_calls_count": stat_res["threshold_calls_count"],
            "threshold_percentage": stat_res["threshold_percentage"],
            "distribution_comparison": stat_res["distribution_comparison"],
        },
        "oti_goal": oti_df.to_dict(orient="records"),
        "top_10_languages": lang_summary.head(10).to_dict(orient="records"),
        "top_5_ranking_shifts": ranking_shifts.head(5).to_dict(orient="records"),
        "top_5_divergent_pairs": divergent_pairs.head(5).to_dict(orient="records"),
        "sample_size_sensitivity": sample_sens.to_dict(orient="records"),
        "year_sensitivity": year_sens.to_dict(orient="records"),
    }
    save_json(summary_payload, "research/results/empirical_summary.json")
    print("Generated all research tables, figures, and empirical_summary.json!")


if __name__ == "__main__":
    main()
