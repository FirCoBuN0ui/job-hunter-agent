from src.storage import init_db, save_ranked_jobs, fetch_stats


def test_fetch_stats(tmp_path):
    db = tmp_path / "stats.db"
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
        {
            "title": "AI Platform Engineer",
            "company": "A Tech",
            "city": "Shanghai",
            "salary": "30k-45k",
            "url": "https://example.com/3",
            "score": 90,
        },
    ]

    save_ranked_jobs(rows, db_path=str(db), run_at="2026-04-09T12:00:00")
    s = fetch_stats(db_path=str(db))

    assert s["total"] == 3
    assert int(s["avg_score"]) == 76  # 76.66...
    assert s["max_score"] == 90
    assert s["top_cities"][0]["city"] == "Shanghai"
    assert s["top_companies"][0]["company"] == "A Tech"