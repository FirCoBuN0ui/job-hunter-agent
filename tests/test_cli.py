import subprocess
import sys


def test_cli_generates_report(tmp_path):
    out_json = tmp_path / "out.json"
    out_md = tmp_path / "out.md"

    cmd = [
        sys.executable,
        "main.py",
        "--input", "data/jobs_mock.json",
        "--keywords", "python", "api",
        "--top", "2",
        "--out", str(out_json),
        "--out-md", str(out_md),
        "--min-score", "30",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0
    assert out_json.exists()
    assert out_md.exists()
    