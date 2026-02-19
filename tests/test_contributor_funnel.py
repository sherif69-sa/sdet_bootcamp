from __future__ import annotations

import json
from pathlib import Path

from sdetkit import contributor_funnel


def test_day8_backlog_has_ten_curated_issues() -> None:
    payload = json.loads(contributor_funnel._render_json())
    assert payload["name"] == "day8-contributor-funnel"
    assert payload["kpis"]["issue_count"] == 10
    assert len(payload["issues"]) == 10
    assert all(len(item["acceptance"]) >= 3 for item in payload["issues"])


def test_markdown_output_file_written(tmp_path: Path) -> None:
    out = tmp_path / "day8.md"
    rc = contributor_funnel.main(["--format", "markdown", "--output", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "# Day 8 contributor funnel backlog" in text
    assert "`GFI-10`" in text
