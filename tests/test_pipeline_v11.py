from src.models import Job
from src.pipeline import deduplicate_jobs, save_report_md


def test_deduplicate_jobs_by_url(tmp_path):
    jobs = [
        Job("t1", "c1", "sh", "10k", "python", "u1"),
        Job("t2", "c2", "bj", "20k", "java", "u1"),  # duplicate url
        Job("t3", "c3", "sz", "30k", "go", "u2"),
    ]
    unique = deduplicate_jobs(jobs)
    assert len(unique) == 2
    assert unique[0].url == "u1"
    assert unique[1].url == "u2"


def test_save_report_md(tmp_path):
    out = tmp_path / "report.md"
    items = [
        {
            "title": "Python Backend Engineer",
            "company": "A Tech",
            "city": "Shanghai",
            "salary": "25k-35k",
            "url": "https://example.com/1",
            "score": 85,
        }
    ]
    save_report_md(items, str(out))
    text = out.read_text(encoding="utf-8")
    assert "# Job Hunter Report" in text
    assert "| Rank | Title |" in text
    assert "Python Backend Engineer" in text