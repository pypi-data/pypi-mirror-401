# mcp-contract-executor

极简版 contract-first MCP server。仅四个核心文件：`server.py`、`worker.py`、`dispatch.py`、`contract.py`。

工作流：
1) 主会话生成并覆盖写 `/.codex/contract.json`（questions 需为空）。
2) 调用 `squad_start(cwd, query, options?)` 启动一次执行；返回 ≤3 行 digest。
3) 按 `forced_wait_s` 轮询 `squad_status(run_id, options={"cwd":...})` 续租；需要时 `cancel=true`。
4) 断联超过 lease_ttl（默认 120s）自动中止 codex；终态包含 artifact 提示（diffstat/report）。

存储：`<repo>/.codex/contract-executor/runs/<run_id>/`（state.json、artifacts/diffstat.txt、report.md、jobs/*）。
