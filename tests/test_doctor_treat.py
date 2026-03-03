from __future__ import annotations

import json
from pathlib import Path

from sdetkit import doctor


def test_doctor_treat_only_emits_treatments(tmp_path: Path, monkeypatch, capsys) -> None:
    (tmp_path / "a.py").write_text("x=1\n", encoding="utf-8")

    calls: list[list[str]] = []

    def fake_run(cmd, *, cwd=None):
        calls.append(list(cmd))
        return 0, "", ""

    monkeypatch.setattr(doctor, "_run", fake_run)
    monkeypatch.chdir(tmp_path)

    rc = doctor.main(["--treat-only", "--format", "json"])
    data = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert [s["id"] for s in data["treatments"]] == ["ruff_fix", "ruff_format_apply"]
    assert data["treatments_ok"] is True
    assert data["post_treat_ok"] is True
    assert calls


def test_doctor_treat_includes_treatments_in_full_payload(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname="x"\nversion="1.2.3"\n', encoding="utf-8"
    )
    (tmp_path / "a.py").write_text("x=1\n", encoding="utf-8")

    def fake_run(cmd, *, cwd=None):
        if cmd == ["git", "status", "--porcelain"]:
            return 0, "", ""
        return 0, "", ""

    monkeypatch.setattr(doctor, "_run", fake_run)
    monkeypatch.chdir(tmp_path)

    rc = doctor.main(["--treat", "--only", "pyproject", "--format", "json"])
    data = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert [s["id"] for s in data["treatments"]] == ["ruff_fix", "ruff_format_apply"]
    assert data["checks"]["pyproject"]["ok"] is True
