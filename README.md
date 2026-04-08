# Job Hunter Agent

一个可配置的岗位筛选与评分工具（Python），用于从职位数据中快速产出 TopN 推荐结果（JSON + Markdown 报告）。

## Features

- 职位数据模型（`Job`）
- 关键词评分引擎（`score_job`）
- 去重（按 `url`）
- 排序与 TopN 截断
- 最低分过滤（`--min-score`）
- 双报告导出：
  - `jobs_report.json`
  - `jobs_report.md`
- CLI 命令行参数支持
- `pytest` 自动化测试（核心逻辑 + CLI）

---

## Project Structure

```text
job-hunter-agent/
├─ data/
│  └─ jobs_mock.json
├─ src/
│  ├─ __init__.py
│  ├─ models.py
│  ├─ scorer.py
│  ├─ pipeline.py
│  └─ logger.py
├─ tests/
│  ├─ test_scorer.py
│  ├─ test_pipeline.py
│  ├─ test_pipeline_v11.py
│  └─ test_cli.py
├─ main.py
├─ README.md
└─ .gitignore
```

---

## Quick Start

### 1) Create venv

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -U pip
pip install pytest
```

### 3) Run tests

```bash
python -m pytest -q
```

### 4) Run CLI

```bash
python main.py --input data/jobs_mock.json --keywords python api remote --min-score 30 --top 5 --out jobs_report.json --out-md jobs_report.md --log-level INFO
```

---

## CLI Arguments

- `--input`：输入职位 JSON 文件路径（默认 `data/jobs_mock.json`）
- `--keywords`：关键词列表（空格分隔）
- `--top`：输出前 N 条
- `--min-score`：最低分过滤阈值（0-100）
- `--out`：JSON 报告输出路径
- `--out-md`：Markdown 报告输出路径
- `--log-level`：日志级别（`DEBUG/INFO/WARNING/ERROR`）

---

## Scoring Rule (v1)

当前版本为规则打分（可解释）：

- 每命中一个关键词：+20
- 包含 `remote` 或 `远程`：+10
- 包含 `python`：+15
- 最终分数上限：100

> 说明：这是 v1 baseline，后续可升级为加权规则 / 语义匹配 / LLM 评估。

---

## Testing Strategy

- **单元测试**
  - `test_scorer.py`：评分逻辑
  - `test_pipeline.py`：加载、排序、JSON 导出
  - `test_pipeline_v11.py`：去重、Markdown 导出
- **集成测试**
  - `test_cli.py`：命令行调用 + 产物文件校验

---

## Roadmap

- [ ] 接入真实招聘数据源（爬虫/API）
- [ ] 增加反爬与重试机制
- [ ] 增加字段标准化（薪资/城市）
- [ ] 引入 SQLite 持久化
- [ ] 增加 GitHub Actions CI

---
