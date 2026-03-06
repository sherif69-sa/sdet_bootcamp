from __future__ import annotations

import json
from pathlib import Path

from sdetkit import gate


def test_format_md_renders_failed_steps_section() -> None:
    rendered = gate._format_md(
        {
            "ok": False,
            "root": "/tmp/repo",
            "steps": [{"id": "ruff", "ok": False, "duration_ms": 12, "rc": 1}],
            "failed_steps": ["ruff"],
        }
    )

    assert "#### Failed steps" in rendered
    assert "- `ruff`" in rendered


def test_run_fast_strict_with_custom_args_and_text_output(
    monkeypatch, capsys, tmp_path: Path
) -> None:
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], cwd: Path) -> dict[str, object]:
        calls.append(cmd)
        return {"cmd": cmd, "rc": 0, "ok": True, "duration_ms": 1, "stdout": "", "stderr": ""}

    monkeypatch.setattr(gate, "_run", fake_run)
    monkeypatch.chdir(tmp_path)

    rc = gate.main(
        [
            "fast",
            "--format",
            "text",
            "--strict",
            "--mypy-args",
            "src tests",
            "--pytest-args",
            "-q tests/test_gate_fast.py",
            "--only",
            "doctor,ci_templates,mypy,pytest",
        ]
    )

    assert rc == 0
    out = capsys.readouterr().out
    assert out.startswith("gate fast: OK")

    doctor_call = calls[0]
    assert doctor_call[3:] == [
        "doctor",
        "--dev",
        "--ci",
        "--deps",
        "--clean-tree",
        "--repo",
        "--fail-on",
        "medium",
        "--format",
        "json",
    ]
    assert calls[1][3:6] == ["ci", "validate-templates", "--root"]
    assert calls[2][3:] == ["src", "tests"]
    assert calls[3][3:] == ["-q", "tests/test_gate_fast.py"]


def test_baseline_check_returns_fast_rc_for_bad_extra_args(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.chdir(tmp_path)
    rc = gate.main(["baseline", "check", "--", "--only", "not-a-step"])

    err = capsys.readouterr().err
    assert rc == 2
    assert "unknown step id" in err


def test_baseline_write_uses_relative_custom_path(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rc = gate.main(
        [
            "baseline",
            "write",
            "--path",
            "snapshots/gate.json",
            "--",
            "--no-doctor",
            "--no-ci-templates",
            "--no-mypy",
            "--no-pytest",
        ]
    )

    assert rc == 0
    custom = tmp_path / "snapshots" / "gate.json"
    assert custom.exists()
    json.loads(custom.read_text(encoding="utf-8"))


def test_release_uses_aliases_selection(monkeypatch, tmp_path: Path, capsys) -> None:
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], cwd: Path) -> dict[str, object]:
        calls.append(cmd)
        return {"cmd": cmd, "rc": 0, "ok": True, "duration_ms": 1, "stdout": "", "stderr": ""}

    monkeypatch.setattr(gate, "_run", fake_run)
    monkeypatch.chdir(tmp_path)

    rc = gate.main(["release", "--format", "json", "--playbooks-aliases"])
    assert rc == 0
    _ = json.loads(capsys.readouterr().out)
    assert calls[1][3:] == ["playbooks", "validate", "--aliases", "--format", "json"]
