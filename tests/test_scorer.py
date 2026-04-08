from src.models import Job
from src.scorer import score_job


def make_job(title: str, description: str) -> Job:
    return Job(
        title=title,
        company="Demo",
        city="Shanghai",
        salary="20k-30k",
        description=description,
        url="https://example.com/job/1",
    )


def test_score_hits_keywords():
    job = make_job("Python Backend Engineer", "Need Python, FastAPI, Docker")
    score = score_job(job, ["python", "fastapi"])
    assert score >= 40


def test_score_remote_bonus():
    job = make_job("Backend Engineer", "支持远程办公，熟悉API开发")
    score = score_job(job, ["api"])
    assert score >= 30


def test_score_empty_keywords():
    job = make_job("Data Engineer", "SQL and ETL")
    score = score_job(job, [])
    assert score == 0