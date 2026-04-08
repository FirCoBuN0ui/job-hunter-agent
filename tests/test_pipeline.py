from pathlib import Path
from src.pipeline import load_jobs, rank_jobs, save_report_json


def test_load_jobs():
    jobs = load_jobs("data/jobs_mock.json")
    assert len(jobs) >= 5
    assert jobs[0].title


def test_rank_jobs_sorted_desc():
    jobs = load_jobs("data/jobs_mock.json")
    ranked = rank_jobs(jobs, ["python", "api", "fastapi"])
    assert len(ranked) == len(jobs)
    assert ranked[0]["score"] >= ranked[-1]["score"]


def test_save_report_json(tmp_path):
    out = tmp_path / "report.json"
    sample = [{"title": "t1", "score": 80}]
    save_report_json(sample, str(out))
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert '"title": "t1"' in content