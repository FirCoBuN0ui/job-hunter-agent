from src.storage import init_db, save_ranked_jobs, fetch_recent_jobs


def test_incremental_insert_ignore_duplicates(tmp_path):
    db = tmp_path / "inc.db"
    init_db(str(db))

    rows = [
        {
            "title": "Python Backend Engineer",
            "company": "A Tech",
            "city": "Shanghai",
            "salary": "25k-35k",
            "url": "https://example.com/1",
            "score": 80,
        },
        {
            "title": "Data Engineer",
            "company": "B Tech",
            "city": "Beijing",
            "salary": "20k-30k",
            "url": "https://example.com/2",
            "score": 60,
        },
    ]

    inserted1 = save_ranked_jobs(rows, db_path=str(db), run_at="2026-04-09T12:00:00")
    inserted2 = save_ranked_jobs(rows, db_path=str(db), run_at="2026-04-09T12:10:00")

    assert inserted1 == 2
    assert inserted2 == 0

    all_rows = fetch_recent_jobs(limit=10, db_path=str(db))
    assert len(all_rows) == 2