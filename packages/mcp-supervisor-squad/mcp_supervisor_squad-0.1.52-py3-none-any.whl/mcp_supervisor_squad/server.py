from __future__ import annotations

from typing import Any, cast
from fastmcp import FastMCP

from .runtime.worker import worker
from .utils.time import utc_now_iso

APP_ID = "mcp-supervisor-squad"


def _require_cwd(options: dict[str, Any]) -> str:
    cwd = options.get("cwd") if isinstance(options, dict) else None
    if not isinstance(cwd, str) or not cwd.strip():
        raise ValueError("options.cwd is required and must be an absolute path inside the target repo.")
    return cwd


def build_server() -> FastMCP:
    # Default to a quiet log level so stdout stays clean for JSON-RPC.
    server = FastMCP(log_level="ERROR")
    store = worker._store

    @server.tool(name="squad_start")
    def squad_start(cwd: str, query: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        _ = options or {}
        try:
            state = worker.start(cwd=cwd, query=query, options=options or {})
        except Exception as exc:
            return {
                "run_id": "",
                "forced_wait_s": 0,
                "event_lines": [f"error: {str(exc)[:160]}"],
                "next_step": "stop polling; print event_lines once",
            }
        store.save(state)
        return state.public_status()

    @server.tool(name="squad_status")
    def squad_status(run_id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        resolved_options = cast(dict[str, Any], options or {})
        try:
            cwd = _require_cwd(resolved_options)
        except Exception as exc:
            return {
                "run_id": run_id,
                "event_lines": [
                    "错误: squad_status 需要 options.cwd（绝对路径）",
                    "示例: options={\"cwd\":\"/Volumes/workspace/.../<repo>\"}",
                    f"原因: {str(exc)[:120]}",
                ][:3],
                "forced_wait_s": 0,
                "next_step": "stop polling; print event_lines once",
            }
        if bool(resolved_options.get("cancel")):
            try:
                _ = worker.cancel(run_id=run_id, cwd=cwd, reason=str(resolved_options.get("cancel_reason") or "").strip() or None)
            except Exception:
                pass
        try:
            state = store.load(run_id, cwd=cwd)
        except Exception as exc:
            return {
                "run_id": run_id,
                "event_lines": [
                    "错误: 找不到 run（请确认 run_id 与 cwd 匹配）",
                    f"原因: {str(exc)[:120]}",
                ][:3],
                "forced_wait_s": 0,
                "next_step": "stop polling; print event_lines once",
            }
        terminal = state.phase in {"done", "error", "canceled"}
        if not terminal:
            state.lease_expires_at = worker._lease_expiry(state.lease_ttl_s)
            state.updated_at = utc_now_iso()
        payload = state.public_status(options=resolved_options)
        store.save(state)
        return payload

    return server


def run_server(*, transport: str = "stdio") -> None:
    if transport != "stdio":
        raise ValueError(f"Unsupported transport '{transport}'.")
    server = build_server()
    server.run(transport=transport)
