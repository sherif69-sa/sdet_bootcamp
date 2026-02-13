from __future__ import annotations

import json
import os
import subprocess
import sys
from types import SimpleNamespace

from sdetkit.maintenance.checks import deps_check
from sdetkit.maintenance.types import MaintenanceContext


def _ctx(tmp_path, env: dict[str, str]) -> MaintenanceContext:
    return MaintenanceContext(
        repo_root=tmp_path,
        python_exe=sys.executable,
        mode="quick",
        fix=False,
        env=env,
        logger=SimpleNamespace(info=lambda *_: None),
    )


def test_deps_check_skips_outdated_by_default(monkeypatch, tmp_path):
    calls: list[list[str]] = []

    def fake_run_cmd(cmd: list[str], *, cwd):
        calls.append(list(cmd))
        if cmd[-1] == "check":
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        raise AssertionError(f"unexpected command: {cmd!r}")

    monkeypatch.setattr(deps_check, "run_cmd", fake_run_cmd)

    result = deps_check.run(_ctx(tmp_path, env={}))
    assert result.ok is True
    assert any(cmd[-1] == "check" for cmd in calls)
    assert not any("--outdated" in cmd for cmd in calls)
    assert result.details["pip_outdated"]["skipped"] is True


def test_deps_check_runs_outdated_when_allowed(monkeypatch, tmp_path):
    calls: list[list[str]] = []

    def fake_run_cmd(cmd: list[str], *, cwd):
        calls.append(list(cmd))
        if cmd[-1] == "check":
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        if "--outdated" in cmd:
            return SimpleNamespace(returncode=0, stdout="pkg 1.0 2.0\n", stderr="")
        raise AssertionError(f"unexpected command: {cmd!r}")

    monkeypatch.setattr(deps_check, "run_cmd", fake_run_cmd)

    result = deps_check.run(_ctx(tmp_path, env={"SDETKIT_ALLOW_NETWORK": "1"}))
    assert result.ok is True
    assert any("--outdated" in cmd for cmd in calls)
    assert result.details["pip_outdated"]["skipped"] is False


def test_maintenance_generated_at_can_be_forced(tmp_path):
    import sys
    from datetime import datetime

    out = tmp_path / "report.json"
    env = os.environ.copy()
    env["SDETKIT_NOW"] = "2000-01-02T03:04:05Z"

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "sdetkit.maintenance",
            "--format",
            "json",
            "--mode",
            "quick",
            "--out",
            str(out),
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode in {0, 1}
    assert out.exists()

    payload = json.loads(out.read_text(encoding="utf-8"))
    got = payload["meta"]["generated_at"]

    def _parse(s: str) -> datetime:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        return datetime.fromisoformat(s)

    assert _parse(got) == _parse("2000-01-02T03:04:05+00:00")
