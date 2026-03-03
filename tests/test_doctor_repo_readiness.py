from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _run_doctor(repo_root: Path, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    return subprocess.run(
        [sys.executable, "-m", "sdetkit.doctor", *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_doctor_accepts_format_markdown_alias(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    proc = _run_doctor(repo_root, tmp_path, "--format", "markdown", "--ci")
    assert proc.returncode == 2
    assert proc.stdout.startswith("### SDET Doctor Report")


def test_doctor_repo_readiness_missing_scripts_fails(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    proc = _run_doctor(repo_root, tmp_path, "--repo", "--format", "json")
    assert proc.returncode == 2, proc.stderr
    data = json.loads(proc.stdout)
    checks = data.get("checks") or {}
    rr = checks.get("repo_readiness") or {}
    assert rr.get("ok") is False
    ev = rr.get("evidence") or []
    assert any("bootstrap.sh" in (item.get("path") or "") for item in ev)


def test_doctor_repo_readiness_passes_with_minimal_files(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    (tmp_path / "scripts").mkdir()
    (tmp_path / "templates" / "ci" / "gitlab").mkdir(parents=True)
    (tmp_path / "templates" / "ci" / "jenkins").mkdir(parents=True)
    (tmp_path / "templates" / "ci" / "tekton").mkdir(parents=True)

    (tmp_path / "scripts" / "bootstrap.sh").write_text(
        "#!/usr/bin/env bash\necho ok\n", encoding="utf-8"
    )
    (tmp_path / "ci.sh").write_text("#!/usr/bin/env bash\necho ok\n", encoding="utf-8")
    (tmp_path / "quality.sh").write_text("#!/usr/bin/env bash\necho ok\n", encoding="utf-8")
    (tmp_path / "security.sh").write_text("#!/usr/bin/env bash\necho ok\n", encoding="utf-8")

    (tmp_path / "templates" / "ci" / "gitlab" / "gitlab-advanced-reference.yml").write_text(
        "x: 1\n", encoding="utf-8"
    )
    (
        tmp_path / "templates" / "ci" / "jenkins" / "jenkins-advanced-reference.Jenkinsfile"
    ).write_text("x\n", encoding="utf-8")
    (tmp_path / "templates" / "ci" / "tekton" / "tekton-self-hosted-reference.yaml").write_text(
        "x: 1\n", encoding="utf-8"
    )

    (tmp_path / "scripts" / "check_repo_layout.py").write_text(
        "import sys\n"
        "from pathlib import Path\n"
        "bad=[]\n"
        "req=[\n"
        "  'templates/ci/gitlab/gitlab-advanced-reference.yml',\n"
        "  'templates/ci/jenkins/jenkins-advanced-reference.Jenkinsfile',\n"
        "  'templates/ci/tekton/tekton-self-hosted-reference.yaml',\n"
        "]\n"
        "bad.extend([f'missing: {p}' for p in req if not Path(p).exists()])\n"
        "if bad:\n"
        "  sys.stderr.write('Repo layout invariant violations:\\n'+'\\n'.join(bad)+'\\n')\n"
        "  raise SystemExit(1)\n"
        "print('ok: repo layout invariants hold')\n",
        encoding="utf-8",
    )

    (tmp_path / ".pre-commit-config.yaml").write_text(
        "repos:\n"
        "  - repo: https://github.com/astral-sh/ruff-pre-commit\n"
        "    rev: v0.15.0\n"
        "    hooks:\n"
        "      - id: ruff\n"
        "      - id: ruff-format\n"
        "  - repo: https://github.com/pre-commit/mirrors-mypy\n"
        "    rev: v1.19.1\n"
        "    hooks:\n"
        "      - id: mypy\n",
        encoding="utf-8",
    )

    proc = _run_doctor(repo_root, tmp_path, "--repo", "--format", "json")
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    checks = data.get("checks") or {}
    rr = checks.get("repo_readiness") or {}
    assert rr.get("ok") is True
