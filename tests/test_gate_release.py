from __future__ import annotations

import json
from pathlib import Path

from sdetkit import gate


def test_gate_release_dry_run_lists_steps(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    rc = gate.main(["release", "--dry-run", "--format", "json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["dry_run"] is True
    assert [step["id"] for step in payload["steps"]] == [
        "doctor_release",
        "playbooks_validate",
        "gate_fast",
    ]


def test_gate_release_runs_expected_commands(monkeypatch, tmp_path: Path, capsys) -> None:
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], cwd: Path) -> dict[str, object]:
        calls.append(cmd)
        return {"cmd": cmd, "rc": 0, "ok": True, "duration_ms": 1, "stdout": "", "stderr": ""}

    monkeypatch.setattr(gate, "_run", fake_run)
    monkeypatch.chdir(tmp_path)

    rc = gate.main(["release", "--format", "json", "--release-full"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert [step["id"] for step in payload["steps"]] == [
        "doctor_release",
        "playbooks_validate",
        "gate_fast",
    ]
    assert calls[0][3:] == ["doctor", "--release-full", "--format", "json"]
    assert calls[1][3:] == ["playbooks", "validate", "--recommended", "--format", "json"]
    assert calls[2][3:6] == ["gate", "fast", "--root"]
