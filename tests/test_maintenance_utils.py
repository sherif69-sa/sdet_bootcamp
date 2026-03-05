from __future__ import annotations

from pathlib import Path

from sdetkit.maintenance.utils import run_cmd


def test_run_cmd_returns_completed_process(tmp_path: Path) -> None:
    proc = run_cmd(["python", "-c", "print('ok')"], cwd=tmp_path)
    assert proc.returncode == 0
    assert proc.stdout.strip() == "ok"
    assert proc.stderr == ""
