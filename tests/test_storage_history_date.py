from src.storage import init_db, save_ranked_jobs, fetch_jobs_by_date


def test_fetch_jobs_by_date(tmp_path):
    db = tmp_path / "test_jobs.db"
    init_db(str(db))

    rows = [
        {
            "title": "Python Backend Engineer",
            "company": "A Tech",
            "city": "Shanghai",
            "salary": "25k-35k",
            "url": "https://example.com/1",
            "score": 80,
        }
    ]


    n1 = save_ranked_jobs(rows, db_path=str(db), run_at="2026-04-09T10:00:00")
    n2 = save_ranked_jobs(rows, db_path=str(db), run_at="2026-04-08T10:00:00")

    assert n1 == 1
    assert n2 == 0

    d1 = fetch_jobs_by_date("2026-04-09", db_path=str(db))
    d2 = fetch_jobs_by_date("2026-04-08", db_path=str(db))
    d3 = fetch_jobs_by_date("2026-04-07", db_path=str(db))

    assert len(d1) == 1
    assert len(d2) == 0
    assert len(d3) == 0
