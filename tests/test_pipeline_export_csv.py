from src.pipeline import save_report_csv


def test_save_report_csv(tmp_path):
    out = tmp_path / "topn.csv"
    rows = [
        {
            "title": "Python Backend Engineer",
            "company": "A Tech",
            "city": "Shanghai",
            "salary": "25k-35k",
            "score": 80,
            "url": "https://example.com/1",
        },
        {
            "title": "Data Engineer",
            "company": "B Tech",
            "city": "Beijing",
            "salary": "20k-30k",
            "score": 65,
            "url": "https://example.com/2",
        },
    ]
    save_report_csv(rows, str(out))
    text = out.read_text(encoding="utf-8")
    assert "title,company,city,salary,score,url" in text
    assert "Python Backend Engineer" in text
    assert "Data Engineer" in text