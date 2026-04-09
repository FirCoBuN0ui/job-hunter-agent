from src.models import Job
from src.scorer import score_job


def make_job(title: str, description: str, salary: str = "20k-25k") -> Job:
    return Job(
        title=title,
        company="Demo",
        city="Shanghai",
        salary=salary,
        description=description,
        url="https://example.com/job/1",
    )


def test_salary_bonus_high_ge_40k():
    job = make_job(title="Backend", description="ETL", salary="20k-45k")
    score = score_job(job, keywords=[])
    assert score == 10


def test_salary_bonus_mid_ge_30k():
    job = make_job(title="Backend", description="ETL", salary="20k-32k")
    score = score_job(job, keywords=[])
    assert score == 5


def test_salary_bonus_invalid_string():
    job = make_job(title="Backend", description="ETL", salary="negotiable")
    score = score_job(job, keywords=[])
    assert score == 0