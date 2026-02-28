from __future__ import annotations

from pathlib import Path

from sdetkit.roadmap_manifest import check_manifest


def test_roadmap_manifest_is_fresh() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ok = check_manifest(repo_root=repo_root)
    assert ok, "docs/roadmap/manifest.json is stale; run: python -m sdetkit.roadmap_manifest write"
