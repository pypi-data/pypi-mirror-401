from __future__ import annotations

import json
import subprocess
import threading
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from ..contract import load_contract
from .dispatch import run_codex_exec


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _lease_expiry(ttl_s: int) -> str:
    return (_utc_now() + timedelta(seconds=max(10, ttl_s or 0))).isoformat()


def _layout(repo_root: Path, run_id: str) -> dict[str, Path]:
    base = repo_root / ".codex" / "contract-executor"
    run_dir = base / "runs" / run_id
    return {
        "base": base,
        "run_dir": run_dir,
        "state": run_dir / "state.json",
        "jobs": run_dir / "jobs",
        "artifacts": run_dir / "artifacts",
        "report": run_dir / "artifacts" / "report.md",
        "diffstat": run_dir / "artifacts" / "diffstat.txt",
    }


@dataclass
class RunState:
    run_id: str
    repo_root: str
    cwd: str
    query: str
    goal: str
    sandbox: str
    approval_policy: str
    coder_model: str
    coder_reasoning_effort: str
    coder_extra_config: list[str]
    phase: str
    next_action: str
    wait_reason: str
    canceled: bool
    lease_ttl_s: int
    lease_expires_at: str
    created_at: str
    updated_at: str
    important_event: str
    forced_wait_ms: int
    event_lines: list[str]
    events: list[dict[str, Any]]
    job_id: str | None

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "RunState":
        return cls(
            run_id=str(data.get("run_id") or ""),
            repo_root=str(data.get("repo_root") or ""),
            cwd=str(data.get("cwd") or ""),
            query=str(data.get("query") or ""),
            goal=str(data.get("goal") or ""),
            sandbox=str(data.get("sandbox") or "workspace-write"),
            approval_policy=str(data.get("approval_policy") or "never"),
            coder_model=str(data.get("coder_model") or "gpt-5.1-codex-mini"),
            coder_reasoning_effort=str(data.get("coder_reasoning_effort") or "medium"),
            coder_extra_config=[str(x) for x in (data.get("coder_extra_config") or []) if str(x).strip()],
            phase=str(data.get("phase") or "coder_run"),
            next_action=str(data.get("next_action") or "wait"),
            wait_reason=str(data.get("wait_reason") or "agent_running"),
            canceled=bool(data.get("canceled") or False),
            lease_ttl_s=int(data.get("lease_ttl_s") or 120),
            lease_expires_at=str(data.get("lease_expires_at") or _lease_expiry(120)),
            created_at=str(data.get("created_at") or _utc_now().isoformat()),
            updated_at=str(data.get("updated_at") or _utc_now().isoformat()),
            important_event=str(data.get("important_event") or "initialized"),
            forced_wait_ms=int(data.get("forced_wait_ms") or 8000),
            event_lines=[str(x) for x in (data.get("event_lines") or []) if str(x).strip()][:3],
            events=[e for e in (data.get("events") or []) if isinstance(e, dict)],
            job_id=str(data.get("job_id")) if data.get("job_id") else None,
        )


def _save_state(path: Path, state: RunState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state.to_json(), ensure_ascii=False, indent=2), encoding="utf-8")


def _load_state(path: Path) -> RunState:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("state.json invalid")
    return RunState.from_json(raw)


