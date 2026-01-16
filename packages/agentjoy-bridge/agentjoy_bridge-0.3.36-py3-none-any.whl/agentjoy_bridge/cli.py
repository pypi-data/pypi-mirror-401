#!/usr/bin/env python3
"""
AgentJoy Bridge
================

A tiny, dependency-free bridge that converts tool/agent activity into AgentJoy run events.

Supported integrations (Phase 1):
- OpenAI Codex CLI (non-interactive JSON mode)
- Claude Code hooks (command hooks / plugin hooks)
- ChatGPT Apps SDK template (separate folder)

This file is intentionally "single file" for beginner-friendly setup.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import queue
import subprocess
import sys
import sysconfig
import threading
import time
import traceback
import socket
import platform
import webbrowser
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse

DEFAULT_API_BASE = "http://127.0.0.1:8000"

try:
    # When run as a module: `python -m agentjoy_bridge` (recommended)
    from . import __version__ as BRIDGE_VERSION
except Exception:
    # When executed as a bare file (less common)
    BRIDGE_VERSION = "dev"


def _is_windows() -> bool:
    return os.name == "nt"


# ---------------------------
# Backend schema compatibility
# ---------------------------

# These sets mirror backend validation (Pydantic Literals).
# Keeping the bridge strict avoids 422 errors and makes the UX predictable.
VALID_EVENT_TYPES = {
    "run.created",
    "phase.started",
    "phase.progress",
    "tool.called",
    "tool.completed",
    "artifact.ready",
    "warning",
    "error",
    "run.completed",
    "run.failed",
    "system.comment",
}

VALID_PHASES = {"prepare", "research", "execute", "format", "verify", "finalize"}

# Allow older/colloquial phase words and normalize them to canonical phases.
PHASE_ALIASES = {
    "start": "prepare",
    "init": "prepare",
    "setup": "prepare",
    "think": "research",
    "research": "research",
    "work": "execute",
    "exec": "execute",
    "run": "execute",
    "report": "format",
    "format": "format",
    "notify": "verify",
    "check": "verify",
    "verify": "verify",
    "done": "finalize",
    "finish": "finalize",
    "stop": "finalize",
    "end": "finalize",
}


def normalize_phase(phase: Any) -> Optional[str]:
    if phase is None:
        return None
    try:
        s = str(phase).strip().lower()
    except Exception:
        return None
    if not s:
        return None
    if s in VALID_PHASES:
        return s
    return PHASE_ALIASES.get(s)


def _truncate_str(s: Any, max_chars: int) -> str:
    try:
        t = str(s if s is not None else "")
    except Exception:
        t = ""
    if len(t) <= max_chars:
        return t
    return t[: max(0, max_chars - 1)] + "…"


def _summarize_any(v: Any, *, max_chars: int = 1200) -> Optional[str]:
    if v is None:
        return None
    if isinstance(v, str):
        s = v
    else:
        try:
            s = json.dumps(v, ensure_ascii=False, separators=(",", ":"))
        except Exception:
            s = str(v)
    s = s.strip()
    if len(s) > max_chars:
        s = s[: max(0, max_chars - 1)] + "…(truncated)"
    return s


def normalize_event_payload(e: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Normalize a single event dict to match backend validation.

    - phase: map aliases -> canonical phases, or drop if unknown
    - tool: convert input/output -> input_summary/output_summary (backend ignores extra keys)
    - type: coerce unknown types to system.comment (and keep original type in message)
    - size: truncate message/detail to backend limits
    """
    if not isinstance(e, dict):
        return None
    out: Dict[str, Any] = dict(e)

    etype = out.get("type")
    if etype is None:
        return None
    etype_s = str(etype)

    # Handle known legacy type(s).
    if etype_s == "tool.failed":
        out["type"] = "tool.completed"
        # Tag + severity, so UI can highlight even though type is tool.completed.
        tags = out.get("tags")
        if not isinstance(tags, list):
            tags = []
        if "failed" not in tags:
            tags.append("failed")
        out["tags"] = tags
        out.setdefault("severity", "error")
        if out.get("message"):
            out["message"] = f"FAILED: {_truncate_str(out.get('message'), 1900)}"

    # Unknown event types: downgrade to a comment rather than failing the whole stream.
    if out.get("type") not in VALID_EVENT_TYPES:
        orig = etype_s
        msg = out.get("message") or ""
        out["type"] = "system.comment"
        out["message"] = _truncate_str(f"[bridge] {orig}: {msg}", 2000)

    # Phase normalization (drop invalid values).
    ph = normalize_phase(out.get("phase"))
    if ph:
        out["phase"] = ph
    else:
        out.pop("phase", None)

    # Message/detail limits (backend: message<=2000, detail<=8000).
    out["message"] = _truncate_str(out.get("message") or out.get("type") or "event", 2000)
    if out.get("detail") is not None:
        out["detail"] = _truncate_str(out.get("detail"), 8000)

    # Tool normalization: backend expects ToolInfo fields only.
    tool = out.get("tool")
    if isinstance(tool, dict):
        name = tool.get("name")
        if name:
            t: Dict[str, Any] = dict(tool)
            t["name"] = str(name)

            # Convert raw input/output to summaries.
            if "input_summary" not in t and "input" in t:
                t["input_summary"] = _summarize_any(redact(t.get("input")))
            if "output_summary" not in t and "output" in t:
                t["output_summary"] = _summarize_any(redact(t.get("output")))

            # Ensure summaries are strings.
            if "input_summary" in t and t.get("input_summary") is not None and not isinstance(t.get("input_summary"), str):
                t["input_summary"] = _summarize_any(redact(t.get("input_summary")))
            if "output_summary" in t and t.get("output_summary") is not None and not isinstance(t.get("output_summary"), str):
                t["output_summary"] = _summarize_any(redact(t.get("output_summary")))

            # Remove unused raw keys to keep payload small.
            t.pop("input", None)
            t.pop("output", None)

            # Latency: best-effort int
            if t.get("latency_ms") is not None:
                try:
                    t["latency_ms"] = int(float(t["latency_ms"]))
                except Exception:
                    t.pop("latency_ms", None)

            out["tool"] = t
        else:
            out.pop("tool", None)
    elif tool is None:
        pass
    else:
        out.pop("tool", None)

    # Meta should be a dict (backend stores JSON).
    meta = out.get("meta")
    if meta is not None and not isinstance(meta, dict):
        out["meta"] = {"raw": _summarize_any(meta, max_chars=800)}

    # Tags: list[str]
    tags = out.get("tags")
    if tags is not None:
        if isinstance(tags, list):
            clean: List[str] = []
            for t in tags:
                if t is None:
                    continue
                s = str(t).strip()
                if s:
                    clean.append(s[:64])
            out["tags"] = clean[:50]
        else:
            out.pop("tags", None)

    # Progress: clamp to 0..1
    if out.get("progress") is not None:
        try:
            p = float(out["progress"])
            out["progress"] = max(0.0, min(1.0, p))
        except Exception:
            out.pop("progress", None)

    return out

# ---------------------------
# Config helpers
# ---------------------------

def _home_dir() -> str:
    return os.path.expanduser("~")


def _config_dir() -> str:
    return os.path.join(_home_dir(), ".agentjoy")


def _config_path() -> str:
    return os.path.join(_config_dir(), "config.json")


def load_config() -> Dict[str, Any]:
    path = _config_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if not isinstance(raw, dict):
            return _normalize_config({})
        return _normalize_config(raw)
    except FileNotFoundError:
        return _normalize_config({})
    except Exception:
        # If config is corrupted, ignore (don't crash automations)
        return _normalize_config({})


def save_config(cfg: Dict[str, Any]) -> None:
    os.makedirs(_config_dir(), exist_ok=True)
    path = _config_path()
    cfg = _normalize_config(cfg)
    # Ensure current profile exists when saving.
    cur = _get_profile_name(cfg)
    _get_profile(cfg, cur, create=True)
    _sync_legacy_keys(cfg)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# ---------------------------
# Adapter overrides (compat layer)
# ---------------------------

def _adapters_path() -> str:
    return os.path.join(_config_dir(), "bridge_adapters.json")


