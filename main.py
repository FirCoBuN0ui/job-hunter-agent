import argparse
from src.storage import fetch_recent_jobs
from src.logger import setup_logger
from src.pipeline import (
    load_jobs,
    deduplicate_jobs,
    rank_jobs,
    save_report_json,
    save_report_md,
    save_report_csv,
)
from datetime import datetime
from src.storage import init_db, save_ranked_jobs
from pathlib import Path
from src.adapters import load_jobs_by_source
import yaml
import sys



def main():
    parser = argparse.ArgumentParser(description="Job Hunter Agent")
    parser.add_argument("--input", default="data/jobs_mock.json", help="Input jobs json path")
    parser.add_argument("--keywords", nargs="+", default=["python", "api", "remote"], help="Keywords for scoring")
    parser.add_argument("--top", type=int, default=5, help="Top N jobs to output")
    parser.add_argument("--out", default="jobs_report.json", help="Output json report path")
    parser.add_argument("--out-md", default="jobs_report.md", help="Output markdown report path")
    parser.add_argument("--log-level", default="INFO", help="Logging level: DEBUG/INFO/WARNING/ERROR")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum score threshold (0-100)")
    parser.add_argument("--db", default="jobs.db", help="SQLite DB path")
    parser.add_argument("--history", type=int, default=0, help="Show recent N records from DB and exit")
    parser.add_argument("--history-date", default="", help="Show records by date (YYYY-MM-DD) and exit")
    parser.add_argument("--history-out-md", default="", help="Output markdown file for history query")
    parser.add_argument("--source", default="local", help="Data source: local/boss/lagou")
    parser.add_argument("--dry-run", action="store_true", help="Preview top results only, do not write files/db")
    parser.add_argument("--export-csv", default="", help="Optional csv output path for topN")
    parser.add_argument("--stats", action="store_true", help="Show DB statistics and exit")
    parser.add_argument("--config", default="", help="Path to yaml config file")
    args = parser.parse_args()
    explicit_flags = get_explicit_cli_flags(sys.argv)
    if args.config:
        cfg = load_yaml_config(args.config)
        apply_config_defaults(args, cfg, explicit_flags)
    logger = setup_logger(args.log_level)
    try:
        if args.stats:
            init_db(args.db)
            from src.storage import fetch_stats
            s = fetch_stats(db_path=args.db)

            print("=== Job DB Stats ===")
            print(f"Total records : {s['total']}")
            print(f"Average score : {s['avg_score']:.2f}")
            print(f"Max score     : {s['max_score']}")

            print("\nTop cities:")
            if s["top_cities"]:
                for i, x in enumerate(s["top_cities"], start=1):
                    print(f"  {i}. {x['city']} ({x['count']})")
            else:
                print("  (no data)")

            print("\nTop companies:")
            if s["top_companies"]:
                for i, x in enumerate(s["top_companies"], start=1):
                    print(f"  {i}. {x['company']} ({x['count']})")
            else:
                print("  (no data)")
            return
        if args.history > 0:
            init_db(args.db)
            records = fetch_recent_jobs(limit=args.history, db_path=args.db)
            if not records:
                print("No history records found.")
            else:
                for i, r in enumerate(records, start=1):
                    print(f"[{i}] {r['run_at']} | {r['score']:>3} | {r['title']} | {r['company']} | {r['city']}")
                    if args.history_out_md:
                        save_history_md(records, args.history_out_md, title=f"History Top {args.history}")
                        print(f"History markdown saved to: {args.history_out_md}")
            return

        if args.history_date and not validate_date_yyyy_mm_dd(args.history_date):
            print(f"Invalid --history-date: {args.history_date}. Expected format: YYYY-MM-DD")
            return
        if args.history_date:
            init_db(args.db)
            from src.storage import fetch_jobs_by_date
            records = fetch_jobs_by_date(args.history_date, db_path=args.db)
            if not records:
                print(f"No records found for date: {args.history_date}")
            else:
                for i, r in enumerate(records, start=1):
                    print(f"[{i}] {r['run_at']} | {r['score']:>3} | {r['title']} | {r['company']} | {r['city']}")
                print(f"Total: {len(records)} records")
                if args.history_out_md:
                    save_history_md(records, args.history_out_md, title=f"History for {args.history_date}")
                    print(f"History markdown saved to: {args.history_out_md}")
            return

        logger.info("Loading jobs from %s", args.input)
        jobs = load_jobs_by_source(args.source, args.input)

        logger.info("Deduplicating jobs...")
        jobs = deduplicate_jobs(jobs)

        logger.info("Ranking jobs with keywords: %s", args.keywords)
        ranked = rank_jobs(jobs, args.keywords)

        logger.info("Filtering jobs with min_score >= %s", args.min_score)
        ranked = [x for x in ranked if x["score"] >= args.min_score]
        topn = ranked[: args.top]

        if args.dry_run:
            print(f"[DRY-RUN] total_after_filter={len(ranked)}, topn={len(topn)}")
            for i, r in enumerate(topn, start=1):
                print(f"[{i}] {r['score']:>3} | {r['title']} | {r['company']} | {r['city']} | {r['salary']}")
            return

        logger.info("Saving json report to %s", args.out)
        save_report_json(topn, args.out)

        logger.info("Saving markdown report to %s", args.out_md)
        save_report_md(topn, args.out_md)

        if args.export_csv:
            logger.info("Saving csv report to %s", args.export_csv)
            save_report_csv(topn, args.export_csv)

        run_at = datetime.now().isoformat(timespec="seconds")
        init_db(args.db)
        n_saved = save_ranked_jobs(topn, db_path=args.db, run_at=run_at)
        logger.info("Saved %s ranked jobs to DB: %s", n_saved, args.db)

        logger.info("Done. total=%s, topn=%s", len(jobs), len(topn))
        print(f"Loaded jobs(after dedup): {len(jobs)}")
        print(f"Keywords: {args.keywords}")
        print(f"Saved top {len(topn)} jobs to: {args.out}")
        print(f"Saved markdown report to: {args.out_md}")


    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        raise SystemExit(1)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
    except ValueError as e:
        print(f"[ERROR] {e}")


