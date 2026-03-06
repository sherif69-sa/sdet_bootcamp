from __future__ import annotations

import argparse
import json
from pathlib import Path

from sdetkit import gate


def test_format_md_renders_failed_steps_section() -> None:
def _ns(**kwargs: object) -> argparse.Namespace:
    base: dict[str, object] = {
        "root": ".",
        "only": None,
        "skip": None,
        "list_steps": False,
        "fix": False,
        "fix_only": False,
        "no_doctor": True,
        "no_ci_templates": True,
        "no_ruff": True,
        "no_mypy": True,
        "no_pytest": True,
        "strict": False,
        "format": "json",
        "out": None,
        "mypy_args": None,
        "full_pytest": False,
        "pytest_args": None,
        "dry_run": False,
        "release_full": False,
        "playbooks_all": False,
        "playbooks_legacy": False,
        "playbooks_aliases": False,
        "playbook_name": [],
        "stable_json": False,
    }
    base.update(kwargs)
    return argparse.Namespace(**base)


def test_format_md_includes_failed_steps_section() -> None:
    rendered = gate._format_md(
        {
            "ok": False,
            "root": "/tmp/repo",
            "steps": [{"id": "ruff", "ok": False, "duration_ms": 12, "rc": 1}],
            "steps": [{"id": "ruff", "ok": False, "duration_ms": 2, "rc": 1}],
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
def test_run_fast_strict_uses_medium_and_runs_ci_templates(monkeypatch) -> None:
    seen: list[list[str]] = []

    def fake_run(cmd: list[str], cwd: Path) -> dict[str, object]:
        seen.append(cmd)
        return {"cmd": cmd, "rc": 0, "ok": True, "duration_ms": 1, "stdout": "", "stderr": ""}

    monkeypatch.setattr(gate, "_run", fake_run)

    rc = gate._run_fast(
        _ns(
            strict=True,
            no_doctor=False,
            no_ci_templates=False,
        )
    )

    assert rc == 0
    doctor = next(cmd for cmd in seen if "doctor" in cmd)
    assert "medium" in doctor
    assert any("validate-templates" in " ".join(cmd) for cmd in seen)


def test_run_fast_uses_custom_mypy_and_pytest_args(monkeypatch, capsys) -> None:
    seen: list[list[str]] = []

    def fake_run(cmd: list[str], cwd: Path) -> dict[str, object]:
        seen.append(cmd)
        return {"cmd": cmd, "rc": 0, "ok": True, "duration_ms": 1, "stdout": "", "stderr": ""}

    monkeypatch.setattr(gate, "_run", fake_run)

    rc = gate._run_fast(
        _ns(
            format="text",
            no_mypy=False,
            no_pytest=False,
            mypy_args="src tests",
            pytest_args="-q tests/test_gate_fast.py",
        )
    )

    assert rc == 0
    _ = capsys.readouterr()
    assert ["src", "tests"] == seen[0][3:]
    assert ["-q", "tests/test_gate_fast.py"] == seen[1][3:]


def test_playbooks_validate_args_aliases_mode() -> None:
    ns = _ns(playbooks_aliases=True)
    assert gate._playbooks_validate_args(ns) == ["--aliases", "--format", "json"]


def test_baseline_check_handles_non_json_and_diff(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    snapshot = tmp_path / "relative-snap.json"
    snapshot.write_text("snapshot-version", encoding="utf-8")

    def fake_run_fast(ns: argparse.Namespace) -> int:
        print("current-version", end="")
        return 0

    monkeypatch.setattr(gate, "_run_fast", fake_run_fast)

    rc = gate.main(
        ["baseline", "check", "--path", "relative-snap.json", "--diff", "--", "--no-doctor"]
    )
    out = capsys.readouterr().out

    assert rc == 2
    assert out == "current-version"


def test_baseline_write_with_relative_path_uses_cwd(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)

    def fake_run_fast(ns: argparse.Namespace) -> int:
        payload = {
            "profile": "fast",
            "root": str(tmp_path),
            "ok": True,
            "failed_steps": [],
            "steps": [],
        }
        print(json.dumps(payload, sort_keys=True), end="")
        return 0

    monkeypatch.setattr(gate, "_run_fast", fake_run_fast)

    rc = gate.main(["baseline", "write", "--path", "nested/snapshot.json", "--", "--no-doctor"])

    assert rc == 0
    snap = tmp_path / "nested" / "snapshot.json"
    assert snap.exists()


def test_baseline_bubbles_nonzero_rc_from_profile_run(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)

    def fake_run_fast(ns: argparse.Namespace) -> int:
        print('{"ok":false}', end="")
        return 7

    monkeypatch.setattr(gate, "_run_fast", fake_run_fast)

    rc = gate.main(["baseline", "check", "--", "--no-doctor"])

    assert rc == 7


def test_main_unknown_command_branch(monkeypatch, capsys) -> None:
    def fake_parse_args(
        self: argparse.ArgumentParser, argv: list[str] | None = None
    ) -> argparse.Namespace:
        return argparse.Namespace(cmd="mystery")

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", fake_parse_args)

    rc = gate.main([])
    err = capsys.readouterr().err

    assert rc == 2
    assert "unknown gate command" in err
