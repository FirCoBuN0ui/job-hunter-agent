from src.pipeline import load_jobs


def test_load_jobs_from_csv():
    jobs = load_jobs("data/jobs_mock.csv")
    assert len(jobs) == 3
    assert jobs[0].title == "Python Backend Engineer"
    assert jobs[0].url == "https://example.com/1"