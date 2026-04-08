import json
from pathlib import Path
from .models import Job
from .scorer import score_job


def load_jobs(path: str) -> list[Job]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    try:
        raw = p.read_text(encoding="utf-8")
    except Exception as e:
        raise RuntimeError(f"Failed to read input file: {path}") from e

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in file: {path}") from e

    if not isinstance(data, list):
        raise ValueError(f"JSON root must be a list: {path}")

    jobs = []
    for i, item in enumerate(data):
        try:
            jobs.append(Job(**item))
        except TypeError as e:
            raise ValueError(f"Invalid job schema at index {i}: {item}") from e

    return jobs


def deduplicate_jobs(jobs: list[Job]) -> list[Job]:
    seen = set()
    unique = []
    for job in jobs:
        if job.url not in seen:
            seen.add(job.url)
            unique.append(job)
    return unique


def rank_jobs(jobs: list[Job], keywords: list[str]) -> list[dict]:
    ranked = []
    for job in jobs:
        s = score_job(job, keywords)
        ranked.append(
            {
                "title": job.title,
                "company": job.company,
                "city": job.city,
                "salary": job.salary,
                "url": job.url,
                "score": s,
            }
        )
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked


def save_report_json(items: list[dict], out_path: str) -> None:
    Path(out_path).write_text(
        json.dumps(items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def save_report_md(items: list[dict], out_path: str) -> None:
    lines = [
        "# Job Hunter Report",
        "",
        "| Rank | Title | Company | City | Salary | Score | URL |",
        "|---:|---|---|---|---|---:|---|",
    ]
    for i, it in enumerate(items, start=1):
        lines.append(
            f"| {i} | {it['title']} | {it['company']} | {it['city']} | "
            f"{it['salary']} | {it['score']} | {it['url']} |"
        )
    Path(out_path).write_text("\n".join(lines), encoding="utf-8")