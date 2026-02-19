from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

_DAY8_ISSUES = [
    {
        "id": "GFI-01",
        "title": "Add --format markdown example for onboarding in README role table",
        "area": "docs",
        "estimate": "S",
        "acceptance": [
            "README role-based onboarding section includes one markdown export example.",
            "Example command matches existing CLI flags and passes copy/paste validation.",
            "No broken links introduced in README/docs after update.",
        ],
    },
    {
        "id": "GFI-02",
        "title": "Add docs index quick link for day6 conversion QA sample",
        "area": "docs",
        "estimate": "S",
        "acceptance": [
            "docs/index.md quick-jump section contains an anchor to Day 6 artifact guidance.",
            "Anchor resolves in rendered markdown.",
            "docs-qa command output remains clean for modified files.",
        ],
    },
    {
        "id": "GFI-03",
        "title": "Add one positive test for onboarding --platform windows payload",
        "area": "tests",
        "estimate": "S",
        "acceptance": [
            "New test asserts windows setup snippet contains at least two actionable commands.",
            "Existing onboarding tests continue to pass.",
            "No production code behavior changes required.",
        ],
    },
    {
        "id": "GFI-04",
        "title": "Document weekly-review JSON schema fields in docs/cli.md",
        "area": "docs",
        "estimate": "S",
        "acceptance": [
            "weekly-review section lists top-level keys produced by --format json.",
            "Field descriptions match current implementation names.",
            "Examples keep line lengths readable and consistent with docs style.",
        ],
    },
    {
        "id": "GFI-05",
        "title": "Add test covering docs-qa markdown formatter heading",
        "area": "tests",
        "estimate": "M",
        "acceptance": [
            "Test verifies markdown output starts with expected Day 6 heading.",
            "Test includes at least one failing-link fixture and checks report summary counts.",
            "Test suite stays deterministic (no network calls).",
        ],
    },
    {
        "id": "GFI-06",
        "title": "Add contributor note for artifact naming convention",
        "area": "docs",
        "estimate": "S",
        "acceptance": [
            "Contributing docs include explicit docs/artifacts/dayX-* naming guidance.",
            "Examples include at least one markdown artifact path.",
            "Language remains beginner-friendly and concise.",
        ],
    },
    {
        "id": "GFI-07",
        "title": "Add smoke test for sdetkit demo --format json output shape",
        "area": "tests",
        "estimate": "M",
        "acceptance": [
            "Test asserts returned JSON includes name, steps, and hints keys.",
            "Test avoids executing shell commands (no --execute).",
            "Test passes on Linux CI environment.",
        ],
    },
    {
        "id": "GFI-08",
        "title": "Improve docs wording around strict mode in proof command",
        "area": "docs",
        "estimate": "S",
        "acceptance": [
            "docs/cli.md explains strict-mode exit behavior in one short paragraph.",
            "Example includes strict usage for local + CI context.",
            "No contradictory language with day-3 report.",
        ],
    },
    {
        "id": "GFI-09",
        "title": "Add tiny helper test for weekly review recommendation count",
        "area": "tests",
        "estimate": "S",
        "acceptance": [
            "Test asserts week-1 review includes exactly three next-week recommendations.",
            "Test uses existing repository fixture style.",
            "No snapshot files required.",
        ],
    },
    {
        "id": "GFI-10",
        "title": "Create docs snippet for running day contract scripts locally",
        "area": "docs",
        "estimate": "S",
        "acceptance": [
            "Contributing or docs index includes a command block for day contract scripts.",
            "Snippet references at least day6 and day7 script examples.",
            "Instructions remain compatible with bash on Linux/macOS.",
        ],
    },
]


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sdetkit contributor-funnel",
        description="Generate Day 8 contributor funnel good-first-issue backlog.",
    )
    p.add_argument("--format", choices=["text", "markdown", "json"], default="text")
    p.add_argument("--output", default="", help="Optional output file path.")
    return p


def _render_text() -> str:
    lines = ["Day 8 contributor funnel backlog", ""]
    for issue in _DAY8_ISSUES:
        lines.append(f"[{issue['id']}] {issue['title']}")
        lines.append(f"  area: {issue['area']} | estimate: {issue['estimate']}")
        lines.append("  acceptance:")
        for item in issue["acceptance"]:
            lines.append(f"    - {item}")
        lines.append("")
    return "\n".join(lines)


def _render_markdown() -> str:
    lines = [
        "# Day 8 contributor funnel backlog",
        "",
        "| ID | Title | Area | Estimate | Acceptance criteria |",
        "| --- | --- | --- | --- | --- |",
    ]
    for issue in _DAY8_ISSUES:
        acceptance = "<br>".join(f"- {item}" for item in issue["acceptance"])
        lines.append(
            f"| `{issue['id']}` | {issue['title']} | {issue['area']} | {issue['estimate']} | {acceptance} |"
        )
    lines.extend(
        [
            "",
            "## Day 8 execution notes",
            "",
            "- Label each item as `good first issue` and include a mentoring contact in the issue body.",
            "- Keep acceptance criteria testable so first-time contributors can self-validate before opening a PR.",
            "- Prioritize docs + tests for the first cohort to reduce ramp-up risk.",
            "",
        ]
    )
    return "\n".join(lines)


def _render_json() -> str:
    payload = {
        "name": "day8-contributor-funnel",
        "issues": _DAY8_ISSUES,
        "kpis": {
            "issue_count": len(_DAY8_ISSUES),
            "docs_items": sum(1 for i in _DAY8_ISSUES if i["area"] == "docs"),
            "tests_items": sum(1 for i in _DAY8_ISSUES if i["area"] == "tests"),
        },
    }
    return json.dumps(payload, indent=2) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(list(argv) if argv is not None else None)

    if args.format == "markdown":
        rendered = _render_markdown()
    elif args.format == "json":
        rendered = _render_json()
    else:
        rendered = _render_text()

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")

    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
