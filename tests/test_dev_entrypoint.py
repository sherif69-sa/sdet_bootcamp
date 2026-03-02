from __future__ import annotations

import subprocess
from pathlib import Path


def test_dev_entrypoint_help_is_stable() -> None:
    root = Path(__file__).resolve().parents[1]
    dev = root / "scripts" / "dev.sh"
    assert dev.exists()

    res = subprocess.run(
        ["bash", str(dev), "--help"],
        cwd=root / "docs",
        check=True,
        capture_output=True,
        text=True,
    )
    out = res.stdout
    assert "usage:" in out
    assert "bootstrap" in out
    assert "quality" in out
    assert "security" in out
    assert "test" in out
    assert "--fast" in out
