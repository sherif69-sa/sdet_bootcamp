from __future__ import annotations

import argparse
import json as std_json
from pathlib import Path

import pytest

from sdetkit import gate


def _ok_run(cmd: list[str], cwd: Path) -> dict[str, object]:
    return {
        "cmd": cmd,
        "rc": 0,
        "ok": True,
        "duration_ms": 1,
        "stdout": "",
        "stderr": "",
    }


def test_run_fast_text_mode_and_strict_doctor(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    seen: list[list[str]] = []

    def fake_run(cmd: list[str], cwd: Path) -> dict[str, object]:
        seen.append(cmd)
        return _ok_run(cmd, cwd)

    monkeypatch.setattr(gate, "_run", fake_run)

    rc = gate.main(["fast", "--only", "doctor", "--strict", "--format", "text"])

    assert rc == 0
    out = capsys.readouterr().out
    assert "gate fast: OK" in out
    doctor_cmd = seen[0]
    assert "--fail-on" in doctor_cmd
    assert "medium" in doctor_cmd


def test_playbooks_validate_args_aliases_branch() -> None:
    ns = argparse.Namespace(
        playbooks_all=False,
        playbooks_legacy=False,
        playbooks_aliases=True,
        playbook_name=[],
    )
    assert gate._playbooks_validate_args(ns) == ["--aliases", "--format", "json"]


def test_baseline_write_uses_relative_path_under_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(gate, "_run", _ok_run)

    rc = gate.main(
        [
            "baseline",
            "write",
            "--path",
            "snapshots/gate.json",
            "--",
            "--only",
            "ruff",
            "--no-doctor",
            "--no-ci-templates",
            "--no-mypy",
            "--no-pytest",
        ]
    )

    assert rc == 0
    out_path = tmp_path / "snapshots" / "gate.json"
    assert out_path.exists()
    payload = std_json.loads(out_path.read_text(encoding="utf-8"))
    assert payload["root"] == "<repo>"


def test_baseline_returns_fast_failure_code(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    def failing_run(cmd: list[str], cwd: Path) -> dict[str, object]:
        result = _ok_run(cmd, cwd)
        result["ok"] = False
        result["rc"] = 1
        return result

    monkeypatch.setattr(gate, "_run", failing_run)

    rc = gate.main(
        [
            "baseline",
            "write",
            "--",
            "--only",
            "ruff",
            "--no-doctor",
            "--no-ci-templates",
            "--no-mypy",
            "--no-pytest",
        ]
    )

    assert rc == 2


def test_baseline_check_diff_handles_non_json_snapshot_and_current(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)
    snap = tmp_path / "bad.snapshot.txt"
    snap.write_text("bad-snapshot", encoding="utf-8")

    def fake_release(ns: argparse.Namespace) -> int:
        # Intentionally non-JSON output to exercise tolerant parsing in baseline check.
        gate._write_output("bad-current", getattr(ns, "out", None))
        return 0

    monkeypatch.setattr(gate, "_run_release", fake_release)

    rc = gate.main(
        [
            "baseline",
            "check",
            "--profile",
            "release",
            "--path",
            str(snap),
            "--diff",
        ]
    )

    assert rc == 2
    out = capsys.readouterr().out
    assert out == "bad-current"


def test_baseline_parsing_tolerates_non_json_then_enriches_payload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(gate, "_run", _ok_run)

    original_loads = gate.json.loads
    calls = {"n": 0}

    def flaky_loads(text: str, *args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("synthetic parse failure")
        return original_loads(text, *args, **kwargs)

    monkeypatch.setattr(gate.json, "loads", flaky_loads)

    rc = gate.main(
        [
            "baseline",
            "check",
            "--",
            "--only",
            "ruff",
            "--no-doctor",
            "--no-ci-templates",
            "--no-mypy",
            "--no-pytest",
        ]
    )

    assert rc == 2
    payload = std_json.loads(capsys.readouterr().out)
    assert payload["snapshot_diff_ok"] is False
    assert "snapshot drift detected" in payload["snapshot_diff_summary"]


def test_main_unknown_command_branch(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fake_parse_args(
        self: argparse.ArgumentParser, args: list[str] | None = None
    ) -> argparse.Namespace:
        return argparse.Namespace(cmd="mystery")

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", fake_parse_args)

    rc = gate.main(["fast"])

    assert rc == 2
    assert "unknown gate command" in capsys.readouterr().err
