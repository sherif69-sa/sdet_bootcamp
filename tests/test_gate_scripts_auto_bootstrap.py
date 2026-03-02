import re
from pathlib import Path


def test_gate_scripts_auto_bootstrap_and_no_pip_upgrade() -> None:
    root = Path(__file__).resolve().parents[1]
    for rel in ["ci.sh", "quality.sh"]:
        p = root / rel
        txt = p.read_text(encoding="utf-8")
        assert "ensure_venv" in txt
        assert "bash scripts/bootstrap.sh" in txt
        assert ". .venv/bin/activate" in txt
        assert re.search(r"pip install\s+-U\s+pip", txt) is None
        assert re.search(r"python\s+-m\s+pip\s+install\s+-U\s+pip", txt) is None
