from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .actions import ActionRegistry, maybe_parse_action_task
from .providers import FakeProvider, LocalHTTPProvider, NoneProvider, Provider

_UTC = dt.UTC

DEFAULT_CONFIG = """roles:
  manager: planner
  worker: executor
  reviewer: verifier
budgets:
  max_steps: 8
  max_actions: 4
  token_budget: 0
provider:
  type: none
  endpoint: http://127.0.0.1:11434/api/generate
  model: llama3
safety:
  write_allowlist:
    - .sdetkit/agent/workdir
  shell_allowlist:
    - python
"""


@dataclass(frozen=True)
class AgentConfig:
    roles: dict[str, str]
    budgets: dict[str, int]
    provider: dict[str, str]
    safety: dict[str, tuple[str, ...]]


def _captured_at() -> str:
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return dt.datetime.fromtimestamp(int(epoch), tz=_UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt.datetime.now(tz=_UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical_json_dumps(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n"


def _canonical_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def _sha(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _parse_scalar(raw: str) -> Any:
    val = raw.strip()
    if val in {"", "null", "~"}:
        return None
    if val.isdigit():
        return int(val)
    if val.lower() in {"true", "false"}:
        return val.lower() == "true"
    return val


def _load_yaml_like(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    section: str | None = None
    subsection: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if indent == 0 and stripped.endswith(":"):
            section = stripped[:-1]
            data.setdefault(section, {})
            subsection = None
            continue
        if section is None:
            continue
        if indent == 2 and stripped.endswith(":"):
            subsection = stripped[:-1]
            if isinstance(data[section], dict):
                data[section][subsection] = []
            continue
        if indent == 2 and ":" in stripped:
            key, value = stripped.split(":", 1)
            if isinstance(data[section], dict):
                data[section][key.strip()] = _parse_scalar(value)
            subsection = None
            continue
        if indent == 4 and ":" in stripped and isinstance(data[section], dict):
            key, value = stripped.split(":", 1)
            parent = data[section]
            if isinstance(parent.get(subsection or ""), dict):
                parent[subsection or ""][key.strip()] = _parse_scalar(value)
            elif subsection:
                parent[subsection] = {key.strip(): _parse_scalar(value)}
            else:
                parent[key.strip()] = _parse_scalar(value)
            continue
        if (
            indent >= 4
            and stripped.startswith("- ")
            and subsection
            and isinstance(data[section], dict)
        ):
            parent = data[section]
            current = parent.get(subsection)
            if not isinstance(current, list):
                current = []
                parent[subsection] = current
            current.append(_parse_scalar(stripped[2:]))
    return data


def load_config(path: Path) -> AgentConfig:
    raw = _load_yaml_like(path)
    roles_raw = raw.get("roles")
    budgets_raw = raw.get("budgets")
    provider_raw = raw.get("provider")
    safety_raw = raw.get("safety")
    roles = cast(dict[str, Any], roles_raw if isinstance(roles_raw, dict) else {})
    budgets = cast(dict[str, Any], budgets_raw if isinstance(budgets_raw, dict) else {})
    provider = cast(dict[str, Any], provider_raw if isinstance(provider_raw, dict) else {})
    safety = cast(dict[str, Any], safety_raw if isinstance(safety_raw, dict) else {})
    return AgentConfig(
        roles={
            "manager": str(roles.get("manager", "manager")),
            "worker": str(roles.get("worker", "worker")),
            "reviewer": str(roles.get("reviewer", "reviewer")),
        },
        budgets={
            "max_steps": int(budgets.get("max_steps", 8)),
            "max_actions": int(budgets.get("max_actions", 4)),
            "token_budget": int(budgets.get("token_budget", 0) or 0),
        },
        provider={
            "type": str(provider.get("type", "none")),
            "endpoint": str(provider.get("endpoint", "")),
            "model": str(provider.get("model", "")),
        },
        safety={
            "write_allowlist": tuple(str(x) for x in (safety.get("write_allowlist") or [])),
            "shell_allowlist": tuple(str(x) for x in (safety.get("shell_allowlist") or [])),
        },
    )


def init_agent(root: Path, config_path: Path) -> list[str]:
    created: list[str] = []
    agent_root = root / ".sdetkit" / "agent"
    for rel in ["", "history", "workdir"]:
        path = agent_root / rel
        path.mkdir(parents=True, exist_ok=True)
        created.append(path.relative_to(root).as_posix())
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(DEFAULT_CONFIG, encoding="utf-8")
        created.append(config_path.relative_to(root).as_posix())
    return created


def _provider_for(config: AgentConfig, *, fake: bool = False) -> Provider:
    if fake:
        return FakeProvider()
    if config.provider.get("type") == "local":
        return LocalHTTPProvider(
            endpoint=config.provider.get("endpoint", ""),
            model=config.provider.get("model", ""),
        )
    return NoneProvider()


def run_agent(
    root: Path, *, config_path: Path, task: str, force_fake_provider: bool = False
) -> dict[str, Any]:
    config = load_config(config_path)
    provider = _provider_for(config, fake=force_fake_provider)
    registry = ActionRegistry(
        root=root,
        write_allowlist=config.safety.get("write_allowlist", tuple()),
        shell_allowlist=config.safety.get("shell_allowlist", tuple()),
    )
    steps: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    outputs: list[dict[str, Any]] = []

    manager_note = provider.complete(role="manager", task=task, context={"budgets": config.budgets})
    steps.append({"role": "manager", "message": manager_note})

    parsed = maybe_parse_action_task(task)
    if parsed is not None and len(actions) < config.budgets["max_actions"]:
        name, params = parsed
        result = registry.run(name, params)
        actions.append(result.to_dict())

    reviewer_note = provider.complete(
        role="reviewer",
        task=task,
        context={"action_count": len(actions), "max_actions": config.budgets["max_actions"]},
    )
    steps.append({"role": "reviewer", "message": reviewer_note})

    for action in actions:
        outputs.append({"kind": "action", "value": action})
    outputs.append({"kind": "summary", "value": f"completed task: {task}"})

    base_record: dict[str, Any] = {
        "captured_at": _captured_at(),
        "task": task,
        "steps": steps,
        "actions": actions,
        "outputs": outputs,
        "status": "ok" if all(item.get("ok") for item in actions or [{"ok": True}]) else "error",
    }
    digest = _sha(base_record)
    base_record["hash"] = digest
    history_path = root / ".sdetkit" / "agent" / "history" / f"{digest}.json"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(canonical_json_dumps(base_record), encoding="utf-8")
    return base_record


def doctor_agent(root: Path, *, config_path: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    if not config_path.exists():
        checks.append({"name": "config", "ok": False, "detail": "config.yaml missing"})
        return {"ok": False, "checks": checks}
    cfg = load_config(config_path)
    checks.append({"name": "config", "ok": True, "detail": str(config_path.relative_to(root))})

    provider_type = cfg.provider.get("type", "none")
    provider_ok = provider_type in {"none", "local"}
    checks.append({"name": "provider", "ok": provider_ok, "detail": provider_type})

    abs_allowlist = [
        item for item in cfg.safety.get("write_allowlist", tuple()) if Path(item).is_absolute()
    ]
    checks.append(
        {
            "name": "write_allowlist",
            "ok": not abs_allowlist,
            "detail": "relative only"
            if not abs_allowlist
            else f"absolute entries: {abs_allowlist}",
        }
    )

    budgets = cfg.budgets
    budget_ok = budgets.get("max_steps", 0) > 0 and budgets.get("max_actions", 0) >= 0
    checks.append(
        {
            "name": "budgets",
            "ok": budget_ok,
            "detail": json.dumps(budgets, ensure_ascii=True, sort_keys=True),
        }
    )

    return {"ok": all(bool(item["ok"]) for item in checks), "checks": checks}


def history_agent(root: Path, *, limit: int = 10) -> list[dict[str, Any]]:
    history_dir = root / ".sdetkit" / "agent" / "history"
    if not history_dir.exists():
        return []
    rows: list[dict[str, Any]] = []
    for file in sorted(history_dir.glob("*.json"), reverse=True):
        try:
            item = json.loads(file.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(item, dict):
            rows.append(
                {
                    "hash": str(item.get("hash", file.stem)),
                    "captured_at": str(item.get("captured_at", "")),
                    "status": str(item.get("status", "")),
                    "task": str(item.get("task", "")),
                }
            )
    rows.sort(key=lambda x: (x["captured_at"], x["hash"]), reverse=True)
    return rows[: max(limit, 0)]
