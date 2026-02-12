from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_no_stdlib_tomllib_shadowing_with_pythonpath_src() -> None:
    root = Path(__file__).resolve().parents[1]
    env = dict(os.environ)
    env["PYTHONPATH"] = "src"
    code = "import tomllib,sys;print(tomllib.__file__);print(sys.version_info[:2])"
    proc = subprocess.run(
        [sys.executable, "-c", code],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout.strip().splitlines()[0]
    assert "src/tomllib.py" not in out


def test_no_top_level_stdlib_shadow_modules_in_src() -> None:
    root = Path(__file__).resolve().parents[1]
    assert not (root / "src" / "tomllib.py").exists()
