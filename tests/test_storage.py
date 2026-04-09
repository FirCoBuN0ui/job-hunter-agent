from src.storage import init_db, save_ranked_jobs
import sqlite3


def test_save_ranked_jobs(tmp_path):
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
        },
        {
            "title": "Data Engineer",
            "company": "B Tech",
            "city": "Beijing",
            "salary": "20k-30k",
            "url": "https://example.com/2",
            "score": 65,
        },
    ]

    n = save_ranked_jobs(rows, db_path=str(db), run_at="2026-04-08T12:00:00")
    assert n == 2

    with sqlite3.connect(str(db)) as conn:
        cnt = conn.execute("SELECT COUNT(*) FROM ranked_jobs").fetchone()[0]
        assert cnt == 2