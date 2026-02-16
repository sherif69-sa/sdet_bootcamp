from __future__ import annotations

import hashlib
from pathlib import Path

from sdetkit import evidence


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_evidence_pack_stable_manifest(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
    out = tmp_path / ".sdetkit" / "out" / "evidence.zip"
    assert evidence.main(["pack", "--output", str(out)]) == 0
    manifest = tmp_path / ".sdetkit" / "out" / "manifest.json"
    first = _sha(manifest)
    assert evidence.main(["pack", "--output", str(out)]) == 0
    second = _sha(manifest)
    assert first == second
