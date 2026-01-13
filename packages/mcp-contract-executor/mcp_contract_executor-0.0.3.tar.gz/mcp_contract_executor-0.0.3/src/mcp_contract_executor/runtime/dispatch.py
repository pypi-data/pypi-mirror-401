from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class JobArtifacts:
    job_dir: Path
    stdout_jsonl: Path
    stderr_log: Path
    last_message: Path
    meta_path: Path


@dataclass(frozen=True, slots=True)
class JobResult:
    job_id: str
    status: str
    exit_code: int
    artifacts: JobArtifacts


def run_codex_exec(
    *,
    job_id: str,
    jobs_dir: Path,
    prompt: str,
    cwd: Path,
    model: str,
    sandbox: str,
    approval_policy: str,
    extra_config: list[str] | None = None,
    timeout_s: int | None = None,
    should_abort: Callable[[], bool] | None = None,
) -> JobResult:
    jobs_dir.mkdir(parents=True, exist_ok=True)
    job_dir = jobs_dir / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = job_dir / "stdout.jsonl"
    stderr_path = job_dir / "stderr.log"
    last_msg_path = job_dir / "last_message.txt"
    meta_path = job_dir / "meta.json"

    cmd: list[str] = ["codex", "-a", approval_policy, "-m", model, "-s", sandbox]
    for cfg in extra_config or []:
        if cfg:
            cmd += ["-c", cfg]
    cmd += [
        "exec",
        "-C",
        str(cwd),
        "--skip-git-repo-check",
        "--json",
        "--color",
        "never",
        "--output-last-message",
        str(last_msg_path),
        "-",
    ]

    meta: dict[str, Any] = {
        "id": job_id,
        "created_at": time.time(),
        "status": "running",
        "pid": None,
        "cwd": str(cwd),
        "command": cmd,
        "timeout_s": timeout_s,
        "artifacts": {
            "job_dir": str(job_dir),
            "stdout_jsonl": str(stdout_path),
            "stderr_log": str(stderr_path),
            "last_message": str(last_msg_path),
        },
    }

    env_vars = os.environ.copy()

    with stdout_path.open("wb") as out, stderr_path.open("wb") as err:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=out, stderr=err, env=env_vars)
        assert proc.stdin is not None
        meta["pid"] = proc.pid
        meta_path.write_text(str(meta), encoding="utf-8")
        proc.stdin.write((prompt or "").encode("utf-8"))
        proc.stdin.close()

        deadline = time.monotonic() + timeout_s if timeout_s else None
        exit_code: int | None = None
        while exit_code is None:
            if should_abort and should_abort():
                try:
                    proc.terminate()
                except Exception:
                    pass
                try:
                    exit_code = proc.wait(timeout=5)
                except Exception:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                    try:
                        exit_code = proc.wait(timeout=5)
                    except Exception:
                        exit_code = -9
                return JobResult(
                    job_id=job_id,
                    status="aborted",
                    exit_code=int(exit_code),
                    artifacts=JobArtifacts(
                        job_dir=job_dir,
                        stdout_jsonl=stdout_path,
                        stderr_log=stderr_path,
                        last_message=last_msg_path,
                        meta_path=meta_path,
                    ),
                )
            if deadline and time.monotonic() > deadline:
                try:
                    proc.terminate()
                except Exception:
                    pass
                try:
                    exit_code = proc.wait(timeout=5)
                except Exception:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                    try:
                        exit_code = proc.wait(timeout=5)
                    except Exception:
                        exit_code = -9
                return JobResult(
                    job_id=job_id,
                    status="failed",
                    exit_code=int(exit_code),
                    artifacts=JobArtifacts(
                        job_dir=job_dir,
                        stdout_jsonl=stdout_path,
                        stderr_log=stderr_path,
                        last_message=last_msg_path,
                        meta_path=meta_path,
                    ),
                )
            try:
                exit_code = proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                exit_code = None
            except Exception:
                exit_code = proc.poll()

    status = "completed" if exit_code == 0 else "failed"
    return JobResult(
        job_id=job_id,
        status=status,
        exit_code=int(exit_code or 1),
        artifacts=JobArtifacts(
            job_dir=job_dir,
            stdout_jsonl=stdout_path,
            stderr_log=stderr_path,
            last_message=last_msg_path,
            meta_path=meta_path,
        ),
    )
