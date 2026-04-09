import sqlite3
from pathlib import Path


def init_db(db_path: str = "jobs.db") -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True) if Path(db_path).parent != Path("") else None
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ranked_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_at TEXT NOT NULL,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                city TEXT NOT NULL,
                salary TEXT NOT NULL,
                url TEXT NOT NULL,
                score INTEGER NOT NULL,
                UNIQUE(title, company, city, url)
            )
            """
        )
        
        conn.commit()
    finally:
        conn.close()


def save_ranked_jobs(rows, db_path="jobs.db", run_at=None) -> int:
    run_at = run_at or datetime.now().isoformat(timespec="seconds")
    inserted = 0

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        for r in rows:
            cur.execute(
                """
                INSERT OR IGNORE INTO ranked_jobs
                (title, company, city, salary, url, score, run_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    r.get("title", ""),
                    r.get("company", ""),
                    r.get("city", ""),
                    r.get("salary", ""),
                    r.get("url", ""),
                    int(r.get("score", 0)),
                    run_at,
                ),
            )
            inserted += cur.rowcount  # 插入成���=1，被忽略=0
        conn.commit()

    return inserted

def fetch_recent_jobs(limit: int = 10, db_path: str = "jobs.db") -> list[dict]:
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(
            """
            SELECT run_at, title, company, city, salary, url, score
            FROM ranked_jobs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cur.fetchall()

    return [
        {
            "run_at": r[0],
            "title": r[1],
            "company": r[2],
            "city": r[3],
            "salary": r[4],
            "url": r[5],
            "score": r[6],
        }
        for r in rows
    ]

def fetch_jobs_by_date(date_str: str, db_path: str = "jobs.db") -> list[dict]:
    """
    按日期查询，date_str 格式: YYYY-MM-DD
    run_at 是 ISO 字符串，如 2026-04-09T13:19:37
    用 LIKE '2026-04-09%' 过滤当天
    """
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(
            """
            SELECT run_at, title, company, city, salary, url, score
            FROM ranked_jobs
            WHERE run_at LIKE ?
            ORDER BY id DESC
            """,
            (f"{date_str}%",),
        )
        rows = cur.fetchall()

    return [
        {
            "run_at": r[0],
            "title": r[1],
            "company": r[2],
            "city": r[3],
            "salary": r[4],
            "url": r[5],
            "score": r[6],
        }
        for r in rows
    ]

def fetch_stats(db_path: str = "jobs.db") -> dict:
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*), AVG(score), MAX(score) FROM ranked_jobs")
        total, avg_score, max_score = cur.fetchone()

        cur.execute(
            """
            SELECT city, COUNT(*) AS c
            FROM ranked_jobs
            GROUP BY city
            ORDER BY c DESC, city ASC
            LIMIT 5
            """
        )
        top_cities = [{"city": r[0], "count": r[1]} for r in cur.fetchall()]

        cur.execute(
            """
            SELECT company, COUNT(*) AS c
            FROM ranked_jobs
            GROUP BY company
            ORDER BY c DESC, company ASC
            LIMIT 5
            """
        )
        top_companies = [{"company": r[0], "count": r[1]} for r in cur.fetchall()]

    return {
        "total": int(total or 0),
        "avg_score": float(avg_score or 0.0),
        "max_score": int(max_score or 0),
        "top_cities": top_cities,
        "top_companies": top_companies,
    }