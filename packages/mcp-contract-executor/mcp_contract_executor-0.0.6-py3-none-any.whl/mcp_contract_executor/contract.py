from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Contract:
    goal: str
    scope_allow: list[str]
    scope_deny: list[str]
    acceptance: list[str]
    questions: list[str]
    risk_flags: list[str]
    context_budget: dict[str, int]
    raw: dict[str, Any]


def _list(data: dict[str, Any], key: str) -> list[str]:
    val = data.get(key)
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    return []


def load_contract(repo_root: Path) -> Contract:
    path = repo_root / ".codex" / "contract.json"
    if not path.is_file():
        raise FileNotFoundError(f"contract.json not found at {path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"contract.json invalid JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError("contract.json must be an object")

    goal = str(raw.get("goal") or "").strip()
    if not goal:
        raise ValueError("contract.goal is required")

    questions = _list(raw, "questions")
    if questions:
        raise ValueError(f"contract.questions must be resolved: {', '.join(questions[:5])}")

    budget_raw = raw.get("context_budget") if isinstance(raw.get("context_budget"), dict) else {}
    context_budget = {
        "max_files": int(budget_raw.get("max_files") or 20),
        "max_lines_per_file": int(budget_raw.get("max_lines_per_file") or 400),
        "max_snippets": int(budget_raw.get("max_snippets") or 10),
    }

    return Contract(
        goal=goal,
        scope_allow=_list(raw, "scope_allow"),
        scope_deny=_list(raw, "scope_deny"),
        acceptance=_list(raw, "acceptance"),
        questions=questions,
        risk_flags=_list(raw, "risk_flags"),
        context_budget=context_budget,
        raw=raw,
    )
