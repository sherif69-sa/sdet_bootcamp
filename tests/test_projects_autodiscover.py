from __future__ import annotations

from pathlib import Path

import pytest

from sdetkit.projects import discover_projects, resolve_project


def _write_pyproject(d: Path, name: str) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "pyproject.toml").write_text(
        f'[project]\nname = "{name}"\nversion = "0.0.0"\n',
        encoding="utf-8",
    )


def test_autodiscover_packages_ignores_node_modules(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    _write_pyproject(repo / "packages" / "a", "pkg-a")
    _write_pyproject(repo / "packages" / "b", "pkg-b")
    _write_pyproject(repo / "node_modules" / "junk", "junk-should-not-appear")

    source, projects = discover_projects(repo, sort=True)
    assert source == "autodiscover"
    assert [(p.name, p.root) for p in projects] == [
        ("pkg-a", "packages/a"),
        ("pkg-b", "packages/b"),
    ]

    resolved = [resolve_project(repo, p) for p in projects]
    assert [r.root_rel for r in resolved] == ["packages/a", "packages/b"]
    assert resolved[0].baseline_rel == "packages/a/.sdetkit/audit-baseline.json"


def test_pyproject_autodiscover_with_custom_roots_and_stable_order(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_pyproject(repo / "services" / "api", "svc-api")
    _write_pyproject(repo / "libs" / "core", "lib-core")
    (repo / "pyproject.toml").write_text(
        """
[tool.sdetkit.projects]
autodiscover = true
autodiscover_roots = ["services", "libs", "services"]
""".strip()
        + "\n",
        encoding="utf-8",
    )

    source, projects = discover_projects(repo, sort=True)
    assert source == "pyproject.toml (autodiscover)"
    assert [(p.name, p.root) for p in projects] == [
        ("lib-core", "libs/core"),
        ("svc-api", "services/api"),
    ]


def test_pyproject_autodiscover_validates_boolean_and_roots_type(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    (repo / "pyproject.toml").write_text(
        """
[tool.sdetkit.projects]
autodiscover = "yes"
""".strip()
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="autodiscover must be a boolean"):
        discover_projects(repo)

    (repo / "pyproject.toml").write_text(
        """
[tool.sdetkit.projects]
autodiscover = true
autodiscover_roots = 12
""".strip()
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="autodiscover_roots"):
        discover_projects(repo)
