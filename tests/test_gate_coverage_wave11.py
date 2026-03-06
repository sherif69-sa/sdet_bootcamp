from __future__ import annotations

import argparse
import json
from pathlib import Path

from sdetkit import gate


def _ns(**kwargs):
    base = dict(
        root=".",
        only=None,
        skip=None,
        list_steps=False,
        fix=False,
        fix_only=False,
        no_doctor=False,
        no_ci_templates=False,
        no_ruff=False,
        no_mypy=False,
        no_pytest=False,
        strict=False,
        format="text",
        out=None,
        mypy_args=None,
        full_pytest=False,
        pytest_args=None,
        stable_json=False,
    )
    base.update(kwargs)
    return argparse.Namespace(**base)


def test_format_md_includes_failed_steps_section() -> None:
    rendered = gate._format_md(
        {
            "ok": False,
            "root": "/tmp/repo",
            "steps": [],
            "failed_steps": ["ruff", "pytest"],
        }
    )
    assert "#### Failed steps" in rendered
    assert "- `ruff`" in rendered
    assert "- `pytest`" in rendered


def test_run_fast_uses_strict_fail_on_and_extra_args(monkeypatch, capsys) -> None:
    commands: list[list[str]] = []

    def fake_run(cmd, cwd):
        commands.append(cmd)
        return {
            "cmd": cmd,
            "rc": 0,
            "ok": True,
            "duration_ms": 1,
            "stdout": "",
            "stderr": "",
        }

    monkeypatch.setattr(gate, "_run", fake_run)
    rc = gate._run_fast(
        _ns(
            strict=True,
            format="text",
            mypy_args="src tests",
            pytest_args="-q tests/test_gate_fast.py",
        )
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "gate fast: OK" in out

    doctor_cmd = next(cmd for cmd in commands if "doctor" in cmd)
    assert "--fail-on" in doctor_cmd
    assert doctor_cmd[doctor_cmd.index("--fail-on") + 1] == "medium"

    ci_cmd = next(cmd for cmd in commands if "validate-templates" in cmd)
    assert "--strict" in ci_cmd

    mypy_cmd = next(cmd for cmd in commands if "-m" in cmd and "mypy" in cmd)
    assert mypy_cmd[-2:] == ["src", "tests"]

    pytest_cmd = next(cmd for cmd in commands if "-m" in cmd and "pytest" in cmd)
    assert pytest_cmd[-2:] == ["-q", "tests/test_gate_fast.py"]


def test_playbooks_validate_aliases_branch() -> None:
    ns = argparse.Namespace(playbooks_all=False, playbooks_legacy=False, playbooks_aliases=True)
    assert gate._playbooks_validate_args(ns) == ["--aliases", "--format", "json"]


def test_baseline_relative_path_and_non_json_diff_payload(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.chdir(tmp_path)

    def fake_run_fast(ns):
        print("not-json-current", end="")
        return 0

    monkeypatch.setattr(gate, "_run_fast", fake_run_fast)

    snap = tmp_path / "snapshots" / "gate.fast.snapshot.json"
    snap.parent.mkdir(parents=True, exist_ok=True)
    snap.write_text("not-json-snapshot", encoding="utf-8")

    rc = gate.main(["baseline", "check", "--path", str(Path("snapshots") / snap.name), "--diff"])
    out = capsys.readouterr().out

    assert rc == 2
    # non-JSON current output exercises fallback behavior and is emitted as-is.
    assert out == "not-json-current"


def test_baseline_diff_with_invalid_snapshot_json(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    def fake_run_fast(ns):
        print('{"ok": false, "steps": []}', end="")
        return 0

    monkeypatch.setattr(gate, "_run_fast", fake_run_fast)

    snap = tmp_path / "gate.fast.snapshot.json"
    snap.write_text("not-json-snapshot", encoding="utf-8")

    rc = gate.main(["baseline", "check", "--path", str(snap), "--diff"])
    data = json.loads(capsys.readouterr().out)

    assert rc == 2
    assert data["snapshot_diff_ok"] is False
    assert "snapshot drift detected" in data["snapshot_diff_summary"]
    assert data["snapshot_diff"].startswith("--- snapshot\n+++ current\n")


def test_baseline_returns_nested_fast_rc(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(gate, "_run_fast", lambda ns: 2)

    rc = gate.main(["baseline", "check"])
    assert rc == 2


def test_main_unknown_command_branch(monkeypatch, capsys) -> None:
    original_parse_args = argparse.ArgumentParser.parse_args

    def fake_parse_args(self, args=None, namespace=None):
        return argparse.Namespace(cmd="unexpected")

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", fake_parse_args)
    try:
        rc = gate.main([])
    finally:
        monkeypatch.setattr(argparse.ArgumentParser, "parse_args", original_parse_args)

    assert rc == 2
    assert "unknown gate command" in capsys.readouterr().err
