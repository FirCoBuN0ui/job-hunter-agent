# v6 阶段验收页（job-hunter-agent）

## 1) 本阶段目标
- 目标一句话：完善环境友好性与核心功能闭环。
- 范围（做了什么）：
  1. 数据源增量同步（去重写入）
  2. 文档与脚本统一到 `scripts.ps1`
  3. 增加定时任务 workflow（schedule + 手动触发）
- 非目标（明确没做什么）：
  1. 真实数据源适配器
  2. 权重配置化
  3. 通知能力
  4. Docker 化部署

## 2) 验收结果
- [x] 本地测试通过（`pytest -q`）
- [x] GitHub Actions 通过（CI）
- [x] 定时任务可手动触发（`workflow_dispatch`）
- [x] 增量入库生效（重复数据不重复写入）
- [x] README 与实际脚本一致（`scripts.ps1`）

结论：通过  
日期：2026-04-10

## 3) 关键证据

- 证据1：本地测试
  ```text
  PS E:\Python-learning\job-hunter-agent> python -m pytest -q
  ....................
  [100%]
  20 passed in 0.47s
  ```

- 证据2：CI workflow
  - https://github.com/FirCoBuN0ui/job-hunter-agent/actions/workflows/ci.yml

- 证据3：Schedule workflow（支持手动触发）
  - https://github.com/FirCoBuN0ui/job-hunter-agent/actions/workflows/schedule.yml

- 证据4：增量入库（同一输入连续执行两次）
  ```text
  # Run 1 (2026-04-10 17:27:48)
  DB upsert done: inserted=3, attempted=3, db=jobs.db

  # Run 2 (2026-04-10 17:27:53)
  DB upsert done: inserted=0, attempted=3, db=jobs.db
  ```

## 4) 已知风险与限制
- 风险1：当前以 mock/本地数据为主，真实源稳定性未验证  
  - 影响：线上可用性不确定  
  - 临时缓解：保留 adapter 接口，先做 dry-run 验证链路
- 风险2：定时任务仅基础可用，告警与失败通知缺失  
  - 影响：失败时无法第一时间感知  
  - 临时缓解：手动巡检 Actions 运行记录

## 5) 经验复盘（决策质量）
- 做对的 3 件事：
  1. 先完成核心闭环（功能→测试→CI→调度）
  2. 增量入库交给数据库约束，降低重复写入风险
  3. 统一脚本入口，提升日常操作一致性
- 做错/可改进的 2 件事：
  1. 文档更新滞后于功能变更
  2. 变更后影响面检查不够系统（调用链联动）
- 下次会提前做的 1 件事：
  - 每次迭代结束先跑“文档一致性检查清单”。

## 6) 下阶段候选（最多 3 项）
- 候选A：真实数据源适配（合规前提）
  - 价值：显著提升真实可用性
  - 成本：反爬、稳定性与解析维护
  - 风险：合法合规与源变更频繁
- 候选B：通知能力（邮件/Webhook）
  - 价值：形成“运行结果触达”闭环
  - 成本：中等（模板 + 配置 + 重试）
  - 风险：通知噪声与失败重试策略
- 候选C：Docker 化部署
  - 价值：提升可移植性与复现效率
  - 成本：中等（镜像、运行参数、存储卷）
  - 风险：环境变量与数据卷管理复杂度上升

## 7) Go / No-Go 决策
- 决策：阶段收官，转新项目
- 理由（3条以内）：
  1. 当前版本已具备完整工程闭环（功能、测试、CI、调度）
  2. 继续深挖同项目的边际学习收益下降
  3. 更适合在新项目中复用并巩固方法论