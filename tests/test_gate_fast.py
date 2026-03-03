from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _run_sdetkit(repo_root: Path, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    return subprocess.run(
        [sys.executable, "-m", "sdetkit", *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_gate_help_includes_fast() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    proc = _run_sdetkit(repo_root, repo_root, "gate", "--help")
    assert proc.returncode == 0
    assert "usage: gate" in proc.stdout
    assert "fast" in proc.stdout


def test_gate_fast_can_run_ci_templates_only(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    (tmp_path / "templates" / "ci" / "gitlab").mkdir(parents=True)
    (tmp_path / "templates" / "ci" / "jenkins").mkdir(parents=True)
    (tmp_path / "templates" / "ci" / "tekton").mkdir(parents=True)

    (tmp_path / "templates" / "ci" / "gitlab" / "day66-advanced-reference.yml").write_text(
        "bash scripts/bootstrap.sh\n. .venv/bin/activate\npython -m sdetkit\nCI_COMMIT_REF_SLUG\n",
        encoding="utf-8",
    )
    (tmp_path / "templates" / "ci" / "jenkins" / "day67-advanced-reference.Jenkinsfile").write_text(
        "bash scripts/bootstrap.sh\n. .venv/bin/activate\npytest -q\nsecurity.sh\nPYTHON_VERSION\n",
        encoding="utf-8",
    )
    (tmp_path / "templates" / "ci" / "tekton" / "day68-self-hosted-reference.yaml").write_text(
        "bash scripts/bootstrap.sh\n. .venv/bin/activate\nbash ci.sh\nbash security.sh\n$(params.branch)\n",
        encoding="utf-8",
    )

    proc = _run_sdetkit(
        repo_root,
        tmp_path,
        "gate",
        "fast",
        "--root",
        str(tmp_path),
        "--format",
        "json",
        "--no-doctor",
        "--no-ruff",
        "--no-mypy",
        "--no-pytest",
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["ok"] is True
    assert [s["id"] for s in data["steps"]] == ["ci_templates"]
