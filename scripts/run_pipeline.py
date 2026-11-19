"""CLI runner for pipeline execution."""
import argparse
import sys
from src.ingestion.refresh import run_full_pipeline


def main():
    parser = argparse.ArgumentParser(description="Beyond the Average: Pipeline Runner")
    parser.add_argument("--max-records", type=int, default=50000, help="Maximum records to ingest (default: 50,000)")
    parser.add_argument("--batch-size", type=int, default=25000, help="Batch size per API call")
    parser.add_argument("--force-download", action="store_true", help="Force fresh download from NYC Open Data")
    args = parser.parse_args()

    print(f"Starting ingestion (max_records={args.max_records}, batch_size={args.batch_size})...")
    res = run_full_pipeline(
        max_records=args.max_records,
        batch_size=args.batch_size,
        force_download=args.force_download
    )
    print("Pipeline Execution Result:")
    for k, v in res.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
