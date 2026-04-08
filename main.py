import argparse
from src.logger import setup_logger
from src.pipeline import (
    load_jobs,
    deduplicate_jobs,
    rank_jobs,
    save_report_json,
    save_report_md,
)


def main():
    parser = argparse.ArgumentParser(description="Job Hunter Agent")
    parser.add_argument("--input", default="data/jobs_mock.json", help="Input jobs json path")
    parser.add_argument("--keywords", nargs="+", default=["python", "api", "remote"], help="Keywords for scoring")
    parser.add_argument("--top", type=int, default=5, help="Top N jobs to output")
    parser.add_argument("--out", default="jobs_report.json", help="Output json report path")
    parser.add_argument("--out-md", default="jobs_report.md", help="Output markdown report path")
    parser.add_argument("--log-level", default="INFO", help="Logging level: DEBUG/INFO/WARNING/ERROR")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum score threshold (0-100)")
    args = parser.parse_args()
    logger = setup_logger(args.log_level)
    try:
        logger.info("Loading jobs from %s", args.input)
        jobs = load_jobs(args.input)

        logger.info("Deduplicating jobs...")
        jobs = deduplicate_jobs(jobs)

        logger.info("Ranking jobs with keywords: %s", args.keywords)
        ranked = rank_jobs(jobs, args.keywords)
        
        logger.info("Filtering jobs with min_score >= %s", args.min_score)
        ranked = [x for x in ranked if x["score"] >= args.min_score]
        topn = ranked[: args.top]

        logger.info("Saving json report to %s", args.out)
        save_report_json(topn, args.out)

        logger.info("Saving markdown report to %s", args.out_md)
        save_report_md(topn, args.out_md)

        logger.info("Done. total=%s, topn=%s", len(jobs), len(topn))
        print(f"Loaded jobs(after dedup): {len(jobs)}")
        print(f"Keywords: {args.keywords}")
        print(f"Saved top {len(topn)} jobs to: {args.out}")
        print(f"Saved markdown report to: {args.out_md}")

    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()