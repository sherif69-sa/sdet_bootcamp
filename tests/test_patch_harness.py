from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path


def _load_patch_harness():
    root = Path(__file__).resolve().parents[1]
    path = root / "tools" / "patch_harness.py"
    spec = importlib.util.spec_from_file_location("patch_harness", path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(ph, argv: list[str], cwd: Path) -> int:
    old = Path.cwd()
    os.chdir(cwd)
    try:
        return int(ph.main(argv))
    finally:
        os.chdir(old)


def test_check_does_not_write_and_returns_1(tmp_path, capsys):
    ph = _load_patch_harness()

    (tmp_path / "a.txt").write_text("MARK\n", encoding="utf-8")
    spec = {
        "files": [
            {
                "path": "a.txt",
                "ops": [
                    {"op": "insert_after", "pattern": r"^MARK$", "text": "X\n"},
                ],
            }
        ]
    }
    (tmp_path / "spec.json").write_text(json.dumps(spec), encoding="utf-8")

    rc = _run(ph, ["spec.json", "--check"], tmp_path)
    out = capsys.readouterr().out
    assert rc == 1
    assert "+X\n" in out
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "MARK\n"


def test_dry_run_prints_diff_and_does_not_write(tmp_path, capsys):
    ph = _load_patch_harness()

    (tmp_path / "a.txt").write_text("MARK\n", encoding="utf-8")
    spec = {
        "files": [
            {
                "path": "a.txt",
                "ops": [
                    {"op": "insert_after", "pattern": r"^MARK$", "text": "X\n"},
                ],
            }
        ]
    }
    (tmp_path / "spec.json").write_text(json.dumps(spec), encoding="utf-8")

    rc = _run(ph, ["spec.json", "--dry-run"], tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert "+X\n" in out
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "MARK\n"


def test_apply_then_check_is_idempotent(tmp_path, capsys):
    ph = _load_patch_harness()

    (tmp_path / "a.txt").write_text("MARK\n", encoding="utf-8")
    spec = {
        "files": [
            {
                "path": "a.txt",
                "ops": [
                    {"op": "insert_after", "pattern": r"^MARK$", "text": "X\n"},
                ],
            }
        ]
    }
    (tmp_path / "spec.json").write_text(json.dumps(spec), encoding="utf-8")

    rc = _run(ph, ["spec.json"], tmp_path)
    assert rc == 0
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "MARK\nX\n"

    capsys.readouterr()
    rc = _run(ph, ["spec.json", "--check"], tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert out.strip() == "no changes"


def test_insert_after_respects_indent_token(tmp_path):
    ph = _load_patch_harness()

    (tmp_path / "m.py").write_text("def f():\n    x = 1\n", encoding="utf-8")
    spec = {
        "files": [
            {
                "path": "m.py",
                "ops": [
                    {
                        "op": "insert_after",
                        "pattern": r"^([ \t]*)x = 1$",
                        "text": "<<INDENT>>y = 2\n",
                    }
                ],
            }
        ]
    }
    (tmp_path / "spec.json").write_text(json.dumps(spec), encoding="utf-8")
    rc = _run(ph, ["spec.json"], tmp_path)
    assert rc == 0
    assert (tmp_path / "m.py").read_text(encoding="utf-8") == "def f():\n    x = 1\n    y = 2\n"


def test_ensure_import_inserts_once(tmp_path):
    ph = _load_patch_harness()

    (tmp_path / "t.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    spec = {
        "files": [
            {
                "path": "t.py",
                "ops": [
                    {"op": "ensure_import", "name": "json"},
                    {"op": "ensure_import", "name": "json"},
                ],
            }
        ]
    }
    (tmp_path / "spec.json").write_text(json.dumps(spec), encoding="utf-8")
    rc = _run(ph, ["spec.json"], tmp_path)
    assert rc == 0
    txt = (tmp_path / "t.py").read_text(encoding="utf-8")
    assert txt.count("import json") == 1


def test_check_does_not_write_files(tmp_path):
    ph = _load_patch_harness()

    f = tmp_path / "a.txt"
    f.write_text("MARK\n", encoding="utf-8")
    before = f.read_bytes()

    spec = {
        "files": [
            {
                "path": "a.txt",
                "ops": [
                    {"op": "insert_after", "pattern": r"^MARK$", "text": "X\n"},
                ],
            }
        ]
    }
    (tmp_path / "spec.json").write_text(json.dumps(spec), encoding="utf-8")

    rc = _run(ph, ["spec.json", "--check"], tmp_path)
    assert rc == 1
    assert f.read_bytes() == before


def test_check_output_is_deterministic(tmp_path, capsys):
    ph = _load_patch_harness()

    (tmp_path / "a.txt").write_text("MARK\n", encoding="utf-8")
    spec = {
        "files": [
            {
                "path": "a.txt",
                "ops": [
                    {"op": "insert_after", "pattern": r"^MARK$", "text": "X\n"},
                ],
            }
        ]
    }
    (tmp_path / "spec.json").write_text(json.dumps(spec), encoding="utf-8")

    capsys.readouterr()
    rc1 = _run(ph, ["spec.json", "--check"], tmp_path)
    out1 = capsys.readouterr().out

    capsys.readouterr()
    rc2 = _run(ph, ["spec.json", "--check"], tmp_path)
    out2 = capsys.readouterr().out

    assert rc1 == 1
    assert rc2 == 1
    assert out1 == out2
