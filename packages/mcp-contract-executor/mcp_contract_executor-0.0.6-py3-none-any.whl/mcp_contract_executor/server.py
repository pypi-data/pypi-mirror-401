from __future__ import annotations

from typing import Any, cast

from fastmcp import FastMCP

from .runtime.worker import worker


def _require_cwd(options: dict[str, Any]) -> str:
    cwd = options.get("cwd") if isinstance(options, dict) else None
    if not isinstance(cwd, str) or not cwd.strip():
        raise ValueError("options.cwd is required (absolute path inside repo)")
    return cwd


def build_server() -> FastMCP:
    server = FastMCP(log_level="ERROR")

    @server.tool(name="squad_start")
    def squad_start(cwd: str, query: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            state = worker.start(cwd=cwd, query=query, options=options or {})
        except Exception as exc:
            return {
                "run_id": "",
                "forced_wait_s": 0,
                "event_lines": [f"error: {str(exc)[:160]}"],
                "next_step": "stop polling; print event_lines once",
            }
        return state.to_json()

    @server.tool(name="squad_status")
    def squad_status(run_id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        opts = cast(dict[str, Any], options or {})
        try:
            cwd = _require_cwd(opts)
        except Exception as exc:
            return {
                "run_id": run_id,
                "forced_wait_s": 0,
                "event_lines": [f"error: {str(exc)[:160]}"],
                "next_step": "stop polling; print event_lines once",
            }
        if bool(opts.get("cancel")):
            worker.cancel(cwd=cwd, run_id=run_id, reason=str(opts.get("cancel_reason") or "").strip() or None)
        return worker.status(cwd=cwd, run_id=run_id)

    return server


def run_server(*, transport: str = "stdio") -> None:
    if transport != "stdio":
        raise ValueError("unsupported transport")
    build_server().run(transport=transport)
