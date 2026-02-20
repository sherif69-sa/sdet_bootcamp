import json

from sdetkit import cli, quality_contribution_delta


def _write_signals(tmp_path, current: str, previous: str):
    current_path = tmp_path / "current.json"
    previous_path = tmp_path / "previous.json"
    current_path.write_text(current, encoding="utf-8")
    previous_path.write_text(previous, encoding="utf-8")
    return current_path, previous_path


def test_day17_delta_default_json(tmp_path, capsys):
    current, previous = _write_signals(
        tmp_path,
        '{"traffic": 2200, "stars": 112, "discussions": 31, "blocker_fixes": 9}\n',
        '{"traffic": 1800, "stars": 90, "discussions": 24, "blocker_fixes": 7}\n',
    )

    rc = quality_contribution_delta.main(
        [
            "--root",
            ".",
            "--current-signals-file",
            str(current),
            "--previous-signals-file",
            str(previous),
            "--format",
            "json",
        ]
    )
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert data["name"] == "day17-quality-contribution-delta"
    assert data["contributions"]["deltas"]["traffic"] == 400
    assert data["contributions"]["delta_percent"]["traffic"] == 22.22
    assert "velocity_score" in data["contributions"]
    assert "stability_score" in data["quality"]


def test_day17_emit_pack(tmp_path, capsys):
    current, previous = _write_signals(
        tmp_path,
        '{"traffic": 2200, "stars": 112, "discussions": 31, "blocker_fixes": 9}\n',
        '{"traffic": 1800, "stars": 90, "discussions": 24, "blocker_fixes": 7}\n',
    )

    rc = quality_contribution_delta.main(
        [
            "--root",
            str(tmp_path),
            "--current-signals-file",
            str(current),
            "--previous-signals-file",
            str(previous),
            "--emit-pack-dir",
            "docs/artifacts/day17-delta-pack",
            "--format",
            "json",
        ]
    )
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert len(data["pack_files"]) == 4


def test_day17_strict_fails_on_negative_delta(tmp_path, capsys):
    current, previous = _write_signals(
        tmp_path,
        '{"traffic": 1750, "stars": 89, "discussions": 20, "blocker_fixes": 6}\n',
        '{"traffic": 1800, "stars": 90, "discussions": 24, "blocker_fixes": 7}\n',
    )

    rc = quality_contribution_delta.main(
        [
            "--root",
            ".",
            "--current-signals-file",
            str(current),
            "--previous-signals-file",
            str(previous),
            "--format",
            "json",
            "--strict",
        ]
    )
    assert rc == 1
    data = json.loads(capsys.readouterr().out)
    assert len(data["strict_failures"]) >= 1


def test_day17_cli_dispatch(tmp_path, capsys):
    current, previous = _write_signals(
        tmp_path,
        '{"traffic": 2200, "stars": 112, "discussions": 31, "blocker_fixes": 9}\n',
        '{"traffic": 1800, "stars": 90, "discussions": 24, "blocker_fixes": 7}\n',
    )

    rc = cli.main(
        [
            "quality-contribution-delta",
            "--root",
            ".",
            "--current-signals-file",
            str(current),
            "--previous-signals-file",
            str(previous),
            "--format",
            "text",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "Day 17 quality + contribution delta pack" in out
    assert "Recommendations:" in out