def save_history_md(records: list[dict], out_path: str, title: str = "History Report") -> None:
    lines = [f"# {title}", ""]
    lines.append("| # | run_at | score | title | company | city |")
    lines.append("|---|---|---:|---|---|---|")
    for i, r in enumerate(records, start=1):
        lines.append(
            f"| {i} | {r['run_at']} | {r['score']} | {r['title']} | {r['company']} | {r['city']} |"
        )
    lines.append("")
    Path(out_path).write_text("\n".join(lines), encoding="utf-8")



def load_yaml_config(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Config file must be a YAML mapping/object")
    return data


def get_explicit_cli_flags(argv: list[str]) -> set[str]:
    """
    从 sys.argv 里提取用户显式传入的 long flags（如 --top, --db, --keywords）
    """
    explicit = set()
    for token in argv[1:]:
        if token.startswith("--"):
            key = token.split("=", 1)[0]   # 兼容 --top=3
            explicit.add(key.lstrip("-").replace("-", "_"))
    return explicit

def apply_config_defaults(args, cfg: dict, explicit_flags: set[str]):
    """
    规则：
    - CLI 显式传入的参数，不被 config 覆盖
    - CLI 未显式传入的参数，可由 config 提供默认
    """
    def can_fill(name: str) -> bool:
        return name not in explicit_flags and name in cfg

    if can_fill("source"):
        args.source = cfg["source"]

    if can_fill("input"):
        args.input = cfg["input"]

    if can_fill("keywords"):
        kw = cfg["keywords"]
        args.keywords = ",".join(str(x) for x in kw) if isinstance(kw, list) else str(kw)

    if can_fill("top"):
        args.top = int(cfg["top"])

    if can_fill("min_score"):
        args.min_score = int(cfg["min_score"])

    if can_fill("db"):
        args.db = str(cfg["db"])

    if can_fill("out"):
        args.out = str(cfg["out"])

    if can_fill("out_md"):
        args.out_md = str(cfg["out_md"])

    if can_fill("export_csv"):
        args.export_csv = str(cfg["export_csv"])

    if can_fill("log_level"):
        args.log_level = str(cfg["log_level"])

    if can_fill("history"):
        args.history = int(cfg["history"])

    if can_fill("history_date"):
        args.history_date = str(cfg["history_date"])

    if can_fill("history_out_md"):
        args.history_out_md = str(cfg["history_out_md"])

    # bool 参数
    if can_fill("dry_run"):
        args.dry_run = bool(cfg["dry_run"])

    if can_fill("stats"):
        args.stats = bool(cfg["stats"])


def validate_date_yyyy_mm_dd(s: str) -> bool:
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    main()