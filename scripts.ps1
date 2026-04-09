param(
  [string]$task = "run"
)

switch ($task) {
  "test"        { python -m pytest -q }
  "run"         { python main.py --config config.yaml }
  "demo"        { python main.py --source local --input data/jobs_mock.csv --keywords python,api --top 5 --db jobs.db --export-csv topn.csv }
  "stats"       { python main.py --stats --db jobs.db }
  "history"     { python main.py --history 10 --db jobs.db --history-out-md history.md }
  "history-date"{ python main.py --history-date 2026-04-09 --db jobs.db --history-out-md history_2026-04-09.md }
  "dry-run"     { python main.py --source lagou --input data/lagou_mock.json --keywords python,etl --top 5 --dry-run }
  "clean"       { python -c "import os; [os.remove(x) for x in ['jobs.db','jobs_report.json','jobs_report.md','topn.csv','history.md','history_2026-04-09.md'] if os.path.exists(x)]" }
  default       { Write-Host "Unknown task: $task"; exit 1 }
}