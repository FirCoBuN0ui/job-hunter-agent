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
- 定时任务调度（GitHub Actions `schedule` + `workflow_dispatch`）
- pytest 测试覆盖核心流程

## Quick Start

```bash
pip install -r requirements.txt
python -m pytest -q
python main.py --config config.yaml
```

## Common Commands (Windows PowerShell)

```powershell
.\scripts.ps1 test
.\scripts.ps1 run
.\scripts.ps1 demo
.\scripts.ps1 stats
.\scripts.ps1 history
.\scripts.ps1 history-date
.\scripts.ps1 dry-run
.\scripts.ps1 clean
```

## Architecture

- `src/adapters.py`：各来源适配 + 注册表分发
- `src/pipeline.py`：加载/去重/导出流程
- `src/scorer.py`：关键词评分
- `src/storage.py`：SQLite 持久化、历史查询、统计
- `main.py`：CLI 入口与运行模式路由

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
├─ .github/workflows/
│  ├─ ci.yml
│  └─ schedule.yml
├─ main.py
├─ config.yaml
├─ requirements.txt
└─ scripts.ps1
```

## Roadmap

### Done
- ✅ v5-4 CI 自动测试
- ✅ v6-1 数据源增量同步（去重写入）
- ✅ v6-2 定时任务调度（`schedule` + `workflow_dispatch`）

### Next (optional)
- [ ] 真实数据源适配器（合规接入）
- [ ] 通知能力（邮件 / webhook）
- [ ] Docker 化部署

## Scheduling Instructions

- `cron` 使用 UTC 时间。
- 支持 `workflow_dispatch` 手动触发。
- 建议先用 `--dry-run` 验证调度链路，再切换到真实写入。