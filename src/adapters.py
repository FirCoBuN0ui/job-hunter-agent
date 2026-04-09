import json
from pathlib import Path
from .models import Job
from .pipeline import load_jobs


def _read_json(path: str):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {path}") from e


def load_from_boss(path: str) -> list[Job]:
    data = _read_json(path)
    if not isinstance(data, list):
        raise ValueError("boss input must be a list")
    jobs = []
    for i, x in enumerate(data):
        try:
            jobs.append(
                Job(
                    title=x["jobName"],
                    company=x["brandName"],
                    city=x["cityName"],
                    salary=x["salaryDesc"],
                    description=x.get("postDescription", ""),
                    url=x["jobUrl"],
                )
            )
        except KeyError as e:
            raise ValueError(f"boss schema error at index {i}: missing {e}") from e
    return jobs


def load_from_lagou(path: str) -> list[Job]:
    data = _read_json(path)
    if not isinstance(data, list):
        raise ValueError("lagou input must be a list")
    jobs = []
    for i, x in enumerate(data):
        try:
            jobs.append(
                Job(
                    title=x["positionName"],
                    company=x["companyFullName"],
                    city=x["city"],
                    salary=x["salary"],
                    description=x.get("positionAdvantage", ""),
                    url=x["positionUrl"],
                )
            )
        except KeyError as e:
            raise ValueError(f"lagou schema error at index {i}: missing {e}") from e
    return jobs


SOURCE_LOADERS = {
    "local": load_jobs,
    "boss": load_from_boss,
    "lagou": load_from_lagou,
}


def supported_sources() -> list[str]:
    return sorted(SOURCE_LOADERS.keys())


def load_jobs_by_source(source: str, path: str) -> list[Job]:
    s = source.lower()
    loader = SOURCE_LOADERS.get(s)
    if loader is None:
        raise ValueError(
            f"Unsupported source: {source}. Supported: {', '.join(supported_sources())}"
        )
    return loader(path)