def load_adapters() -> Dict[str, Any]:
    """Load adapter overrides.

    This file is optional. It exists to make upstream tool changes survivable
    without requiring an immediate package release.
    """
    path = _adapters_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return raw if isinstance(raw, dict) else {}
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def write_adapters_template(force: bool = False) -> str:
    """Create a template adapters file and return its path."""
    os.makedirs(_config_dir(), exist_ok=True)
    path = _adapters_path()
    if os.path.exists(path) and not force:
        return path
    template = {
        "codex_jsonl": {
            # Codex JSONL is mostly stable, but upstream changes do happen.
            # If fields rename/move, you can add paths here without waiting for a release.
            "event_type": ["type", "event", "kind"],
            "timestamp": ["timestamp", "ts", "time"],
            "item": ["item", "data", "payload.item"],
            "item_type": ["item.type", "itemType", "item_kind", "data.type"],
            "item_status": ["item.status", "status", "state"],
            "item_id": ["item.id", "id", "itemId"],
            "text": ["item.text", "item.content", "item.message", "text", "content"],
            "command": [
                "item.command",
                "item.cmd",
                "item.input.command",
                "item.input.cmd",
                "command",
                "cmd",
            ],
            "output": ["item.output", "item.result", "item.stdout", "output", "result", "stdout"],
            "exit_code": ["item.exit_code", "item.exitCode", "item.code", "exit_code", "code"],
        },
        "claude_hook": {
            # Add/override dot-paths used to read Claude hook JSON.
            # Example: if a future version renames `sessionId` -> `session_id`,
            # you can add it here without updating the package.
            "hook_event_name": ["hook_event_name", "hookEventName", "event", "type"],
            "session_id": ["session_id", "sessionId", "session", "meta.session_id", "meta.sessionId"],
            "tool_call_id": [
                "tool_use_id",
                "toolUseId",
                "tool_call_id",
                "toolCallId",
                "call_id",
                "callId",
                "id",
                "event_id",
                "eventId",
                "meta.tool_call_id",
                "meta.toolCallId",
            ],
            "tool_name": ["tool_name", "toolName", "tool.name", "meta.tool_name", "meta.toolName"],
            "tool_input": ["tool_input", "toolInput", "tool.input", "input", "meta.tool_input"],
            "tool_result": ["tool_response", "tool_result", "toolResult", "tool.result", "result", "meta.tool_result"],
            "message": ["message", "content", "text", "meta.message"],
        }
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    return path


def _get_by_path(obj: Any, path: str) -> Any:
    """Best-effort nested lookup for dict/list structures.

    Supports dot paths (e.g. "tool.name") and list indexes (e.g. "choices[0]").
    """
    if not path:
        return None
    cur: Any = obj
    # Fast exit for non-container roots.
    if cur is None:
        return None
    for part in str(path).split("."):
        if cur is None:
            return None
        token = part
        # Allow a token to be purely an index: "[0]"
        if token.startswith("[") and token.endswith("]"):
            name = ""
            idxs = [token[1:-1]]
        else:
            # token may be like "name[0][1]"
            name = token.split("[")[0]
            idxs = []
            if "[" in token and token.endswith("]"):
                # collect all indices
                try:
                    idxs = [x.split("]")[0] for x in token.split("[")[1:]]
                except Exception:
                    idxs = []

        if name:
            if isinstance(cur, dict) and name in cur:
                cur = cur.get(name)
            else:
                return None

        for raw_idx in idxs:
            try:
                i = int(raw_idx)
            except Exception:
                return None
            if isinstance(cur, list) and 0 <= i < len(cur):
                cur = cur[i]
            else:
                return None
    return cur


def _first_by_paths(obj: Any, paths: List[str]) -> Any:
    for p in paths:
        try:
            v = _get_by_path(obj, p)
        except Exception:
            v = None
        if v is None:
            continue
        # Treat empty strings as missing.
        if isinstance(v, str) and not v.strip():
            continue
        return v
    return None


def _adapter_paths(overrides: Dict[str, Any], adapter: str, field: str, defaults: List[str]) -> List[str]:
    ov = None
    try:
        ad = overrides.get(adapter)
        if isinstance(ad, dict):
            ov = ad.get(field)
    except Exception:
        ov = None
    if isinstance(ov, list):
        clean: List[str] = []
        for x in ov:
            if x is None:
                continue
            s = str(x).strip()
            if s:
                clean.append(s)
        # Prepend overrides so users can shadow defaults.
        return clean + defaults
    return defaults


# ---------------------------
# Multi-profile config helpers
# ---------------------------

LEGACY_CONFIG_KEYS: Tuple[str, ...] = (
    "api_base",
    "api_key",
    "user_token",
    "default_pack",
    "default_mode",
)


def _normalize_config(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize config to a shape that supports multiple profiles.

    Backward compatible:
      - legacy flat keys are kept (and mirrored from the current profile on save)
      - if profiles are missing but legacy keys exist, we create a default profile in-memory
    """
    if not isinstance(cfg, dict):
        cfg = {}

    profiles = cfg.get("profiles")
    if not isinstance(profiles, dict):
        # Migrate legacy flat keys to profiles.
        legacy: Dict[str, Any] = {}
        for k in LEGACY_CONFIG_KEYS:
            v = cfg.get(k)
            if v is not None and v != "":
                legacy[k] = v
        profiles = {}
        if legacy:
            profiles["default"] = legacy
        cfg["profiles"] = profiles

    cur = cfg.get("current_profile")
    if not isinstance(cur, str) or not cur.strip():
        cur = "default"
        cfg["current_profile"] = cur
    else:
        cur = cur.strip()
        cfg["current_profile"] = cur

    # If current profile is missing but we have profiles, pick the first.
    if profiles and cur not in profiles:
        cfg["current_profile"] = next(iter(profiles.keys()))

    return cfg


def _get_profile_name(cfg: Dict[str, Any], override: Optional[str] = None) -> str:
    name = (override or os.environ.get("AGENTJOY_PROFILE") or cfg.get("current_profile") or "default")
    name = str(name).strip() if name is not None else "default"
    return name or "default"


def _get_profiles(cfg: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    ps = cfg.get("profiles")
    if isinstance(ps, dict):
        # type: ignore[return-value]
        return ps  # pyright: ignore
    return {}


def _get_profile(cfg: Dict[str, Any], name: str, *, create: bool = False) -> Dict[str, Any]:
    cfg = _normalize_config(cfg)
    profiles = cfg.setdefault("profiles", {})
    p = profiles.get(name)
    if isinstance(p, dict):
        return p
    if create:
        profiles[name] = {}
        return profiles[name]
    return {}


def _sync_legacy_keys(cfg: Dict[str, Any]) -> None:
    """Mirror the active profile into legacy top-level keys for backwards compatibility."""
    cur = _get_profile_name(cfg)
    p = _get_profile(cfg, cur, create=False)
    for k in LEGACY_CONFIG_KEYS:
        if k in p and p.get(k) is not None and p.get(k) != "":
            cfg[k] = p.get(k)
        else:
            cfg.pop(k, None)


def _mask_secret(s: Optional[str]) -> str:
    if not s:
        return "(unset)"
    s = str(s)
    if len(s) <= 8:
        if len(s) <= 2:
            return "*" * len(s)
        return s[0] + ("*" * (len(s) - 2)) + s[-1]
    return s[:4] + "…" + s[-4:]


# ---------------------------
# HTTP client (stdlib-only)
# ---------------------------

@dataclass
class ApiClient:
    api_base: str
    api_key: Optional[str] = None
    user_token: Optional[str] = None
    timeout_s: float = 10.0

    def _headers(self, use_user: bool = False) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        # Backend expects X-AgentJoy-User-Token (not Authorization: Bearer) for console/admin endpoints.
        if use_user and self.user_token:
            h["X-AgentJoy-User-Token"] = self.user_token
        elif self.api_key:
            h["X-AgentJoy-Key"] = self.api_key
        return h

    def _request(self, method: str, path: str, body: Optional[Dict[str, Any]] = None, *, use_user: bool = False) -> Any:
        url = urljoin(self.api_base.rstrip("/") + "/", path.lstrip("/"))
        data = None
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urlrequest.Request(url, data=data, method=method, headers=self._headers(use_user=use_user))
        try:
            with urlrequest.urlopen(req, timeout=self.timeout_s) as resp:
                raw = resp.read().decode("utf-8")
                if not raw:
                    return None
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return raw
        except HTTPError as e:
            raw = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"HTTP {e.code} {method} {url}: {raw}") from None
        except URLError as e:
            raise RuntimeError(f"Network error {method} {url}: {e}") from None

    def get(self, path: str, *, use_user: bool = False) -> Any:
        return self._request("GET", path, use_user=use_user)

    def post(self, path: str, body: Dict[str, Any], *, use_user: bool = False) -> Any:
        return self._request("POST", path, body=body, use_user=use_user)


# ---------------------------
# AgentJoy API wrappers
# ---------------------------

def api_health_info(client: ApiClient) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """Return backend health with diagnostics.

    Returns:
        (ok, data, error_message)
    """
    try:
        r = client.get("/health")
        if isinstance(r, dict) and r.get("status") == "ok":
            return True, r, None
        return False, (r if isinstance(r, dict) else None), f"Unexpected /health response: {r!r}"
    except Exception as e:
        return False, None, str(e)


def api_connect_ping_best_effort(
    client: ApiClient,
    kind: str,
    *,
    profile: Optional[str] = None,
    note: Optional[str] = None,
) -> None:
    """Non-failing 'proof of life' ping used by the Connect page.

    The backend endpoint is intentionally optional so the bridge stays compatible with
    older AgentJoy versions.
    """
    body = {
        "kind": kind,
        "bridge_version": BRIDGE_VERSION,
        "profile": profile,
        "note": note,
    }
    try:
        client.post("/v1/connect/ping", body)
    except Exception:
        # best-effort; ignore (backend might be older / endpoint disabled)
        pass


def api_capabilities_info(client: ApiClient) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """Return backend capabilities with diagnostics.

    This is optional: older backends may not implement this endpoint.
    """
    try:
        r = client.get("/v1/capabilities")
        if isinstance(r, dict) and r.get("status") == "ok":
            return True, r, None
        return False, (r if isinstance(r, dict) else None), f"Unexpected /v1/capabilities response: {r!r}"
    except Exception as e:
        return False, None, str(e)


def api_health(client: ApiClient) -> bool:
    ok, _, _ = api_health_info(client)
    return ok


def api_create_workspace(client: ApiClient, name: str) -> Dict[str, Any]:
    """Create a workspace and return the API response.

    This endpoint is intentionally unauthenticated (bootstrap).
    Response contains:
      - workspace
      - api_key (write key)
      - owner_user_token (console/admin token)
    """
    body = {"name": name}
    return client.post("/v1/workspaces", body)


def api_create_run(
    client: ApiClient,
    title: str,
    *,
    mode: str = "default",
    pack: str = "default",
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    body = {
        "title": title,
        "mode": mode,
        "pack": pack,
        "metadata": metadata or {},
    }
    return client.post("/v1/runs", body)


def api_post_events(client: ApiClient, run_id: str, events: List[Dict[str, Any]]) -> None:
    # batch endpoint exists, but we keep a simple loop for compatibility
    # (and because failures are easier to attribute per-event).
    for e in events:
        payload = normalize_event_payload(e)
        if payload is None:
            continue
        client.post(f"/v1/runs/{run_id}/events", payload)


def api_share_run(client: ApiClient, run_id: str, expires_in_hours: int = 72) -> Optional[str]:
    """Returns share URL if possible, else None."""
    body = {"expires_in_hours": expires_in_hours}
    # Prefer API-key based endpoint (new in this bundle).
    try:
        r = client.post(f"/v1/runs/{run_id}/share_by_key", body)
        return r.get("url") if isinstance(r, dict) else None
    except Exception:
        pass
    # Fallback to user-token endpoint if provided.
    if client.user_token:
        try:
            r = client.post(f"/v1/runs/{run_id}/share", body, use_user=True)
            return r.get("url") if isinstance(r, dict) else None
        except Exception:
            return None
    return None


# ---------------------------
# Redaction helpers
# ---------------------------

SENSITIVE_KEYS = {"api_key", "apikey", "token", "secret", "password", "authorization", "bearer"}

def redact(obj: Any, *, max_chars: int = 4000) -> Any:
    """Best-effort redaction + truncation for tool inputs/outputs.

    We don't try to be perfect. We just avoid obvious footguns and keep payload small.
    """
    try:
        if obj is None:
            return None
        if isinstance(obj, (int, float, bool)):
            return obj
        if isinstance(obj, str):
            s = obj
            if len(s) > max_chars:
                s = s[:max_chars] + "…(truncated)"
            return s
        if isinstance(obj, list):
            return [redact(x, max_chars=max_chars) for x in obj[:200]]
        if isinstance(obj, dict):
            out = {}
            for k, v in list(obj.items())[:200]:
                lk = str(k).lower()
                if lk in SENSITIVE_KEYS:
                    out[k] = "***redacted***"
                else:
                    out[k] = redact(v, max_chars=max_chars)
            return out
        # Fallback: stringification
        return redact(str(obj), max_chars=max_chars)
    except Exception:
        return "***redacted***"


# ---------------------------
# Codex bridge
# ---------------------------

class CodexBridge:
    def __init__(self, client: ApiClient, *, title: str, pack: str = "default", mode: str = "default", share: bool = True):
        self.client = client
        self.title = title
        self.pack = pack
        self.mode = mode
        self.share = share
        self.run: Optional[Dict[str, Any]] = None
        self.run_id: Optional[str] = None
        self.share_url: Optional[str] = None
        self._final_messages: List[str] = []
        # Optional compat layer. If Codex changes its JSONL fields, users can patch
        # extraction paths locally via `agentjoy adapters --init`.
        self._adapters = load_adapters()
        self._q: "queue.Queue[Dict[str, Any]]" = queue.Queue()
        self._stop = threading.Event()
        self._sender = threading.Thread(target=self._sender_loop, daemon=True)

    def start(self) -> None:
        self.run = api_create_run(self.client, self.title, mode=self.mode, pack=self.pack, metadata={"source": "codex"})
        self.run_id = self.run["run"]["id"]
        if self.share:
            self.share_url = api_share_run(self.client, self.run_id)  # may be None
        self._sender.start()
        # initial note
        self.enqueue_event({
            "type": "system.comment",
            "phase": "prepare",
            "message": "Codex の実行を監視しています。",
            "detail": None,
            "tool": None,
        })

    def enqueue_event(self, e: Dict[str, Any]) -> None:
        if not self.run_id:
            return
        self._q.put(e)

    def _sender_loop(self) -> None:
        buf: List[Dict[str, Any]] = []
        last_flush = time.time()
        while not self._stop.is_set() or not self._q.empty():
            try:
                e = self._q.get(timeout=0.2)
                buf.append(e)
            except queue.Empty:
                pass
            now = time.time()
            if buf and (len(buf) >= 5 or (now - last_flush) >= 0.75):
                try:
                    api_post_events(self.client, self.run_id, buf)
                except Exception:
                    # Avoid killing the bridge. Print once and keep going.
                    print("[agentjoy] failed to post events (continuing)", file=sys.stderr)
                buf = []
                last_flush = now
        # final flush
        if buf and self.run_id:
            try:
                api_post_events(self.client, self.run_id, buf)
            except Exception:
                pass

    def stop(self, ok: bool = True, *, message: Optional[str] = None) -> None:
        if ok:
            self.enqueue_event({
                "type": "run.completed",
                "phase": "finalize",
                "message": message or "Codex の処理が完了しました。",
                "detail": None,
                "tool": None,
                "artifacts": None,
            })
        else:
            self.enqueue_event({
                "type": "run.failed",
                "phase": "finalize",
                "message": message or "Codex の処理が失敗しました。",
                "detail": None,
                "tool": None,
            })
        # let sender flush
        self._stop.set()
        self._sender.join(timeout=3.0)

    def on_jsonl_event(self, line_obj: Dict[str, Any]) -> None:
        overrides = self._adapters
        etype = _first_by_paths(
            line_obj,
            _adapter_paths(overrides, "codex_jsonl", "event_type", ["type"]),
        )
        etype = str(etype or "").strip()

        item = _first_by_paths(
            line_obj,
            _adapter_paths(overrides, "codex_jsonl", "item", ["item"]),
        )
        if not isinstance(item, dict):
            item = {}

        # Timestamp is optional (we currently don't send it to backend), but we keep
        # the extraction here so future UI/telemetry can use it.
        ts = _first_by_paths(
            line_obj,
            _adapter_paths(overrides, "codex_jsonl", "timestamp", ["timestamp", "ts"]),
        )

        # Thread / turn lifecycle
        if etype == "thread.started":
            self.enqueue_event({"type": "system.comment", "phase": "prepare", "message": "Codex: thread started", "detail": None})
            return
        if etype in {"thread.completed", "thread.ended"}:
            self.enqueue_event({"type": "system.comment", "phase": "finalize", "message": "Codex: thread completed", "detail": None})
            return

        # Item lifecycle
        if etype in {"item.started", "item.delta", "item.completed"} and isinstance(item, dict):
            itype = _first_by_paths(
                line_obj,
                _adapter_paths(overrides, "codex_jsonl", "item_type", ["item.type"]),
            )
            status = _first_by_paths(
                line_obj,
                _adapter_paths(overrides, "codex_jsonl", "item_status", ["item.status"]),
            )
            item_id = _first_by_paths(
                line_obj,
                _adapter_paths(overrides, "codex_jsonl", "item_id", ["item.id"]),
            )
            itype = str(itype or "").strip()
            status = str(status or "").strip()

            # Most useful: agent_message + command execution-ish.
            if itype in {"agent_message", "assistant_message"}:
                txt = _first_by_paths(
                    line_obj,
                    _adapter_paths(
                        overrides,
                        "codex_jsonl",
                        "text",
                        ["item.text", "item.content", "item.message"],
                    ),
                )
                txt = str(txt or "")
                if txt:
                    # Store for printing final answer.
                    if etype == "item.completed":
                        self._final_messages.append(txt)
                    # Stream partial as comments (lightly throttled by sender).
                    self.enqueue_event({
                        "type": "system.comment",
                        "phase": "think" if status == "in_progress" else "report",
                        "message": txt.splitlines()[0][:120] if txt else "assistant",
                        "detail": txt if len(txt) <= 2000 else (txt[:2000] + "…"),
                    })
                return

            # Heuristic: command execution
            cmd = _first_by_paths(
                line_obj,
                _adapter_paths(
                    overrides,
                    "codex_jsonl",
                    "command",
                    [
                        "item.command",
                        "item.cmd",
                        "item.input.command",
                        "item.input.cmd",
                    ],
                ),
            )
            if cmd:
                cmd_s = str(cmd)
                if etype == "item.started":
                    ev = {
                        "type": "tool.called",
                        "phase": "execute",
                        "message": f"実行: {cmd_s}",
                        "detail": None,
                        "tool": {"name": "bash", "input_summary": cmd_s},
                    }
                    if item_id is not None:
                        ev["meta"] = {"tool_call_id": str(item_id)}
                    self.enqueue_event(ev)
                elif etype == "item.completed":
                    out = _first_by_paths(
                        line_obj,
                        _adapter_paths(
                            overrides,
                            "codex_jsonl",
                            "output",
                            ["item.output", "item.result", "item.stdout"],
                        ),
                    )
                    code = _first_by_paths(
                        line_obj,
                        _adapter_paths(
                            overrides,
                            "codex_jsonl",
                            "exit_code",
                            ["item.exit_code", "item.exitCode", "item.code"],
                        ),
                    )
                    detail = ""
                    if code is not None:
                        detail += f"exit_code={code}\n"
                    if out:
                        detail += str(out)

                    ev = {
                        "type": "tool.completed",
                        "phase": "execute",
                        "message": f"完了: {cmd_s}",
                        "detail": detail[:4000] + ("…(truncated)" if len(detail) > 4000 else ""),
                        "tool": {
                            "name": "bash",
                            "input_summary": cmd_s,
                            "output_summary": _truncate_str(redact(out), 1200),
                        },
                    }
                    if item_id is not None:
                        ev["meta"] = {"tool_call_id": str(item_id)}
                    self.enqueue_event(ev)
                return

            # Generic tool-ish item: show type
            if itype and etype == "item.started":
                ev = {
                    "type": "tool.called",
                    "phase": "work",
                    "message": f"{itype} を開始",
                    "detail": None,
                    "tool": {"name": itype, "input_summary": _summarize_any(redact(item.get("input") or {}))},
                }
                if item_id is not None:
                    ev["meta"] = {"tool_call_id": str(item_id)}
                self.enqueue_event(ev)
                return
            if itype and etype == "item.completed":
                ev = {
                    "type": "tool.completed",
                    "phase": "work",
                    "message": f"{itype} が完了",
                    "detail": None,
                    "tool": {"name": itype, "output_summary": _summarize_any(redact(item))},
                }
                if item_id is not None:
                    ev["meta"] = {"tool_call_id": str(item_id)}
                self.enqueue_event(ev)
                return

        # Anything else: keep quiet.

    def final_answer(self) -> str:
        # Prefer last completed message.
        if self._final_messages:
            return self._final_messages[-1].strip()
        return ""


def run_codex_subprocess(prompt: str, extra_args: List[str]) -> subprocess.Popen:
    # Use Codex CLI in non-interactive JSON mode.
    # Docs: `codex exec --json "..."` streams JSONL events to stdout.
    cmd = ["codex", "exec", "--json", prompt] + extra_args
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)


def codex_run_flow(args: argparse.Namespace, client: ApiClient) -> int:
    title = args.title or f"Codex: {args.prompt[:60]}"
    pack, mode = resolve_pack_mode(args)

    # Proof-of-life (Codex integration)
    api_connect_ping_best_effort(client, "codex", profile=getattr(args, "profile", None), note="codex-run")
    bridge = CodexBridge(client, title=title, pack=pack, mode=mode, share=args.share)
    bridge.start()

    # Print URLs to stderr so stdout can be reserved for final answer.
    print(f"[agentjoy] run_id={bridge.run_id}", file=sys.stderr)
    if bridge.share_url:
        print(f"[agentjoy] share_url={bridge.share_url}", file=sys.stderr)
    else:
        print("[agentjoy] share_url=（未作成。必要ならConsoleでShare作成してください）", file=sys.stderr)
    if bridge.run and bridge.run.get("run") and bridge.run["run"].get("console_url"):
        print(f"[agentjoy] console_url={bridge.run['run']['console_url']}", file=sys.stderr)

    try:
        proc = run_codex_subprocess(args.prompt, args.codex_args or [])
    except FileNotFoundError:
        # Beginner-friendly: Codex CLI is frequently missing from PATH.
        print("[agentjoy] ERROR: `codex` command not found (Codex CLI).", file=sys.stderr)
        print("[agentjoy]        Ensure Codex CLI is installed and available on PATH.", file=sys.stderr)
        print("[agentjoy]        Quick check: `codex --help` (or `codex --version`).", file=sys.stderr)
        return 1
    assert proc.stdout is not None
    assert proc.stderr is not None

    # Forward stderr in background (so codex progress/errors aren't lost)
    def _stderr_forward():
        for line in proc.stderr:
            sys.stderr.write(line)
    t = threading.Thread(target=_stderr_forward, daemon=True)
    t.start()

    ok = True
    try:
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            bridge.on_jsonl_event(obj)
    except KeyboardInterrupt:
        ok = False
        bridge.stop(ok=False, message="中断されました。")
        proc.kill()
        return 130
    except Exception as e:
        ok = False
        bridge.stop(ok=False, message=f"ブリッジ側エラー: {e}")
        proc.kill()
        return 1

    rc = proc.wait()
    ok = ok and (rc == 0)
    bridge.stop(ok=ok, message="Codex が終了しました。")
    ans = bridge.final_answer()
    if ans:
        # Print final answer to stdout for convenience.
        print(ans)
    return 0 if ok else rc or 1


def codex_stream_flow(args: argparse.Namespace, client: ApiClient) -> int:
    title = args.title or "Codex (stream)"
    pack, mode = resolve_pack_mode(args)

    # Proof-of-life (Codex integration)
    api_connect_ping_best_effort(client, "codex", profile=getattr(args, "profile", None), note="codex-stream")
    bridge = CodexBridge(client, title=title, pack=pack, mode=mode, share=args.share)
    bridge.start()
    print(f"[agentjoy] run_id={bridge.run_id}", file=sys.stderr)
    if bridge.share_url:
        print(f"[agentjoy] share_url={bridge.share_url}", file=sys.stderr)

    ok = True
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            bridge.on_jsonl_event(obj)
    except KeyboardInterrupt:
        ok = False
    except Exception as e:
        ok = False
        print(f"[agentjoy] error: {e}", file=sys.stderr)
    bridge.stop(ok=ok, message="Codex stream ended.")
    ans = bridge.final_answer()
    if ans:
        print(ans)
    return 0 if ok else 1


# ---------------------------
# Claude hook helper (standalone)
# ---------------------------

SESSION_MAP_PATH = os.path.join(_config_dir(), "claude_sessions.json")

def _load_session_map() -> Dict[str, str]:
    try:
        with open(SESSION_MAP_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

def _save_session_map(m: Dict[str, str]) -> None:
    os.makedirs(_config_dir(), exist_ok=True)
    tmp = SESSION_MAP_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    os.replace(tmp, SESSION_MAP_PATH)

TOOLCALL_MAP_PATH = os.path.join(_config_dir(), "claude_toolcalls.json")

def _load_toolcall_map() -> Dict[str, Dict[str, Any]]:
    """Persisted map so PreToolUse / PostToolUse can share a tool_call_id.

    Claude hooks are executed as separate processes, so we can't rely on in-memory state.
    """
    try:
        with open(TOOLCALL_MAP_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, dict):
            return raw  # type: ignore[return-value]
        return {}
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

def _save_toolcall_map(m: Dict[str, Dict[str, Any]]) -> None:
    os.makedirs(_config_dir(), exist_ok=True)
    tmp = TOOLCALL_MAP_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    os.replace(tmp, TOOLCALL_MAP_PATH)

def claude_hook_flow(args: argparse.Namespace, client: ApiClient) -> int:
    try:
        inp = json.load(sys.stdin)
    except Exception:
        return 0  # Claude hooks must be resilient

    # Resolve defaults once (profile-aware). We mutate args so downstream code remains simple.
    pack, mode = resolve_pack_mode(args)
    args.pack = pack
    args.mode = mode

    # Proof-of-life (Claude hooks integration)
    api_connect_ping_best_effort(client, "claude", profile=getattr(args, "profile", None), note="claude-hook")

    overrides = load_adapters()
    hook = _first_by_paths(
        inp,
        _adapter_paths(overrides, "claude_hook", "hook_event_name", ["hook_event_name", "hookEventName", "event", "type"]),
    ) or ""
    session_id = _first_by_paths(
        inp,
        _adapter_paths(overrides, "claude_hook", "session_id", ["session_id", "sessionId", "session", "meta.session_id", "meta.sessionId"]),
    ) or "unknown"
    tool_name = _first_by_paths(
        inp,
        _adapter_paths(overrides, "claude_hook", "tool_name", ["tool_name", "toolName", "tool.name", "meta.tool_name", "meta.toolName"]),
    )
    tool_input = _first_by_paths(
        inp,
        _adapter_paths(overrides, "claude_hook", "tool_input", ["tool_input", "toolInput", "tool.input", "input", "meta.tool_input"]),
    )
    tool_response = _first_by_paths(
        inp,
        _adapter_paths(
            overrides,
            "claude_hook",
            "tool_result",
            ["tool_response", "tool_result", "toolResult", "tool.result", "result", "meta.tool_result"],
        ),
    )
    message = _first_by_paths(inp, _adapter_paths(overrides, "claude_hook", "message", ["message", "content", "text", "meta.message"]))
    reason = _first_by_paths(inp, ["reason", "meta.reason"])  # optional

    # Ensure stable key types (upstream tools sometimes change shapes).
    hook = str(hook)
    session_id = str(session_id)

    sessions = _load_session_map()
    run_id = sessions.get(session_id)
    toolcalls = _load_toolcall_map()

    def _ensure_run() -> str:
        nonlocal run_id
        if run_id:
            return run_id
        title = args.title or f"Claude Code: {session_id}"
        run = api_create_run(client, title, mode=args.mode, pack=args.pack, metadata={"source": "claude_code", "session_id": session_id})
        run_id = run["run"]["id"]
        sessions[session_id] = run_id
        _save_session_map(sessions)
        # Share link if possible
        if args.share:
            share_url = api_share_run(client, run_id)
            if share_url:
                # Show to user as systemMessage (Claude Code hook JSON output).
                out = {"systemMessage": f"AgentJoy tracking started: {share_url}", "suppressOutput": True}
                print(json.dumps(out, ensure_ascii=False))
        return run_id

    # SessionStart: create a run and announce
    if hook == "SessionStart":
        _ensure_run()
        api_post_events(client, run_id, [{
            "type": "system.comment",
            "phase": "start",
            "message": "Claude Code セッション開始",
            "detail": inp.get("cwd") or None,
        }])
        return 0

    # Other hooks: ensure run exists but do not spam systemMessage.
    _ensure_run()

    if hook == "PreToolUse" and tool_name:
        call_id = (
            _first_by_paths(
                inp,
                _adapter_paths(
                    overrides,
                    "claude_hook",
                    "tool_call_id",
                    ["tool_use_id", "toolUseId", "tool_call_id", "toolCallId", "call_id", "callId", "id", "event_id", "eventId"],
                ),
            )
            or f"claude_{session_id}_{int(time.time() * 1000)}"
        )
        # Persist a small stack so PostToolUse can reuse the same tool_call_id.
        try:
            lst = toolcalls.get(session_id)
            if not isinstance(lst, list):
                lst = []
            lst.append({
                "tool_name": str(tool_name),
                "tool_call_id": call_id,
                "ts": datetime.now(timezone.utc).isoformat(),
            })
            toolcalls[session_id] = lst
            _save_toolcall_map(toolcalls)
        except Exception:
            pass

        ev = {
            "type": "tool.called",
            "phase": "execute",
            "message": f"Tool: {tool_name}",
            "detail": None,
            "tool": {"name": tool_name, "input_summary": _summarize_any(redact(tool_input))},
        }
        if call_id:
            ev["meta"] = {"tool_call_id": call_id}
        api_post_events(client, run_id, [ev])
        return 0

    if hook == "PostToolUse" and tool_name:
        # Determine success if tool_response has a "success" bool
        success = True
        if isinstance(tool_response, dict) and "success" in tool_response:
            success = bool(tool_response.get("success"))

        call_id = _first_by_paths(
            inp,
            _adapter_paths(
                overrides,
                "claude_hook",
                "tool_call_id",
                ["tool_use_id", "toolUseId", "tool_call_id", "toolCallId", "call_id", "callId", "id", "event_id", "eventId"],
            ),
        )

        # If Claude doesn't provide an id, try to reuse the last PreToolUse id for this session/tool.
        try:
            lst = toolcalls.get(session_id)
            if isinstance(lst, list) and lst:
                if call_id:
                    # Remove matching id to keep the stack clean.
                    for i in range(len(lst) - 1, -1, -1):
                        ent = lst[i]
                        if isinstance(ent, dict) and str(ent.get("tool_call_id") or "") == call_id:
                            lst.pop(i)
                            break
                else:
                    for i in range(len(lst) - 1, -1, -1):
                        ent = lst[i]
                        if isinstance(ent, dict) and str(ent.get("tool_name") or "") == str(tool_name):
                            call_id = str(ent.get("tool_call_id") or "").strip() or None
                            lst.pop(i)
                            break

                if lst:
                    toolcalls[session_id] = lst
                else:
                    toolcalls.pop(session_id, None)
                _save_toolcall_map(toolcalls)
        except Exception:
            pass

        in_sum = _summarize_any(redact(tool_input))
        out_sum = _summarize_any(redact(tool_response))

        evs: List[Dict[str, Any]] = []

        tool_ev: Dict[str, Any] = {
            "type": "tool.completed",
            "phase": "execute",
            "message": f"Tool done: {tool_name}" if success else f"Tool failed: {tool_name}",
            "detail": None,
            "tool": {"name": tool_name, "input_summary": in_sum, "output_summary": out_sum},
        }
        if call_id:
            tool_ev["meta"] = {"tool_call_id": call_id}
        if not success:
            tool_ev["tags"] = ["failed"]
            tool_ev["severity"] = "error"
        evs.append(tool_ev)

        if not success:
            err_ev: Dict[str, Any] = {
                "type": "error",
                "phase": "execute",
                "message": f"Tool failed: {tool_name}",
                "detail": out_sum,
                "tool": {"name": tool_name},
            }
            if call_id:
                err_ev["meta"] = {"tool_call_id": call_id}
            evs.append(err_ev)

        api_post_events(client, run_id, evs)
        return 0

    if hook == "Notification" and message:
        api_post_events(client, run_id, [{
            "type": "warning" if inp.get("notification_type") else "system.comment",
            "phase": "notify",
            "message": str(message)[:200],
            "detail": str(message),
        }])
        return 0

    if hook in {"Stop", "SubagentStop"}:
        api_post_events(client, run_id, [{
            "type": "system.comment",
            "phase": "stop",
            "message": "停止要求",
            "detail": json.dumps({"stop_reason": inp.get("stop_reason") or inp.get("reason")}, ensure_ascii=False),
        }])
        return 0

    if hook == "SessionEnd":
        api_post_events(client, run_id, [{
            "type": "run.completed",
            "phase": "done",
            "message": f"Claude Code セッション終了 ({reason or 'unknown'})",
            "detail": None,
        }])
        # Cleanup mapping
        try:
            sessions.pop(session_id, None)
            _save_session_map(sessions)
            toolcalls.pop(session_id, None)
            _save_toolcall_map(toolcalls)
        except Exception:
            pass
        return 0

    return 0


# ---------------------------
# CLI
# ---------------------------

def build_client_from_args(args: argparse.Namespace) -> ApiClient:
    cfg = load_config()
    profile = _get_profile_name(cfg, getattr(args, "profile", None))
    p = _get_profile(cfg, profile, create=False)
    p_default = _get_profile(cfg, "default", create=False)

    api_base = (
        getattr(args, "api_base", None)
        or os.environ.get("AGENTJOY_API_BASE")
        or p.get("api_base")
        or p_default.get("api_base")
        or cfg.get("api_base")
        or DEFAULT_API_BASE
    )
    api_key = (
        getattr(args, "api_key", None)
        or os.environ.get("AGENTJOY_API_KEY")
        or p.get("api_key")
        or p_default.get("api_key")
        or cfg.get("api_key")
    )
    user_token = (
        getattr(args, "user_token", None)
        or os.environ.get("AGENTJOY_USER_TOKEN")
        or p.get("user_token")
        or p_default.get("user_token")
        or cfg.get("user_token")
    )
    return ApiClient(api_base=api_base, api_key=api_key, user_token=user_token, timeout_s=10.0)


def resolve_pack_mode(args: argparse.Namespace) -> Tuple[str, str]:
    """Resolve (pack, mode) with profile-aware defaults."""
    cfg = load_config()
    profile = _get_profile_name(cfg, getattr(args, "profile", None))
    p = _get_profile(cfg, profile, create=False)
    p_default = _get_profile(cfg, "default", create=False)
    pack = (
        getattr(args, "pack", None)
        or p.get("default_pack")
        or p_default.get("default_pack")
        or cfg.get("default_pack")
        or "default"
    )
    mode = (
        getattr(args, "mode", None)
        or p.get("default_mode")
        or p_default.get("default_mode")
        or cfg.get("default_mode")
        or "default"
    )

    return str(pack), str(mode)



# ---------------------------
# Beginner-friendly commands
# ---------------------------

def _python_cmd_hint() -> str:
    """Return a best-effort Python executable name.

    Why this exists:
    - Windows Store installs often provide `python` but not the `py` launcher.
    - python.org installs may have both.
    - We want copy-paste commands that work on the widest set of machines.
    """
    if _is_windows():
        for c in ("python", "py", "python3"):
            if shutil_which(c):
                return c
        return "python"
    for c in ("python3", "python"):
        if shutil_which(c):
            return c
    return "python3"

def _agentjoy_invocation_hint() -> str:
    """Return the safest way to invoke this CLI for the current environment."""
    # If the entrypoint is on PATH, prefer it.
    if shutil_which("agentjoy"):
        return "agentjoy"
    # Otherwise, suggest module invocation.
    return f"{_python_cmd_hint()} -m agentjoy_bridge"


def _parse_api_base(api_base: str) -> Tuple[str, int, str]:
    """Parse api_base into (host, port, scheme)."""
    s = api_base.strip()
    if "://" not in s:
        s = "http://" + s
    u = urlparse(s)
    host = u.hostname or "127.0.0.1"
    scheme = u.scheme or "http"
    port = u.port or (443 if scheme == "https" else 80)
    return host, int(port), scheme


def _is_port_listening(host: str, port: int, *, timeout_s: float = 0.25) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            return True
    except OSError:
        return False


def _pick_free_port(host: str, preferred_port: int, *, tries: int = 25) -> int:
    """Pick a free port by scanning forward from preferred_port."""
    port = max(1, int(preferred_port))
    for p in range(port, port + tries):
        if not _is_port_listening(host, p):
            return p
    return port


def _find_backend_dir(start_dir: str) -> Optional[str]:
    """Best-effort search for the repo backend directory from current cwd."""
    cur = os.path.abspath(start_dir)
    for _ in range(8):
        # If user is already in backend/
        if os.path.isfile(os.path.join(cur, "agentjoy", "main.py")):
            return cur

        cand = os.path.join(cur, "backend")
        if os.path.isfile(os.path.join(cand, "agentjoy", "main.py")):
            return cand

        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return None


def _backend_log_path() -> str:
    return os.path.join(_config_dir(), "backend.log")


def _start_backend_uvicorn(
    *,
    backend_dir: str,
    host: str,
    port: int,
    public_base_url: str,
    reload: bool = False,
    log_path: Optional[str] = None,
) -> subprocess.Popen:
    """Start AgentJoy backend via uvicorn in a detached process."""
    os.makedirs(_config_dir(), exist_ok=True)
    log_path = log_path or _backend_log_path()
    logf = open(log_path, "ab", buffering=0)

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "agentjoy.main:app",
        "--host",
        host,
        "--port",
        str(int(port)),
    ]
    if reload:
        cmd.append("--reload")

    env = os.environ.copy()
    env.setdefault("AGENTJOY_PUBLIC_BASE_URL", public_base_url)

    # Onboarding-friendly DB location: keep DB under backend dir by default.
    env.setdefault("AGENTJOY_DB_PATH", os.path.join(backend_dir, "agentjoy.db"))

    kwargs: Dict[str, Any] = {
        "cwd": backend_dir,
        "env": env,
        "stdin": subprocess.DEVNULL,
        "stdout": logf,
        "stderr": logf,
    }

    if _is_windows():
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        kwargs["close_fds"] = True
    else:
        kwargs["start_new_session"] = True

    return subprocess.Popen(cmd, **kwargs)


def _wait_for_backend(api_base: str, *, timeout_s: float = 20.0) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """Poll /health until backend becomes reachable."""
    client = ApiClient(api_base=api_base)
    deadline = time.monotonic() + float(timeout_s)
    sleep_s = 0.25
    last_data: Optional[Dict[str, Any]] = None
    last_err: Optional[str] = None
    while time.monotonic() < deadline:
        ok, data, err = api_health_info(client)
        if ok:
            return True, data, None
        if isinstance(data, dict):
            last_data = data
        if err:
            last_err = err
        time.sleep(sleep_s)
        sleep_s = min(1.5, sleep_s * 1.35)
    return False, last_data, last_err

def _suggest_workspace_name() -> str:
    """Generate a friendly default workspace name."""
    cwd = os.path.basename(os.getcwd()) or "agentjoy"
    host = "local"
    try:
        host = socket.gethostname().split(".")[0] or "local"
    except Exception:
        pass
    name = f"{cwd}-{host}"
    # keep it short (UI-friendly)
    if len(name) > 40:
        name = name[:40]
    return name


def init_flow(args: argparse.Namespace) -> int:
    """Create a Workspace on the backend and persist config.

    This is the fastest way for beginners to get an API key + console token
    without touching curl.
    """
    cfg = load_config()
    profile = _get_profile_name(cfg, getattr(args, "profile", None))
    p = _get_profile(cfg, profile, create=False)
    p_default = _get_profile(cfg, "default", create=False)

    api_base = (
        args.api_base
        or os.environ.get("AGENTJOY_API_BASE")
        or p.get("api_base")
        or p_default.get("api_base")
        or cfg.get("api_base")
        or DEFAULT_API_BASE
    )
    bootstrap_client = ApiClient(api_base=api_base)

    ok, data, err = api_health_info(bootstrap_client)
    if not ok:
        health_url = urljoin(api_base.rstrip("/") + "/", "health")
        print(f"[agentjoy] ERROR: backend is not reachable: {health_url}", file=sys.stderr)
        if err:
            print(f"  reason: {err}", file=sys.stderr)
        print("", file=sys.stderr)
        print("[agentjoy] Quick checks:", file=sys.stderr)
        print(f"  curl {health_url}", file=sys.stderr)
        print("", file=sys.stderr)
        print("[agentjoy] Start backend:", file=sys.stderr)

        py = _python_cmd_hint()
        cwd = os.getcwd()
        rel_candidates = ["backend", os.path.join("..", "backend"), os.path.join("..", "..", "backend")]
        shown = False
        for rel in rel_candidates:
            cand = os.path.normpath(os.path.join(cwd, rel))
            if os.path.isdir(cand):
                cd_part = f'cd "{rel}"' if " " in rel else f"cd {rel}"
                print(f"  {cd_part} && {py} -m uvicorn agentjoy.main:app --reload --port 8000", file=sys.stderr)
                shown = True
                break
        if not shown:
            print(f"  cd backend && {py} -m uvicorn agentjoy.main:app --reload --port 8000", file=sys.stderr)
            if os.name == "nt":
                print(
                    f"  (If you're in packages\\agentjoy-bridge: cd ..\\..\\backend && {py} -m uvicorn agentjoy.main:app --reload --port 8000)",
                    file=sys.stderr,
                )
        return 2

    name = args.name or _suggest_workspace_name()
    try:
        r = api_create_workspace(bootstrap_client, name)
    except Exception as e:
        print(f"[agentjoy] ERROR: failed to create workspace: {e}", file=sys.stderr)
        return 2

    api_key = r.get("api_key")
    owner_user_token = r.get("owner_user_token")
    ws = r.get("workspace") or {}
    if not api_key or not owner_user_token:
        print("[agentjoy] ERROR: unexpected response from backend (missing api_key / owner_user_token).", file=sys.stderr)
        return 2

    # Persist config for subsequent commands (profile-aware).
    cfg = load_config()
    cfg["current_profile"] = profile
    prof = _get_profile(cfg, profile, create=True)
    prof["api_base"] = api_base
    prof["api_key"] = api_key
    prof["user_token"] = owner_user_token
    if getattr(args, "pack", None):
        prof["default_pack"] = args.pack
    if getattr(args, "mode", None):
        prof["default_mode"] = args.mode
    save_config(cfg)

    console_url = f"{api_base.rstrip('/')}/console?token={owner_user_token}"

    print("[agentjoy] ✅ Workspace created")
    print(f"  name: {ws.get('name', name)}")
    if ws.get("id"):
        print(f"  id:   {ws.get('id')}")
    print("")
    print("[agentjoy] Saved config:")
    print(f"  {_config_path()}")
    print(f"  profile: {profile}")
    print("")
    print("[agentjoy] Next (3-min demo):")
    print(f"  {_agentjoy_invocation_hint()} demo --open")
    print("")
    print("[agentjoy] Console:")
    print(f"  {console_url}")

    if getattr(args, "open", False):
        try:
            webbrowser.open(console_url)
        except Exception:
            pass

    return 0


def demo_flow(args: argparse.Namespace, client: ApiClient) -> int:
    """Create a demo run and stream a few events (no Codex required)."""
    title = args.title or "AgentJoy Demo"
    cfg = load_config()
    profile = _get_profile_name(cfg, getattr(args, "profile", None))
    p = _get_profile(cfg, profile, create=False)
    p_default = _get_profile(cfg, "default", create=False)
    pack = (
        args.pack
        or p.get("default_pack")
        or p_default.get("default_pack")
        or cfg.get("default_pack")
        or "default"
    )
    mode = (
        args.mode
        or p.get("default_mode")
        or p_default.get("default_mode")
        or cfg.get("default_mode")
        or "default"
    )

    try:
        r = api_create_run(client, title, mode=mode, pack=pack, metadata={"source": "agentjoy.demo"})
    except Exception as e:
        print(f"[agentjoy] ERROR: failed to create run: {e}", file=sys.stderr)
        return 2

    run = r.get("run") or {}
    run_id = run.get("id")
    publish_token = r.get("publish_token")
    stream_url = r.get("stream_url")
    if not run_id:
        print("[agentjoy] ERROR: run id missing from response.", file=sys.stderr)
        return 2

    steps = int(getattr(args, "steps", 12) or 12)
    sleep_s = float(getattr(args, "sleep", 0.25) or 0.25)

    # A short, user-facing event script.
    script: List[Dict[str, Any]] = [
        {"type": "phase.started", "phase": "prepare", "message": "準備中…", "progress": 0.05, "actor": "system"},
        {"type": "system.comment", "message": "はじめまして。いまから “見守り” を始めます。", "actor": "system"},
        {"type": "tool.called", "phase": "prepare", "message": "環境チェック", "progress": 0.10, "actor": "tool",
         "meta": {"tool_call_id": "demo_env_check"},
         "tool": {"name": "env.check", "input_summary": "node/python versions"}},
        {"type": "tool.completed", "phase": "prepare", "message": "環境OK", "progress": 0.18, "actor": "tool",
         "meta": {"tool_call_id": "demo_env_check"},
         "tool": {"name": "env.check", "output_summary": "all green", "latency_ms": 120}},
        {"type": "phase.started", "phase": "research", "message": "情報収集中…", "progress": 0.25, "actor": "agent"},
        {"type": "tool.called", "phase": "research", "message": "関連ファイルを探索", "progress": 0.33, "actor": "tool",
         "meta": {"tool_call_id": "demo_repo_scan"},
         "tool": {"name": "repo.scan", "input_summary": "README / src / tests"}},
        {"type": "tool.completed", "phase": "research", "message": "探索完了", "progress": 0.45, "actor": "tool",
         "meta": {"tool_call_id": "demo_repo_scan"},
         "tool": {"name": "repo.scan", "output_summary": "found 12 relevant files", "latency_ms": 420}},
        {"type": "phase.started", "phase": "execute", "message": "実装案を組み立て中…", "progress": 0.55, "actor": "agent"},
        {"type": "tool.called", "phase": "execute", "message": "変更案を生成", "progress": 0.62, "actor": "tool",
         "meta": {"tool_call_id": "demo_plan_generate"},
         "tool": {"name": "plan.generate", "input_summary": "onboarding + UX"}},
        {"type": "tool.completed", "phase": "execute", "message": "変更案OK", "progress": 0.78, "actor": "tool",
         "meta": {"tool_call_id": "demo_plan_generate"},
         "tool": {"name": "plan.generate", "output_summary": "3 improvements", "latency_ms": 780}},
        {"type": "artifact.ready", "phase": "format", "message": "成果物を整形", "progress": 0.88, "actor": "agent",
         "artifacts": [{"kind": "text", "label": "Summary", "value": "✅ README / ✅ CLI / ✅ Widget"}]},
        {"type": "phase.started", "phase": "finalize", "message": "最終確認…", "progress": 0.95, "actor": "system"},
        {"type": "run.completed", "message": "完了！見守りURLを共有できます。", "progress": 1.0, "actor": "system"},
    ]

    # Trim/expand script to requested steps (best-effort)
    if steps < len(script):
        script = script[:steps]
    elif steps > len(script):
        # pad with gentle progress events
        p = 0.96
        while len(script) < steps - 1:
            p = min(0.99, p + 0.01)
            script.insert(-1, {"type": "phase.progress", "phase": "finalize", "message": "仕上げ中…", "progress": p, "actor": "system"})

    for ev in script:
        try:
            api_post_events(client, run_id, [ev])
        except Exception as e:
            print(f"[agentjoy] WARN: failed to post event: {e}", file=sys.stderr)
            break
        time.sleep(sleep_s)

    share_url = None
    if getattr(args, "share", True):
        share_url = api_share_run(client, run_id, expires_in_hours=int(getattr(args, "share_hours", 72)))

    print("[agentjoy] ✅ Demo run created")
    print(f"  run_id: {run_id}")
    if stream_url:
        print(f"  stream_url: {stream_url}")
    if publish_token:
        print(f"  publish_token: {publish_token}")
    if share_url:
        print(f"  share_url: {share_url}")
    else:
        print("  share_url: (not created)")

    if getattr(args, "open", False) and share_url:
        try:
            webbrowser.open(share_url)
        except Exception:
            pass

    return 0


def quickstart_flow(args: argparse.Namespace) -> int:
    """One command onboarding: (optionally) start backend -> init -> demo.

    Goals:
      - Reduce "2 terminals + 4 commands" into a single, reliable command.
      - Be resilient on Windows where PATH is often not configured.
    """

    # 1) Resolve API base (profile-aware)
    cfg0 = load_config()
    profile = _get_profile_name(cfg0, getattr(args, "profile", None))
    p_prof = _get_profile(cfg0, profile, create=False)
    p_default = _get_profile(cfg0, "default", create=False)
    api_base = (
        getattr(args, "api_base", None)
        or os.environ.get("AGENTJOY_API_BASE")
        or p_prof.get("api_base")
        or p_default.get("api_base")
        or cfg0.get("api_base")
        or DEFAULT_API_BASE
    )
    host, port, scheme = _parse_api_base(api_base)

    # 2) Ensure backend is reachable (auto-start if requested)
    bootstrap_client = ApiClient(api_base=api_base)
    ok, data, err = api_health_info(bootstrap_client)

    backend_proc: Optional[subprocess.Popen] = None
    backend_log = args.backend_log or _backend_log_path()

    if not ok and getattr(args, "start_backend", True):
        backend_dir = args.backend_dir or _find_backend_dir(os.getcwd())
        if not backend_dir:
            health_url = urljoin(api_base.rstrip("/") + "/", "health")
            print(f"[agentjoy] ERROR: backend is not reachable: {health_url}", file=sys.stderr)
            if err:
                print(f"  reason: {err}", file=sys.stderr)
            print("", file=sys.stderr)
            print("[agentjoy] I also tried to auto-start the backend, but could not find ./backend/ in this directory tree.", file=sys.stderr)
            print("  tip: run this command from the repo root, or start backend manually:", file=sys.stderr)
            py = _python_cmd_hint()
            print(f"  cd backend && {py} -m uvicorn agentjoy.main:app --reload --port {port}", file=sys.stderr)
            return 2

        # If the chosen port is busy (and it's not AgentJoy), scan a few ports.
        if getattr(args, "auto_port", True) and _is_port_listening(host, port):
            new_port = _pick_free_port(host, port)
            if new_port != port:
                print(f"[agentjoy] Port {port} is busy. Starting backend on port {new_port} instead.")
                port = new_port
                api_base = f"{scheme}://{host}:{port}"
                bootstrap_client = ApiClient(api_base=api_base)

        public_base_url = f"{scheme}://{host}:{port}"
        print("[agentjoy] Starting backend…")
        try:
            backend_proc = _start_backend_uvicorn(
                backend_dir=backend_dir,
                host=host,
                port=port,
                public_base_url=public_base_url,
                reload=bool(getattr(args, "dev", False)),
                log_path=backend_log,
            )
        except Exception as e:
            print(f"[agentjoy] ERROR: failed to start backend: {e}", file=sys.stderr)
            print(f"  backend_dir: {backend_dir}", file=sys.stderr)
            print(f"  log: {backend_log}", file=sys.stderr)
            return 2

        ok, data, err = _wait_for_backend(api_base, timeout_s=float(getattr(args, "wait", 20.0)))
        if not ok:
            health_url = urljoin(api_base.rstrip("/") + "/", "health")
            print(f"[agentjoy] ERROR: backend did not become ready: {health_url}", file=sys.stderr)
            if err:
                print(f"  reason: {err}", file=sys.stderr)
            if backend_proc and backend_proc.poll() is not None:
                print(f"  backend process exited (code={backend_proc.returncode}).", file=sys.stderr)
            print(f"  log: {backend_log}", file=sys.stderr)
            print("", file=sys.stderr)
            print("[agentjoy] Common fixes:", file=sys.stderr)
            py = _python_cmd_hint()
            print(f"  cd backend && {py} -m pip install -r requirements.txt  # core (pure-Python)", file=sys.stderr)
            print(f"  # optional full deps (OGP images / speedups): cd backend && {py} -m pip install -r requirements-full.txt", file=sys.stderr)
            print(f"  cd backend && {py} -m uvicorn agentjoy.main:app --reload --port {port}", file=sys.stderr)
            return 2

        if backend_proc and backend_proc.poll() is None:
            pid = backend_proc.pid
            print(f"[agentjoy] ✅ Backend started (pid={pid})")
            print(f"  api_base: {api_base}")
            print(f"  log: {backend_log}")

    elif not ok:
        health_url = urljoin(api_base.rstrip("/") + "/", "health")
        print(f"[agentjoy] ERROR: backend is not reachable: {health_url}", file=sys.stderr)
        if err:
            print(f"  reason: {err}", file=sys.stderr)
        print("  tip: start backend or run with --start-backend", file=sys.stderr)
        return 2

    # 3) Ensure we have a valid API key for the selected profile.
    cfg = load_config()
    profile = _get_profile_name(cfg, getattr(args, "profile", None))
    prof = _get_profile(cfg, profile, create=False)

    need_init = bool(getattr(args, "force_init", False))
    if not need_init:
        if not prof.get("api_key") or not prof.get("user_token"):
            need_init = True

    if not need_init:
        # Validate key (non-mutating): GET /v1/workspaces/me
        try:
            ApiClient(api_base=api_base, api_key=str(prof.get("api_key"))).get("/v1/workspaces/me")
        except Exception:
            need_init = True
        else:
            # Key is valid; update api_base in profile if needed.
            if prof.get("api_base") != api_base:
                prof["api_base"] = api_base
                cfg["current_profile"] = profile
                save_config(cfg)

    if need_init:
        # Backup config if it exists (avoid surprise overwrite).
        try:
            if os.path.isfile(_config_path()):
                ts = datetime.now().strftime("%Y%m%d-%H%M%S")
                bak = _config_path() + f".bak-{ts}"
                with open(_config_path(), "rb") as rf:
                    raw = rf.read()
                with open(bak, "wb") as wf:
                    wf.write(raw)
        except Exception:
            pass

        init_args = argparse.Namespace(
            profile=profile,
            api_base=api_base,
            name=getattr(args, "name", None),
            pack=getattr(args, "pack", None),
            mode=getattr(args, "mode", None),
            open=bool(getattr(args, "open_console", False) or getattr(args, "open", False)),
        )
        rc = init_flow(init_args)
        if rc != 0:
            return rc

    # Reload config after init.
    cfg = load_config()
    profile = _get_profile_name(cfg, getattr(args, "profile", None))
    prof = _get_profile(cfg, profile, create=False)
    client = ApiClient(api_base=api_base, api_key=prof.get("api_key"), user_token=prof.get("user_token"))

    # Proof-of-life for the Connect page (non-failing)
    api_connect_ping_best_effort(client, "bridge", profile=profile, note="quickstart")

    # 4) Demo run (optional)
    if not getattr(args, "no_demo", False):
        demo_args = argparse.Namespace(
            profile=profile,
            title=getattr(args, "title", "AgentJoy Demo"),
            pack=getattr(args, "pack", None),
            mode=getattr(args, "mode", None),
            steps=int(getattr(args, "steps", 12) or 12),
            sleep=float(getattr(args, "sleep", 0.25) or 0.25),
            share=bool(getattr(args, "share", True)),
            share_hours=int(getattr(args, "share_hours", 72) or 72),
            open=bool(getattr(args, "open", False)),
        )
        rc = demo_flow(demo_args, client)
        if rc != 0:
            return rc

    # 5) Final hints
    cmd = _agentjoy_invocation_hint()
    print("")
    print("[agentjoy] Next:")
    print(f"  {cmd} demo --open")
    print(f"  {cmd} codex-run \"Fix failing tests\"")

    # If we started backend, give stop hint.
    if backend_proc and backend_proc.poll() is None:
        pid = backend_proc.pid
        print("")
        print("[agentjoy] Stop backend:")
        if _is_windows():
            print(f"  taskkill /PID {pid} /F")
        else:
            print(f"  kill {pid}")

    return 0


def profile_flow(args: argparse.Namespace) -> int:
    """Manage multiple config profiles (local/staging/prod)."""
    cfg = load_config()
    profiles = _get_profiles(cfg)

    subcmd = getattr(args, "profile_cmd", None) or "list"

    if subcmd == "list":
        if not profiles:
            print("[agentjoy] No profiles configured yet.")
            print(f"  config: {_config_path()}")
            print("  next: agentjoy init  # or: agentjoy profile set <name> --api ...")
            return 1
        cur = cfg.get("current_profile") or "default"
        print("[agentjoy] Profiles")
        for name in sorted(profiles.keys()):
            p = profiles.get(name) if isinstance(profiles.get(name), dict) else {}
            mark = "*" if name == cur else " "
            api_base = p.get("api_base") or "(unset)"
            k = "set" if p.get("api_key") else "unset"
            t = "set" if p.get("user_token") else "unset"
            print(f"  {mark} {name}")
            print(f"     api_base: {api_base}")
            print(f"     api_key:  {k}  user_token: {t}")
        return 0

    if subcmd == "show":
        name = getattr(args, "name", None) or cfg.get("current_profile") or "default"
        if name not in profiles:
            print(f"[agentjoy] ERROR: profile not found: {name}", file=sys.stderr)
            return 2
        p = _get_profile(cfg, name, create=False)
        out = {
            "name": name,
            "current": bool(name == (cfg.get("current_profile") or "default")),
            "api_base": p.get("api_base"),
            "api_key": _mask_secret(p.get("api_key")),
            "user_token": _mask_secret(p.get("user_token")),
            "default_pack": p.get("default_pack"),
            "default_mode": p.get("default_mode"),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    if subcmd == "use":
        name = getattr(args, "name", None)
        if not name:
            print("[agentjoy] ERROR: profile name is required.", file=sys.stderr)
            return 2
        if name not in profiles:
            print(f"[agentjoy] ERROR: profile not found: {name}", file=sys.stderr)
            return 2
        cfg["current_profile"] = name
        save_config(cfg)
        print(f"[agentjoy] ✅ current profile: {name}")
        return 0

    if subcmd == "set":
        name = getattr(args, "name", None)
        if not name:
            print("[agentjoy] ERROR: profile name is required.", file=sys.stderr)
            return 2
        p = _get_profile(cfg, name, create=True)
        if getattr(args, "api_base", None):
            p["api_base"] = args.api_base
        if getattr(args, "api_key", None):
            p["api_key"] = args.api_key
        if getattr(args, "user_token", None):
            p["user_token"] = args.user_token
        if getattr(args, "pack", None):
            p["default_pack"] = args.pack
        if getattr(args, "mode", None):
            p["default_mode"] = args.mode
        # Optional: switch current profile on request.
        if bool(getattr(args, "use", False)):
            cfg["current_profile"] = name
        save_config(cfg)
        print(f"[agentjoy] ✅ profile saved: {name}")
        if not bool(getattr(args, "use", False)):
            print(f"  tip: agentjoy profile use {name}")
        return 0

    if subcmd == "delete":
        name = getattr(args, "name", None)
        if not name:
            print("[agentjoy] ERROR: profile name is required.", file=sys.stderr)
            return 2
        if name not in profiles:
            print(f"[agentjoy] ERROR: profile not found: {name}", file=sys.stderr)
            return 2
        profiles.pop(name, None)
        if cfg.get("current_profile") == name:
            cfg["current_profile"] = next(iter(profiles.keys()), "default")
        save_config(cfg)
        print(f"[agentjoy] ✅ profile deleted: {name}")
        return 0

    print(f"[agentjoy] ERROR: unknown profile subcommand: {subcmd}", file=sys.stderr)
    return 2


def doctor_flow(args: argparse.Namespace) -> int:
    """Environment + configuration diagnostics."""
    cfg = load_config()
    profile = _get_profile_name(cfg, getattr(args, "profile", None))
    profiles = _get_profiles(cfg)

    warnings: List[str] = []
    errors: List[str] = []

    # Core environment
    print("[agentjoy] doctor")
    print(f"  os: {platform.system()} {platform.release()} ({os.name})")
    print(f"  python: {platform.python_version()}")
    print(f"  executable: {sys.executable}")

    # PATH / entrypoint
    on_path = bool(shutil_which("agentjoy"))
    print(f"  agentjoy on PATH: {on_path}")

    if _is_windows():
        scripts_dir = None
        try:
            scripts_dir = sysconfig.get_path("scripts", scheme="nt_user")
        except Exception:
            scripts_dir = None
        if scripts_dir:
            path_parts = [os.path.normcase(p) for p in os.environ.get("PATH", "").split(os.pathsep) if p]
            scripts_on_path = os.path.normcase(scripts_dir) in path_parts
            print(f"  scripts_dir: {scripts_dir}")
            print(f"  scripts_dir on PATH: {scripts_on_path}")
            if not scripts_on_path:
                warnings.append("User Scripts directory is not on PATH (agentjoy command may not be found).")
        else:
            warnings.append("Could not resolve user scripts directory (Windows PATH check skipped).")

    # Config / profiles
    conf_path = _config_path()
    print(f"  config: {conf_path} ({'exists' if os.path.isfile(conf_path) else 'missing'})")
    if profiles:
        cur = cfg.get("current_profile") or "default"
        print(f"  profiles: {', '.join(sorted(profiles.keys()))} (current={cur})")
    else:
        warnings.append("No profiles configured yet. Run `agentjoy init` (or `agentjoy profile set`).")
    print(f"  selected profile: {profile}")

    # Effective connection settings
    client = build_client_from_args(args)
    print(f"  api_base: {client.api_base}")
    print(f"  api_key: {_mask_secret(client.api_key)}")
    print(f"  user_token: {_mask_secret(client.user_token)}")

    # Backend reachability
    ok, data, err = api_health_info(ApiClient(api_base=client.api_base))
    if ok:
        print("  backend /health: ok")
        if isinstance(data, dict):
            print(f"    {json.dumps(data, ensure_ascii=False)}")

        # Proof-of-life (doctor counts as "bridge can talk to backend")
        api_connect_ping_best_effort(client, "doctor", profile=profile, note="doctor")
    else:
        print("  backend /health: failed")
        if err:
            print(f"    reason: {err}")
        errors.append("Backend is not reachable. Start backend (or use quickstart).")

    # Backend capabilities (optional)
    # - Helps when bridge/backend drift happens
    # - Helps users debug "422" issues in a self-serve manner
    okc, cap, errc = api_capabilities_info(ApiClient(api_base=client.api_base))
    if okc and isinstance(cap, dict):
        print("  backend /v1/capabilities: ok")
        try:
            print(f"    api_schema_version={cap.get('api_schema_version')}, version={cap.get('version')}")
        except Exception:
            pass

        accepted = cap.get("accepted") if isinstance(cap.get("accepted"), dict) else {}
        ev = accepted.get("event_types")
        ph = accepted.get("phases")
        if isinstance(ev, list):
            ev_set = {str(x) for x in ev if x is not None}
            missing = sorted(list(VALID_EVENT_TYPES - ev_set))
            extra = sorted(list(ev_set - VALID_EVENT_TYPES))
            if missing or extra:
                warnings.append(
                    "Backend capabilities 'event_types' differs from bridge defaults. "
                    f"missing={missing[:6]}{'…' if len(missing) > 6 else ''} "
                    f"extra={extra[:6]}{'…' if len(extra) > 6 else ''}"
                )
        if isinstance(ph, list):
            ph_set = {str(x) for x in ph if x is not None}
            missing_p = sorted(list(VALID_PHASES - ph_set))
            extra_p = sorted(list(ph_set - VALID_PHASES))
            if missing_p or extra_p:
                warnings.append(
                    "Backend capabilities 'phases' differs from bridge defaults. "
                    f"missing={missing_p[:6]}{'…' if len(missing_p) > 6 else ''} "
                    f"extra={extra_p[:6]}{'…' if len(extra_p) > 6 else ''}"
                )
    else:
        # Don't treat as an error (backward compatible)
        if errc:
            warnings.append("/v1/capabilities not available (older backend or blocked).")

    # API key validation
    if client.api_key:
        try:
            ws = ApiClient(api_base=client.api_base, api_key=client.api_key).get("/v1/workspaces/me")
            if isinstance(ws, dict):
                print("  api_key access: ok")
                if ws.get("name"):
                    print(f"    workspace: {ws.get('name')}")
        except Exception as e:
            print("  api_key access: failed")
            print(f"    reason: {e}")
            errors.append("API key is missing or invalid for this api_base.")
    else:
        warnings.append("api_key is not configured. Run `agentjoy init` or `agentjoy configure --api-key ...`. ")

    # User token validation (console/admin)
    if client.user_token:
        try:
            ws2 = ApiClient(api_base=client.api_base, user_token=client.user_token).get("/v1/workspaces/me/by-user", use_user=True)
            if isinstance(ws2, dict):
                print("  user_token access: ok")
        except Exception as e:
            print("  user_token access: failed")
            print(f"    reason: {e}")
            warnings.append("user_token seems invalid (console/admin endpoints may not work).")
    else:
        warnings.append("user_token is not configured. `--open` console shortcuts may not work.")

    # Tooling checks
    if shutil_which("codex") is None:
        warnings.append("`codex` command not found (codex-run will not work until installed).")

    # Optional write-test (creates a run)
    if bool(getattr(args, "write_test", False)):
        if not client.api_key:
            errors.append("write-test requires api_key.")
        elif not ok:
            errors.append("write-test requires backend to be reachable.")
        else:
            try:
                # small, harmless run with a single event
                pack, mode = resolve_pack_mode(args)
                r = api_create_run(ApiClient(api_base=client.api_base, api_key=client.api_key), "Doctor write-test", mode=mode, pack=pack, metadata={"source": "agentjoy.doctor"})
                run_id = (r.get("run") or {}).get("id")
                if run_id:
                    api_post_events(ApiClient(api_base=client.api_base, api_key=client.api_key), run_id, [{
                        "type": "system.comment",
                        "phase": "check",
                        "message": "doctor write-test: ok",
                        "detail": None,
                    }])
                    print("  write-test: ok")
                    share_url = api_share_run(ApiClient(api_base=client.api_base, api_key=client.api_key), run_id)
                    if share_url:
                        print(f"    share_url: {share_url}")
                else:
                    errors.append("write-test failed: run_id missing")
            except Exception as e:
                errors.append(f"write-test failed: {e}")

    # Summary
    print("")
    if errors:
        print("[agentjoy] ❌ issues")
        for m in errors:
            print(f"  - {m}")
    if warnings:
        print("[agentjoy] ⚠ warnings")
        for m in warnings:
            print(f"  - {m}")

    if errors:
        return 2
    if warnings:
        return 1
    print("[agentjoy] ✅ looks good")
    return 0


def adapters_flow(args: argparse.Namespace) -> int:
    """Show/initialize adapter overrides used for compatibility."""
    path = _adapters_path()
    if getattr(args, "path", False):
        print(path)
        return 0

    if getattr(args, "init", False):
        p = write_adapters_template(force=getattr(args, "force", False))
        print(f"[agentjoy] ✅ adapters template written: {p}")
        print("[agentjoy] Edit this file to add dot-path overrides (optional).")
        return 0

    overrides = load_adapters()
    exists = os.path.isfile(path)
    print("[agentjoy] adapters")
    print(f"  path: {path} ({'exists' if exists else 'missing'})")
    if not exists:
        print("  tip: run `agentjoy adapters --init` to create a template")
        return 0

    try:
        keys = sorted([k for k in overrides.keys() if isinstance(k, str)])
    except Exception:
        keys = []
    print(f"  adapters: {', '.join(keys) if keys else '(none)'}")
    # Print a compact preview (safe to copy-paste)
    try:
        preview = json.dumps(overrides, ensure_ascii=False, indent=2)
        print("\n" + preview)
    except Exception:
        print("  (failed to render JSON preview)")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="agentjoy", description="Bridge Codex/Claude activity into AgentJoy runs.")
    # Do not hard-error on missing subcommand.
    # Many beginners will type `agentjoy` expecting "start". Instead of an
    # argparse error, show a friendly "next step".
    sub = p.add_subparsers(dest="cmd", required=False)

    # Shared option: choose a config profile (local / staging / prod). We attach this to
    # each subcommand so users can write: `agentjoy <cmd> --profile staging ...`.
    profile_parent = argparse.ArgumentParser(add_help=False)
    profile_parent.add_argument("--profile", default=None, help="Config profile name (default: current_profile).")

    # quickstart
    pqs = sub.add_parser(
        "quickstart",
        help="One command onboarding: start backend (if needed) -> init -> demo.",
        parents=[profile_parent],
    )
    pqs.add_argument("--api-base", "--api", dest="api_base", default=None)
    pqs.add_argument("--name", default=None, help="Workspace name (optional).")
    pqs.add_argument("--title", default="AgentJoy Demo", help="Demo run title.")
    pqs.add_argument("--pack", default=None)
    pqs.add_argument("--mode", default=None)
    pqs.add_argument("--open", action="store_true", help="Open share URL (and console when bootstrapping).")
    pqs.add_argument("--open-console", dest="open_console", action="store_true", help="Open console after init.")
    pqs.add_argument("--no-demo", dest="no_demo", action="store_true", help="Skip demo run creation.")
    pqs.add_argument("--force-init", dest="force_init", action="store_true", help="Always create a new workspace/config.")
    pqs.add_argument("--no-start-backend", dest="start_backend", action="store_false", help="Do not auto-start backend.")
    pqs.set_defaults(start_backend=True)
    pqs.add_argument("--no-auto-port", dest="auto_port", action="store_false", help="Do not auto-pick a free port.")
    pqs.set_defaults(auto_port=True)
    pqs.add_argument("--backend-dir", dest="backend_dir", default=None, help="Backend directory (auto-detected by default).")
    pqs.add_argument("--backend-log", dest="backend_log", default=None, help="Backend log file path.")
    pqs.add_argument("--wait", type=float, default=20.0, help="Seconds to wait for backend readiness.")
    pqs.add_argument("--dev", action="store_true", help="Start backend with --reload (dev mode).")
    # Demo tuning
    pqs.add_argument("--steps", type=int, default=12)
    pqs.add_argument("--sleep", type=float, default=0.25)
    pqs.add_argument("--share", action="store_true", default=True)
    pqs.add_argument("--no-share", dest="share", action="store_false")
    pqs.add_argument("--share-hours", dest="share_hours", type=int, default=72)

    # init (bootstrap)
    pinit = sub.add_parser("init", help="Create a workspace and save config (fastest setup).", parents=[profile_parent])
    pinit.add_argument("--name", default=None, help="Workspace name (optional).")
    pinit.add_argument("--api-base", "--api", dest="api_base", default=None)
    pinit.add_argument("--pack", default=None, help="Default persona pack (optional).")
    pinit.add_argument("--mode", default=None, help="Default mode (professional/playful).")
    pinit.add_argument("--open", action="store_true", help="Open console in browser after init.")

    # demo (no Codex required)
    pdemo = sub.add_parser("demo", help="Create a demo run and stream a few fake events.", parents=[profile_parent])
    pdemo.add_argument("--title", default="AgentJoy Demo")
    pdemo.add_argument("--pack", default=None)
    pdemo.add_argument("--mode", default=None)
    pdemo.add_argument("--steps", type=int, default=12)
    pdemo.add_argument("--sleep", type=float, default=0.25, help="Seconds between events.")
    pdemo.add_argument("--share", action="store_true", default=True)
    pdemo.add_argument("--no-share", dest="share", action="store_false")
    pdemo.add_argument("--share-hours", dest="share_hours", type=int, default=72)
    pdemo.add_argument("--open", action="store_true", help="Open share URL in browser (if created).")
    pdemo.add_argument("--api-base", "--api", dest="api_base", default=None)
    pdemo.add_argument("--api-key", default=None)
    pdemo.add_argument("--user-token", default=None)

    # configure
    pcfg = sub.add_parser("configure", help="Save AgentJoy API settings to ~/.agentjoy/config.json", parents=[profile_parent])
    pcfg.add_argument("--api-base", "--api", dest="api_base", default=None)
    pcfg.add_argument("--api-key", default=None)
    pcfg.add_argument("--user-token", default=None)
    pcfg.add_argument("--pack", default=None)
    pcfg.add_argument("--mode", default=None)

    # adapters (compat)
    pad = sub.add_parser("adapters", help="Show/initialize Bridge adapter overrides (compat layer).")
    pad.add_argument("--init", action="store_true", help="Write a template overrides file under ~/.agentjoy/")
    pad.add_argument("--force", action="store_true", help="Overwrite the file when used with --init")
    pad.add_argument("--path", action="store_true", help="Print the overrides file path and exit")

    # health
    phealth = sub.add_parser("health", help="Check AgentJoy backend health", parents=[profile_parent])
    phealth.add_argument("--api-base", "--api", dest="api_base", default=None)

    # codex-run
    pcodex = sub.add_parser("codex-run", help="Run `codex exec --json` and stream into AgentJoy", parents=[profile_parent])
    pcodex.add_argument("prompt", help="Prompt passed to codex exec")
    pcodex.add_argument("--title", default=None)
    pcodex.add_argument("--pack", default=None)
    pcodex.add_argument("--mode", default=None)
    pcodex.add_argument("--share", action="store_true", default=True)
    pcodex.add_argument("--no-share", dest="share", action="store_false")
    pcodex.add_argument("--api-base", "--api", dest="api_base", default=None)
    pcodex.add_argument("--api-key", default=None)
    pcodex.add_argument("--user-token", default=None)
    pcodex.add_argument("--codex-args", nargs=argparse.REMAINDER, help="Extra args after -- passed to codex")

    # codex-stream
    pstream = sub.add_parser("codex-stream", help="Read Codex JSONL from stdin and stream into AgentJoy", parents=[profile_parent])
    pstream.add_argument("--title", default="Codex (stdin)")
    pstream.add_argument("--pack", default=None)
    pstream.add_argument("--mode", default=None)
    pstream.add_argument("--share", action="store_true", default=True)
    pstream.add_argument("--no-share", dest="share", action="store_false")
    pstream.add_argument("--api-base", "--api", dest="api_base", default=None)
    pstream.add_argument("--api-key", default=None)
    pstream.add_argument("--user-token", default=None)

    # claude-hook
    pcl = sub.add_parser("claude-hook", help="Claude Code hook entrypoint (reads JSON from stdin).", parents=[profile_parent])
    pcl.add_argument("--title", default=None)
    pcl.add_argument("--pack", default=None)
    pcl.add_argument("--mode", default=None)
    pcl.add_argument("--share", action="store_true", default=True)
    pcl.add_argument("--no-share", dest="share", action="store_false")
    pcl.add_argument("--api-base", "--api", dest="api_base", default=None)
    pcl.add_argument("--api-key", default=None)
    pcl.add_argument("--user-token", default=None)

    # doctor (diagnostics)
    pdoc = sub.add_parser("doctor", help="Diagnose environment + configuration.", parents=[profile_parent])
    pdoc.add_argument("--api-base", "--api", dest="api_base", default=None)
    pdoc.add_argument("--api-key", default=None)
    pdoc.add_argument("--user-token", default=None)
    pdoc.add_argument("--write-test", dest="write_test", action="store_true", help="Create a small run+event to verify write access.")
    # Optional defaults for write-test
    pdoc.add_argument("--pack", default=None)
    pdoc.add_argument("--mode", default=None)

    # profile management
    pprof = sub.add_parser("profile", help="Manage multiple config profiles (local/staging/prod).")
    ppsub = pprof.add_subparsers(dest="profile_cmd", required=True)
    ppsub.add_parser("list", help="List profiles")

    pshow = ppsub.add_parser("show", help="Show a profile (redacted secrets)")
    pshow.add_argument("name", nargs="?", default=None)

    puse = ppsub.add_parser("use", help="Set current profile")
    puse.add_argument("name")

    pset = ppsub.add_parser("set", help="Create/update a profile")
    pset.add_argument("name")
    pset.add_argument("--api-base", "--api", dest="api_base", default=None)
    pset.add_argument("--api-key", default=None)
    pset.add_argument("--user-token", default=None)
    pset.add_argument("--pack", default=None)
    pset.add_argument("--mode", default=None)
    pset.add_argument("--use", action="store_true", help="Also set as current profile")

    pdel = ppsub.add_parser("delete", help="Delete a profile")
    pdel.add_argument("name")

    args = p.parse_args(argv)

    # No subcommand: show help + a single recommended next step.
    if not getattr(args, "cmd", None):
        p.print_help()
        print("")
        inv = _agentjoy_invocation_hint()
        print("Next step (recommended):")
        print(f"  {inv} quickstart --open")
        print("Other useful commands:")
        print(f"  {inv} doctor")
        print(f"  {inv} configure")
        return 0

    if args.cmd == "quickstart":
        return quickstart_flow(args)

    if args.cmd == "init":
        return init_flow(args)

    if args.cmd == "profile":
        return profile_flow(args)

    if args.cmd == "doctor":
        return doctor_flow(args)

    if args.cmd == "configure":
        cfg = load_config()
        profile = _get_profile_name(cfg, getattr(args, "profile", None))
        prof = _get_profile(cfg, profile, create=True)
        if args.api_base:
            prof["api_base"] = args.api_base
        if args.api_key:
            prof["api_key"] = args.api_key
        if args.user_token:
            prof["user_token"] = args.user_token
        if args.pack:
            prof["default_pack"] = args.pack
        if args.mode:
            prof["default_mode"] = args.mode
        # If user explicitly picked a profile, assume they want to use it.
        if getattr(args, "profile", None):
            cfg["current_profile"] = profile
        save_config(cfg)
        print(f"Saved: {_config_path()}")
        print(f"  profile: {profile}")
        return 0

    if args.cmd == "adapters":
        return adapters_flow(args)

    if args.cmd == "health":
        client = build_client_from_args(args)
        ok, data, err = api_health_info(client)
        if ok:
            print("ok")
            if isinstance(data, dict):
                print(json.dumps(data, ensure_ascii=False))
            return 0
        print("failed")
        if err:
            print(err, file=sys.stderr)
        return 1

    client = build_client_from_args(args)
    if not client.api_key and args.cmd in {"codex-run", "codex-stream", "claude-hook", "demo"}:
        print("[agentjoy] ERROR: api_key is required. Set AGENTJOY_API_KEY or run `agentjoy configure --api-key ...`", file=sys.stderr)
        return 2

    if args.cmd == "demo":
        return demo_flow(args, client)

    if args.cmd == "codex-run":
        # Ensure codex exists
        if shutil_which("codex") is None:
            print("[agentjoy] ERROR: `codex` command not found. Install OpenAI Codex CLI first.", file=sys.stderr)
            return 2
        extra = args.codex_args or []
        # `--` separator is typical; if present, drop it
        if extra and extra[0] == "--":
            extra = extra[1:]
        args.codex_args = extra
        return codex_run_flow(args, client)

    if args.cmd == "codex-stream":
        return codex_stream_flow(args, client)

    if args.cmd == "claude-hook":
        return claude_hook_flow(args, client)

    return 0


def shutil_which(cmd: str) -> Optional[str]:
    # tiny replacement for shutil.which to avoid importing shutil everywhere
    path = os.environ.get("PATH", "")
    exts = [""]  # on windows, PATHEXT is relevant
    if os.name == "nt":
        exts = os.environ.get("PATHEXT", ".EXE;.BAT;.CMD").split(";")
    for p in path.split(os.pathsep):
        for ext in exts:
            cand = os.path.join(p, cmd + ext)
            if os.path.isfile(cand) and os.access(cand, os.X_OK):
                return cand
    return None


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as e:
        print(f"[agentjoy] fatal: {e}", file=sys.stderr)
        traceback.print_exc()
        raise SystemExit(1)
