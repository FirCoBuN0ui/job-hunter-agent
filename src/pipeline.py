import json
from pathlib import Path
from .models import Job
from .scorer import score_job


def load_jobs(path: str) -> list[Job]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Job(**item) for item in data]


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