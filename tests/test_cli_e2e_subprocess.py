from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def test_repo_audit_json_and_sarif_outputs_are_stable(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# x\n", encoding="utf-8")

    out1 = tmp_path / "audit1.json"
    out2 = tmp_path / "audit2.json"
    sarif1 = tmp_path / "audit1.sarif"
    sarif2 = tmp_path / "audit2.sarif"

    cmd = [
        "-m",
        "sdetkit.cli",
        "repo",
        "audit",
        str(tmp_path),
        "--allow-absolute-path",
        "--fail-on",
        "none",
        "--format",
        "json",
        "--output",
    ]
    p1 = _run(cmd + [str(out1)], cwd=Path.cwd())
    p2 = _run(cmd + [str(out2)], cwd=Path.cwd())
    assert p1.returncode == 0, p1.stderr
    assert p2.returncode == 0, p2.stderr

    j1 = json.loads(out1.read_text(encoding="utf-8"))
    j2 = json.loads(out2.read_text(encoding="utf-8"))
    j1.get("metadata", {}).pop("generated_at_utc", None)
    j2.get("metadata", {}).pop("generated_at_utc", None)
    assert j1 == j2

    s_cmd = [
        "-m",
        "sdetkit.cli",
        "repo",
        "audit",
        str(tmp_path),
        "--allow-absolute-path",
        "--fail-on",
        "none",
        "--format",
        "sarif",
        "--output",
    ]
    s1 = _run(s_cmd + [str(sarif1)], cwd=Path.cwd())
    s2 = _run(s_cmd + [str(sarif2)], cwd=Path.cwd())
    assert s1.returncode == 0, s1.stderr
    assert s2.returncode == 0, s2.stderr

    sarif_a = json.loads(sarif1.read_text(encoding="utf-8"))
    sarif_b = json.loads(sarif2.read_text(encoding="utf-8"))
    assert sarif_a == sarif_b
    assert sarif_a["version"] == "2.1.0"


def test_doctor_json_subprocess_exit_code_and_output(tmp_path: Path) -> None:
    proc = _run(["-m", "sdetkit.doctor", "--json"], cwd=Path.cwd())
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert "checks" in payload
