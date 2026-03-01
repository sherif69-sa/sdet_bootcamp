import re
from pathlib import Path


def test_ci_templates_use_bootstrap_and_no_pip_upgrade() -> None:
    root = Path(__file__).resolve().parents[1]
    ci_dir = root / "templates" / "ci"
    files = sorted([p for p in ci_dir.rglob("*") if p.is_file()])
    assert files, "expected templates/ci to contain files"

    required = ["bash scripts/bootstrap.sh", ". .venv/bin/activate"]
    forbidden = [
        r"pip install\s+-U\s+pip",
        r"python\s+-m\s+pip\s+install\s+-U\s+pip",
    ]

    for p in files:
        txt = p.read_text(encoding="utf-8")
        for s in required:
            assert s in txt, f"{p} missing required snippet: {s}"
        for pat in forbidden:
            assert re.search(pat, txt) is None, f"{p} contains forbidden pattern: {pat}"
