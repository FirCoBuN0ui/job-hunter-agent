# Job Hunter Agent

一个可扩展的岗位数据处理 CLI 工具：支持多来源输入、统一模型、关键词打分、报告导出、历史查询与统计分析。

## Features

- 多来源输入（`local/boss/lagou`）
- Adapter + Registry 可扩展架构
- 岗位去重、关键词打分、TopN筛选
- 导出：JSON / Markdown / CSV
- SQLite 持久化
- 历史查询：`--history` / `--history-date`
- 统计分析：`--stats`
- 配置驱动：`--config config.yaml`
- 预览模式：`--dry-run`
- pytest 测试覆盖核心流程

## Quick Start

```bash
pip install -r requirements.txt
python -m pytest -q
python main.py --config config.yaml
```

## Common Commands

```bash
# 正常运行（配置驱动）
python main.py --config config.yaml

# CLI覆盖配置
python main.py --config config.yaml --top 2 --keywords python,etl

# 预览模式（不写文件/不入库）
python main.py --source lagou --input data/lagou_mock.json --keywords python,etl --top 5 --dry-run

# 导出 CSV
python main.py --source local --input data/jobs_mock.csv --keywords python,api --top 5 --export-csv topn.csv --db jobs.db

# 历史查询
python main.py --history 10 --db jobs.db
python main.py --history-date 2026-04-09 --db jobs.db --history-out-md history_2026-04-09.md

# 统计摘要
python main.py --stats --db jobs.db
```

## Architecture

- `src/adapters.py`：各来源适配 + 注册表分发
- `src/pipeline.py`：加载/去重/导出流程
- `src/scorer.py`：关键词评分
- `src/storage.py`：SQLite 持久化、历史查询、统计
- `main.py`：CLI入口与运行模式路由

## Project Structure

```text
.
├─ data/
├─ src/
│  ├─ adapters.py
│  ├─ models.py
│  ├─ pipeline.py
│  ├─ scorer.py
│  └─ storage.py
├─ tests/
├─ main.py
├─ config.yaml
├─ requirements.txt
└─ Makefile
```

## Roadmap

- [ ] v5-2 参数优先级单元测试完善
- [ ] v5-3 日志落盘与轮转
- [ ] v5-4 CI（GitHub Actions）自动测试
- [ ] v6 数据源增量同步与任务调度