class Worker:
    def __init__(self) -> None:
        self._lock = threading.Lock()

    def _classify(self, query: str) -> str:
        q = (query or "").lower()
        if not q.strip():
            return "medium"
        simple = ["typo", "rename", "doc", "comment", "log", "small", "tiny"]
        hard = ["architecture", "refactor", "protocol", "schema", "api", "multi", "redesign"]
        if any(k in q for k in hard):
            return "hard"
        if any(k in q for k in simple):
            return "simple"
        return "medium"

    def _update(self, *, repo_root: Path, run_id: str, mutator: Callable[[RunState], None]) -> RunState:
        with self._lock:
            paths = _layout(repo_root, run_id)
            state = _load_state(paths["state"])
            mutator(state)
            state.updated_at = _utc_now().isoformat()
            _save_state(paths["state"], state)
            return state

    def start(self, *, cwd: str, query: str, options: dict[str, Any]) -> RunState:
        repo_root = Path(cwd).resolve()
        contract = load_contract(repo_root)
        run_id = f"ssx-{uuid.uuid4().hex}"
        paths = _layout(repo_root, run_id)
        paths["run_dir"].mkdir(parents=True, exist_ok=True)
        paths["jobs"].mkdir(parents=True, exist_ok=True)
        paths["artifacts"].mkdir(parents=True, exist_ok=True)

        lease_ttl_s = int(options.get("lease_ttl_s") or 120)
        difficulty = self._classify(query)
        forced_wait_ms = 5000 if difficulty == "simple" else 10000 if difficulty == "hard" else 8000
        now = _utc_now().isoformat()
        state = RunState(
            run_id=run_id,
            repo_root=str(repo_root),
            cwd=str(Path(cwd).resolve()),
            query=query,
            goal=contract.goal,
            sandbox=str(options.get("sandbox") or "workspace-write"),
            approval_policy=str(options.get("approval_policy") or "never"),
            coder_model=str(options.get("coder_model") or "gpt-5.1-codex-mini"),
            coder_reasoning_effort=str(options.get("coder_reasoning_effort") or "medium"),
            coder_extra_config=[str(x) for x in (options.get("coder_extra_config") or []) if str(x).strip()],
            phase="coder_run",
            next_action="wait",
            wait_reason="agent_running",
            canceled=False,
            lease_ttl_s=lease_ttl_s,
            lease_expires_at=_lease_expiry(lease_ttl_s),
            created_at=now,
            updated_at=now,
            important_event=f"started coder ({difficulty})",
            forced_wait_ms=forced_wait_ms,
            event_lines=[f"started coder ({difficulty})"],
            events=[{"ts": now, "phase": "coder_run", "kind": "info", "message": f"started coder ({difficulty})"}],
            job_id=None,
        )
        _save_state(paths["state"], state)

        thread = threading.Thread(target=self._run, args=(state, contract), name=f"ssx-{run_id}", daemon=True)
        thread.start()
        return state

    def cancel(self, *, cwd: str, run_id: str, reason: str | None = None) -> None:
        repo_root = Path(cwd).resolve()

        def mut(s: RunState) -> None:
            s.canceled = True
            s.phase = "canceled"
            s.next_action = "done"
            s.wait_reason = "canceled"
            msg = f"canceled: {reason or ''}".strip() or "canceled"
            s.important_event = msg
            s.forced_wait_ms = 0
            s.event_lines = [msg][:3]
            s.events.append({"ts": _utc_now().isoformat(), "phase": "canceled", "kind": "info", "message": msg})

        try:
            self._update(repo_root=repo_root, run_id=run_id, mutator=mut)
        except Exception:
            return

    def status(self, *, cwd: str, run_id: str) -> dict[str, Any]:
        repo_root = Path(cwd).resolve()
        paths = _layout(repo_root, run_id)
        try:
            state = _load_state(paths["state"])
        except Exception as exc:
            return {
                "run_id": run_id,
                "forced_wait_s": 0,
                "event_lines": [f"error: {str(exc)[:160]}"],
                "next_step": "stop polling; print event_lines once",
            }
        terminal = state.phase in {"done", "error", "canceled"}
        if not terminal:
            state.lease_expires_at = _lease_expiry(state.lease_ttl_s)
            _save_state(paths["state"], state)
        if terminal:
            lines = [str(ev.get("message") or "").strip() for ev in state.events if isinstance(ev, dict) and str(ev.get("message") or "").strip()]
            payload_events = lines[:50] if lines else (state.event_lines or [])
        else:
            payload_events = state.event_lines[:3] if state.event_lines else []
        payload: dict[str, Any] = {
            "run_id": run_id,
            "forced_wait_s": 0 if terminal else round(max(state.forced_wait_ms, 500) / 1000, 1),
            "event_lines": payload_events,
        }
        if terminal:
            payload["next_step"] = "stop polling; print event_lines once"
            # clear events to avoid re-sending
            state.events = []
            _save_state(paths["state"], state)
        return payload

    def _run(self, state: RunState, contract) -> None:
        repo_root = Path(state.repo_root).resolve()
        paths = _layout(repo_root, state.run_id)
        job_id = f"{state.run_id}--coder"

        def should_abort() -> bool:
            try:
                cur = _load_state(paths["state"])
            except Exception:
                return False
            if cur.canceled or cur.phase == "canceled":
                return True
            try:
                exp = datetime.fromisoformat(cur.lease_expires_at)
            except Exception:
                return False
            return _utc_now() > exp

        def prompt() -> str:
            parts = [
                "You are a focused code-writing agent.",
                f"Goal: {contract.goal}",
                "Scope allow:",
                *([f"- {p}" for p in contract.scope_allow] or ["- (none)"]),
                "Scope deny:",
                *([f"- {p}" for p in contract.scope_deny] or ["- (none)"]),
                "Acceptance:",
                *([f"- {a}" for a in contract.acceptance] or ["- (none)"]),
                "Rules: keep changes minimal; avoid deps/config unless required; stay within scope; do not delete/move core configs.",
                f"User query (context only): {(state.query or '').strip()[:2000]}",
                "Apply changes directly. Do not return patches.",
            ]
            return "\n".join(parts)

        def add_event(kind: str, message: str, phase: str) -> None:
            def mut(s: RunState) -> None:
                s.events.append({"ts": _utc_now().isoformat(), "phase": phase, "kind": kind, "message": message})
                s.event_lines = [message][:3]
                s.important_event = message
                s.updated_at = _utc_now().isoformat()

            self._update(repo_root=repo_root, run_id=state.run_id, mutator=mut)

        self._update(repo_root=repo_root, run_id=state.run_id, mutator=lambda s: s.__setattr__("job_id", job_id))

        res = run_codex_exec(
            job_id=job_id,
            jobs_dir=paths["jobs"],
            prompt=prompt(),
            cwd=repo_root,
            model=state.coder_model,
            sandbox=state.sandbox,
            approval_policy=state.approval_policy,
            extra_config=[f"model_reasoning_effort=\"{state.coder_reasoning_effort}\"", *state.coder_extra_config],
            timeout_s=90,
            should_abort=should_abort,
        )

        if res.status == "aborted":
            add_event("warning", "aborted (lease/cancel)", "canceled")
            self._update(
                repo_root=repo_root,
                run_id=state.run_id,
                mutator=lambda s: (
                    s.__setattr__("phase", "canceled"),
                    s.__setattr__("next_action", "done"),
                    s.__setattr__("wait_reason", "canceled"),
                    s.__setattr__("forced_wait_ms", 0),
                ),
            )
            return
        if res.status != "completed":
            add_event("error", f"coder failed: exit={res.exit_code}", "error")
            self._update(
                repo_root=repo_root,
                run_id=state.run_id,
                mutator=lambda s: (
                    s.__setattr__("phase", "error"),
                    s.__setattr__("next_action", "done"),
                    s.__setattr__("wait_reason", "error"),
                    s.__setattr__("forced_wait_ms", 0),
                ),
            )
            return

        diffstat_path = paths["diffstat"]
        try:
            diffstat = (
                subprocess.run(
                    ["git", "-C", str(repo_root), "diff", "--stat"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    check=False,
                ).stdout.strip()
            )
            diffstat_path.write_text(diffstat or "(no diff)", encoding="utf-8")
        except Exception:
            diffstat_path.write_text("(failed to collect diffstat)", encoding="utf-8")

        report_lines = [
            "# report",
            f"- run_id: {state.run_id}",
            f"- goal: {contract.goal}",
            f"- status: completed",
            f"- diffstat: {diffstat_path}",
        ]
        paths["report"].write_text("\n".join(report_lines), encoding="utf-8")

        def mut_complete(s: RunState) -> None:
            s.phase = "done"
            s.next_action = "done"
            s.wait_reason = "completed"
            s.forced_wait_ms = 0
            s.event_lines = ["completed", f"diffstat: {diffstat_path}"][:3]
            s.events.append({"ts": _utc_now().isoformat(), "phase": "done", "kind": "info", "message": f"diffstat: {diffstat_path}"})
            s.important_event = "completed"

        self._update(repo_root=repo_root, run_id=state.run_id, mutator=mut_complete)


worker = Worker()
