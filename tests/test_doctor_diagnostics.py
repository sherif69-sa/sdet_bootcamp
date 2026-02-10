from __future__ import annotations

import json
from pathlib import Path

from sdetkit import doctor


def test_doctor_ci_missing_files(tmp_path: Path, monkeypatch, capsys):
    root = tmp_path / "repo"
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")

    def fake_run(cmd, *, cwd=None):
        return 0, "", ""

    monkeypatch.setattr(doctor, "_run", fake_run)
    monkeypatch.chdir(root)

    rc = doctor.main(["--ci", "--json"])
    data = json.loads(capsys.readouterr().out)

    assert rc == 1
    assert ".github/workflows/quality.yml" in data["ci_missing"]
    assert ".github/workflows/security.yml" in data["ci_missing"]


def test_doctor_ci_yaml_invalid_reports_files(tmp_path: Path, monkeypatch, capsys):
    root = tmp_path / "repo"
    wf = root / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "ci.yml").write_text("name: ci\n", encoding="utf-8")
    (wf / "quality.yml").write_text("name: q\n", encoding="utf-8")
    (wf / "security.yml").write_text("name: s\n", encoding="utf-8")

    def fake_run(cmd, *, cwd=None):
        if "pre_commit" in " ".join(cmd) and "check-yaml" in cmd:
            return 1, "Failed\n.github/workflows/ci.yml\n", ""
        return 0, "", ""

    monkeypatch.setattr(doctor, "_run", fake_run)
    monkeypatch.chdir(root)

    rc = doctor.main(["--ci", "--json"])
    data = json.loads(capsys.readouterr().out)

    assert rc == 1
    assert "ci_missing" in data and data["ci_missing"] == []
    assert ".github/workflows/ci.yml" in data["yaml_invalid"]


def test_doctor_pre_commit_and_deps_and_clean_tree(tmp_path: Path, monkeypatch, capsys):
    root = tmp_path / "repo"
    root.mkdir()
    (root / ".pre-commit-config.yaml").write_text("repos: []\n", encoding="utf-8")

    def fake_run(cmd, *, cwd=None):
        s = " ".join(cmd)
        if s.endswith("-m pre_commit --version"):
            return 0, "pre-commit 9.9.9\n", ""
        if "validate-config" in s:
            return 0, "", ""
        if s.endswith("-m pip check"):
            return 0, "", ""
        if s == "git status --porcelain":
            return 0, "", ""
        if "check-yaml" in s:
            return 0, "", ""
        return 0, "", ""

    monkeypatch.setattr(doctor, "_run", fake_run)
    monkeypatch.chdir(root)

    rc = doctor.main(["--pre-commit", "--deps", "--clean-tree", "--json"])
    data = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert data["pre_commit_ok"] is True
    assert data["deps_ok"] is True
    assert data["clean_tree_ok"] is True
