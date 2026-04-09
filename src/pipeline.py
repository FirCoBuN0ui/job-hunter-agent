import json
from pathlib import Path
from .models import Job
from .scorer import score_job
import csv


def load_jobs(path: str) -> list[Job]:
    p = Path(path)
    ext = p.suffix.lower()

    if ext == ".json":
        return load_jobs_json(path)
    if ext == ".csv":
        return load_jobs_csv(path)

    raise ValueError(f"Unsupported input file type: {ext}. Use .json or .csv")


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




def save_report_csv(rows: list[dict], out_path: str) -> None:
    fieldnames = ["title", "company", "city", "salary", "score", "url"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(
                {
                    "title": r.get("title", ""),
                    "company": r.get("company", ""),
                    "city": r.get("city", ""),
                    "salary": r.get("salary", ""),
                    "score": r.get("score", 0),
                    "url": r.get("url", ""),
                }
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


def load_jobs_csv(path: str) -> list[Job]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    jobs = []
    try:
        with p.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            required = {"title", "company", "city", "salary", "description", "url"}
            if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
                raise ValueError(
                    f"CSV missing required columns. required={required}, got={reader.fieldnames}"
                )

            for i, row in enumerate(reader, start=2):  # 第2行开始是数据行
                try:
                    jobs.append(
                        Job(
                            title=row["title"],
                            company=row["company"],
                            city=row["city"],
                            salary=row["salary"],
                            description=row["description"],
                            url=row["url"],
                        )
                    )
                except Exception as e:
                    raise ValueError(f"Invalid CSV row at line {i}: {row}") from e
    except UnicodeDecodeError as e:
        raise ValueError(f"CSV encoding must be utf-8: {path}") from e

    return jobs


def load_jobs_json(path: str) -> list[Job]:
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