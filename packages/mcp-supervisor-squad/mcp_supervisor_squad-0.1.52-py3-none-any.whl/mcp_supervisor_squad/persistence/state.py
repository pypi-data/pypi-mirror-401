from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import math

from ..utils.storage import read_json, atomic_write_json
from ..utils.time import utc_now_iso
from ..utils.path import find_repo_root
from .storage import StorageLayout


@dataclass
class RunTask:
    slug: str
    project_root: str
    worktree: str
    job_id: str | None = None
    status: str = "pending"
    started_at: str | None = None
    finished_at: str | None = None
    error: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RunTask":
        return cls(
            slug=str(payload.get("slug") or "single"),
            project_root=str(payload.get("project_root") or ""),
            worktree=str(payload.get("worktree") or ""),
            job_id=payload.get("job_id") if isinstance(payload.get("job_id"), str) else None,
            status=str(payload.get("status") or "pending"),
            started_at=payload.get("started_at") if isinstance(payload.get("started_at"), str) else None,
            finished_at=payload.get("finished_at") if isinstance(payload.get("finished_at"), str) else None,
            error=payload.get("error") if isinstance(payload.get("error"), str) else None,
        )


@dataclass
class RunState:
    run_id: str
    repo_root: str
    cwd: str
    query: str
    sandbox: str
    approval_policy: str
    coder_model: str
    coder_reasoning_effort: str
    coder_extra_config: list[str]
    mode: str
    phase: str
    next_action: str
    wait_reason: str
    requirements_brief: str
    canceled: bool
    lease_ttl_s: int
    lease_expires_at: str
    created_at: str
    updated_at: str
    phase_started_at: str
    retention_days: int
    important_event: str
    important_event_at: str
    forced_wait_ms: int
    event_seq: int
    events: list[dict[str, Any]]
    tasks: list[RunTask]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["tasks"] = [asdict(t) for t in self.tasks]
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RunState":
        tasks = [RunTask.from_dict(t) for t in (payload.get("tasks") or []) if isinstance(t, dict)]
        return cls(
            run_id=str(payload.get("run_id") or ""),
            repo_root=str(payload.get("repo_root") or ""),
            cwd=str(payload.get("cwd") or ""),
            query=str(payload.get("query") or ""),
            sandbox=str(payload.get("sandbox") or "workspace-write"),
            approval_policy=str(payload.get("approval_policy") or "never"),
            coder_model=str(payload.get("coder_model") or "gpt-5.1-codex-mini"),
            coder_reasoning_effort=str(payload.get("coder_reasoning_effort") or "medium"),
            coder_extra_config=[str(x) for x in (payload.get("coder_extra_config") or []) if str(x).strip()],
            mode=str(payload.get("mode") or "single"),
            phase=str(payload.get("phase") or "coder_run"),
            next_action=str(payload.get("next_action") or "wait"),
            wait_reason=str(payload.get("wait_reason") or "agent_running"),
            requirements_brief=str(payload.get("requirements_brief") or ""),
            canceled=bool(payload.get("canceled") or False),
            lease_ttl_s=int(payload.get("lease_ttl_s") or 120),
            lease_expires_at=str(payload.get("lease_expires_at") or utc_now_iso()),
            created_at=str(payload.get("created_at") or utc_now_iso()),
            updated_at=str(payload.get("updated_at") or utc_now_iso()),
            phase_started_at=str(payload.get("phase_started_at") or payload.get("important_event_at") or payload.get("created_at") or utc_now_iso()),
            retention_days=int(payload.get("retention_days") or 10),
            important_event=str(payload.get("important_event") or "initialized"),
            important_event_at=str(payload.get("important_event_at") or utc_now_iso()),
            forced_wait_ms=int(payload.get("forced_wait_ms") or 8000),
            event_seq=int(payload.get("event_seq") or 0),
            events=[e for e in (payload.get("events") or []) if isinstance(e, dict)],
            tasks=tasks,
        )

    def public_status(self, *, options: dict[str, Any] | None = None) -> dict[str, Any]:
        poll_ms = 0 if self.phase in {"done", "error", "canceled"} else int(self.forced_wait_ms or 8000)

        events_lines: list[str] = []
        for ev in list(self.events or []):
            if not isinstance(ev, dict):
                continue
            msg = str(ev.get("message") or "").strip()
            if msg:
                events_lines.append(msg)
        if self.phase in {"done", "canceled", "error"}:
            poll_ms = 0
            self.forced_wait_ms = 0
        else:
            self.forced_wait_ms = poll_ms
        terminal = self.phase in {"done", "canceled", "error"}
        display_events = events_lines if terminal else events_lines[-3:]
        payload = {"run_id": self.run_id, "forced_wait_s": math.ceil(poll_ms / 100) / 10.0}
        if display_events:
            payload["event_lines"] = display_events[:3]
        if terminal:
            payload["next_step"] = "stop polling; print event_lines once"
            self.events = []
        return payload


class RunStore:
    def __init__(self) -> None:
        self._lock = None

    def _layout(self, *, cwd: str | None = None) -> StorageLayout:
        root = find_repo_root(Path(cwd).resolve()) if cwd else find_repo_root(Path.cwd())
        return StorageLayout.for_repo(root)

    def load(self, run_id: str, *, cwd: str | None = None) -> RunState:
        layout = self._layout(cwd=cwd)
        state_path = layout.run_paths(run_id).state_path
        raw = read_json(state_path)
        if not raw:
            if cwd is None:
                raise FileNotFoundError(
                    f"run_id not found in current repo: {run_id}. Pass options.cwd pointing inside the target repo that created this run."
                )
            raise FileNotFoundError(f"run_id not found: {run_id}")
        return RunState.from_dict(raw)

    def save(self, state: RunState) -> None:
        layout = StorageLayout.for_repo(Path(state.repo_root))
        paths = layout.run_paths(state.run_id)
        paths.run_dir.mkdir(parents=True, exist_ok=True)
        atomic_write_json(paths.state_path, state.to_dict())
