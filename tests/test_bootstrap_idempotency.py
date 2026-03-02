from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


def _run(cmd: list[str], cwd: Path) -> str:
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(
            f"command failed: {' '.join(cmd)}\nstdout:\n{p.stdout}\nstderr:\n{p.stderr}"
        )
    return p.stdout


def _ensure_git_clean(root: Path) -> None:
    try:
        _run(["git", "rev-parse", "--is-inside-work-tree"], cwd=root)
    except Exception:
        pytest.skip("requires git worktree")

    status = _run(
        ["git", "status", "--porcelain=v1", "--untracked-files=no"],
        cwd=root,
    ).strip()
    if status:
        pytest.skip("requires clean git worktree (tracked files)")


def _assert_no_tracked_changes(root: Path) -> None:
    diff = _run(["git", "diff", "--name-only"], cwd=root).strip()
    status = _run(
        ["git", "status", "--porcelain=v1", "--untracked-files=no"],
        cwd=root,
    ).strip()
    assert diff == ""
    assert status == ""


def test_bootstrap_is_idempotent_and_toolchain_works() -> None:
    root = Path(__file__).resolve().parents[1]

    _ensure_git_clean(root)

    for _ in range(2):
        _run(["bash", "scripts/bootstrap.sh"], cwd=root)

        vpy = root / ".venv" / "bin" / "python"
        assert vpy.exists()

        _run([str(vpy), "-m", "sdetkit", "--help"], cwd=root)

        _assert_no_tracked_changes(root)
