from __future__ import annotations

import json
from pathlib import Path

from sdetkit.agent.actions import ActionRegistry
from sdetkit.agent.core import canonical_json_dumps, init_agent, run_agent


def test_agent_init_creates_expected_files(tmp_path: Path) -> None:
    created = init_agent(tmp_path, tmp_path / ".sdetkit/agent/config.yaml")

    assert ".sdetkit/agent" in created
    assert ".sdetkit/agent/history" in created
    assert ".sdetkit/agent/workdir" in created
    assert (tmp_path / ".sdetkit/agent/config.yaml").exists()


def test_agent_run_deterministic_mode_stable_output(tmp_path: Path, monkeypatch) -> None:
    init_agent(tmp_path, tmp_path / ".sdetkit/agent/config.yaml")
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1700000000")
    monkeypatch.chdir(tmp_path)

    first = run_agent(
        tmp_path, config_path=tmp_path / ".sdetkit/agent/config.yaml", task="health-check"
    )
    second = run_agent(
        tmp_path,
        config_path=tmp_path / ".sdetkit/agent/config.yaml",
        task="health-check",
    )

    assert first["hash"] == second["hash"]
    assert first["status"] == "ok"


def test_agent_run_records_are_canonical(tmp_path: Path, monkeypatch) -> None:
    init_agent(tmp_path, tmp_path / ".sdetkit/agent/config.yaml")
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1700000000")
    monkeypatch.chdir(tmp_path)

    record = run_agent(
        tmp_path, config_path=tmp_path / ".sdetkit/agent/config.yaml", task="health-check"
    )
    history_file = tmp_path / ".sdetkit/agent/history" / f"{record['hash']}.json"
    assert history_file.exists()

    on_disk = history_file.read_text(encoding="utf-8")
    loaded = json.loads(on_disk)
    assert loaded["hash"] == record["hash"]
    assert on_disk == canonical_json_dumps(loaded)


def test_unsafe_absolute_write_is_blocked(tmp_path: Path) -> None:
    registry = ActionRegistry(
        root=tmp_path,
        write_allowlist=(".sdetkit/agent/workdir",),
        shell_allowlist=(),
    )

    result = registry.run("fs.write", {"path": "/tmp/not-allowed.txt", "content": "x"})

    assert result.ok is False
    assert "allowlist" in result.payload["error"]
