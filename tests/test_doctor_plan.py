from __future__ import annotations

import json
from pathlib import Path

from sdetkit import doctor


def test_doctor_plan_is_deterministic(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    rc1 = doctor.main(["--plan", "--format", "json"])
    data1 = json.loads(capsys.readouterr().out)
    assert rc1 == 0
    plan1 = data1["plan"]

    rc2 = doctor.main(["--plan", "--format", "json"])
    data2 = json.loads(capsys.readouterr().out)
    assert rc2 == 0
    plan2 = data2["plan"]

    assert plan1["plan_id"] == plan2["plan_id"]
    assert [a["id"] for a in plan1["actions"]] == ["ruff_fix", "ruff_format_apply"]


def test_doctor_apply_plan_rejects_mismatch(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    rc = doctor.main(["--plan", "--format", "json"])
    plan = json.loads(capsys.readouterr().out)["plan"]
    assert rc == 0

    rc2 = doctor.main(["--apply-plan", "deadbeefdead", "--format", "json"])
    data2 = json.loads(capsys.readouterr().out)
    assert rc2 == 2
    assert data2["error"]["code"] == "plan_id_mismatch"
    assert data2["expected"] == plan["plan_id"]


def test_doctor_apply_plan_runs_actions(tmp_path: Path, monkeypatch, capsys) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname="x"\nversion="1.2.3"\n', encoding="utf-8"
    )
    monkeypatch.chdir(tmp_path)

    calls: list[list[str]] = []

    def fake_run(cmd, *, cwd=None):
        calls.append(list(cmd))
        if cmd == ["git", "status", "--porcelain"]:
            return 0, "", ""
        return 0, "", ""

    monkeypatch.setattr(doctor, "_run", fake_run)

    rc = doctor.main(["--plan", "--format", "json"])
    plan = json.loads(capsys.readouterr().out)["plan"]
    assert rc == 0

    rc2 = doctor.main(["--apply-plan", plan["plan_id"], "--only", "pyproject", "--format", "json"])
    data2 = json.loads(capsys.readouterr().out)
    assert rc2 == 0
    assert data2["plan"]["plan_id"] == plan["plan_id"]
    assert [s["id"] for s in data2["plan_steps"]] == ["ruff_fix", "ruff_format_apply"]
    assert any(c[:3] == [doctor.sys.executable, "-m", "ruff"] for c in calls)
