from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from pathlib import Path
from typing import Any

_PAGE_PATH = "docs/integrations-day31-phase2-kickoff.md"
_TOP10_PATH = "docs/top-10-github-strategy.md"
_SECTION_HEADER = "# Day 31 — Phase-2 kickoff baseline"
_REQUIRED_SECTIONS = [
    "## Why Day 31 matters",
    "## Required inputs (Day 30)",
    "## Day 31 command lane",
    "## Baseline + weekly targets",
    "## Scoring model",
]
_REQUIRED_COMMANDS = [
    "python -m sdetkit day31-phase2-kickoff --format json --strict",
    "python -m sdetkit day31-phase2-kickoff --emit-pack-dir docs/artifacts/day31-phase2-pack --format json --strict",
    "python -m sdetkit day31-phase2-kickoff --execute --evidence-dir docs/artifacts/day31-phase2-pack/evidence --format json --strict",
    "python scripts/check_day31_phase2_kickoff_contract.py",
]
_EXECUTION_COMMANDS = [
    "python -m sdetkit day31-phase2-kickoff --format json --strict",
    "python scripts/check_day31_phase2_kickoff_contract.py --skip-evidence",
]

_DAY31_DEFAULT_PAGE = """# Day 31 — Phase-2 kickoff baseline

Day 31 starts Phase-2 with a measurable baseline carried over from Day 30 and a fixed weekly growth target set.

## Why Day 31 matters

- Converts Day 30 handoff into a measurable execution contract.
- Locks objective targets so weekly reviews can score progress without ambiguity.
- Forces evidence-backed growth planning before feature/distribution expansion.

## Required inputs (Day 30)

- `docs/artifacts/day30-wrap-pack/day30-phase1-wrap-summary.json`
- `docs/artifacts/day30-wrap-pack/day30-phase2-backlog.md`

## Day 31 command lane

```bash
python -m sdetkit day31-phase2-kickoff --format json --strict
python -m sdetkit day31-phase2-kickoff --emit-pack-dir docs/artifacts/day31-phase2-pack --format json --strict
python -m sdetkit day31-phase2-kickoff --execute --evidence-dir docs/artifacts/day31-phase2-pack/evidence --format json --strict
python scripts/check_day31_phase2_kickoff_contract.py
```

## Baseline + weekly targets

- Baseline source: Day 30 activation score and closeout rollup.
- Week-1 Phase-2 target: maintain activation score >= 95 and preserve strict pass.
- Week-1 growth target: publish 3 external-facing assets and 1 KPI checkpoint.
- Week-1 quality gate: every shipped action includes command evidence and a summary artifact.

## Scoring model

Day 31 weighted score (0-100):

- Docs contract + command lane completeness: 35 points.
- Discoverability alignment (README/docs index/top-10): 25 points.
- Day 30 input continuity + quality thresholds: 30 points.
- Weekly target contract quality: 10 points.
"""


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _load_day30(path: Path) -> tuple[float, bool]:
    if not path.exists():
        return 0.0, False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 0.0, False
    summary = data.get("summary") if isinstance(data, dict) else None
    score = summary.get("activation_score") if isinstance(summary, dict) else None
    strict_pass = summary.get("strict_pass") if isinstance(summary, dict) else False
    if isinstance(score, (int, float)):
        return float(score), bool(strict_pass)
    return 0.0, False


def build_day31_phase2_kickoff_summary(
    root: Path,
    *,
    readme_path: str = "README.md",
    docs_index_path: str = "docs/index.md",
    docs_page_path: str = _PAGE_PATH,
    top10_path: str = _TOP10_PATH,
) -> dict[str, Any]:
    page_path = root / docs_page_path
    page_text = _read(page_path)
    readme_text = _read(root / readme_path)
    docs_index_text = _read(root / docs_index_path)
    top10_text = _read(root / top10_path)

    missing_sections = [s for s in [_SECTION_HEADER, *_REQUIRED_SECTIONS] if s not in page_text]
    missing_commands = [c for c in _REQUIRED_COMMANDS if c not in page_text]

    day30_summary = root / "docs/artifacts/day30-wrap-pack/day30-phase1-wrap-summary.json"
    day30_backlog = root / "docs/artifacts/day30-wrap-pack/day30-phase2-backlog.md"
    day30_score, day30_strict = _load_day30(day30_summary)

    checklist_count = sum(1 for line in page_text.splitlines() if line.strip().startswith("- ") and "target" in line.lower())

    checks: list[dict[str, Any]] = [
        {"key": "docs_page_exists", "weight": 10, "passed": page_path.exists(), "evidence": str(page_path)},
        {"key": "required_sections_present", "weight": 15, "passed": not missing_sections, "evidence": {"missing_sections": missing_sections}},
        {"key": "required_commands_present", "weight": 10, "passed": not missing_commands, "evidence": {"missing_commands": missing_commands}},
        {"key": "readme_day31_link", "weight": 10, "passed": "docs/integrations-day31-phase2-kickoff.md" in readme_text, "evidence": "docs/integrations-day31-phase2-kickoff.md"},
        {"key": "readme_day31_command", "weight": 5, "passed": "day31-phase2-kickoff" in readme_text, "evidence": "day31-phase2-kickoff"},
        {"key": "docs_index_day31_links", "weight": 10, "passed": ("day-31-ultra-upgrade-report.md" in docs_index_text and "integrations-day31-phase2-kickoff.md" in docs_index_text), "evidence": "day-31-ultra-upgrade-report.md + integrations-day31-phase2-kickoff.md"},
        {"key": "top10_day31_alignment", "weight": 5, "passed": ("Day 31 — Phase-2 kickoff" in top10_text and "Day 32 — Release cadence setup" in top10_text), "evidence": "Day 31 + Day 32 strategy chain"},
        {"key": "day30_summary_present", "weight": 10, "passed": day30_summary.exists(), "evidence": str(day30_summary)},
        {"key": "day30_backlog_present", "weight": 10, "passed": day30_backlog.exists(), "evidence": str(day30_backlog)},
        {"key": "day30_strict_quality", "weight": 10, "passed": day30_strict and day30_score >= 90, "evidence": {"day30_score": day30_score, "strict_pass": day30_strict}},
        {"key": "weekly_target_contract", "weight": 5, "passed": checklist_count >= 3, "evidence": {"target_lines": checklist_count}},
    ]

    failed = [c for c in checks if not c["passed"]]
    score = int(round(sum(c["weight"] for c in checks if c["passed"])))
    critical_failures: list[str] = []
    if not day30_summary.exists() or not day30_backlog.exists():
        critical_failures.append("day30_handoff_inputs")

    wins: list[str] = []
    misses: list[str] = []
    handoff_actions: list[str] = []

    if day30_strict:
        wins.append(f"Day 30 handoff continuity verified (score={day30_score}).")
    else:
        misses.append("Day 30 strict continuity signal is missing or below threshold.")
        handoff_actions.append("Re-run Day 30 wrap command and restore strict pass baseline before Phase-2 expansion.")

    if checklist_count >= 3:
        wins.append(f"Day 31 weekly target contract locked with {checklist_count} target lines.")
    else:
        misses.append("Weekly target contract is incomplete (<3 target lines).")
        handoff_actions.append("Expand Day 31 baseline + weekly targets section with at least 3 explicit target bullets.")

    if not failed and not critical_failures:
        wins.append("Day 31 kickoff is launch-ready for immediate Phase-2 execution.")

    return {
        "name": "day31-phase2-kickoff",
        "inputs": {
            "readme": readme_path,
            "docs_index": docs_index_path,
            "docs_page": docs_page_path,
            "top10": top10_path,
            "day30_summary": str(day30_summary.relative_to(root)) if day30_summary.exists() else str(day30_summary),
            "day30_backlog": str(day30_backlog.relative_to(root)) if day30_backlog.exists() else str(day30_backlog),
        },
        "checks": checks,
        "rollup": {"day30_activation_score": day30_score},
        "summary": {
            "activation_score": score,
            "passed_checks": len(checks) - len(failed),
            "failed_checks": len(failed),
            "critical_failures": critical_failures,
            "strict_pass": not failed and not critical_failures,
        },
        "wins": wins,
        "misses": misses,
        "handoff_actions": handoff_actions,
    }


def _to_text(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    return (
        "Day 31 phase-2 kickoff summary\n"
        f"Activation score: {summary['activation_score']}\n"
        f"Passed checks: {summary['passed_checks']}\n"
        f"Failed checks: {summary['failed_checks']}\n"
        f"Critical failures: {', '.join(summary['critical_failures']) if summary['critical_failures'] else 'none'}\n"
    )


def _to_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Day 31 phase-2 kickoff summary",
        "",
        f"- Activation score: **{summary['activation_score']}**",
        f"- Passed checks: **{summary['passed_checks']}**",
        f"- Failed checks: **{summary['failed_checks']}**",
        f"- Critical failures: **{', '.join(summary['critical_failures']) if summary['critical_failures'] else 'none'}**",
        "",
        "## Day 30 continuity",
        "",
        f"- Day 30 activation score: `{payload['rollup']['day30_activation_score']}`",
        "",
        "## Wins",
    ]
    lines.extend(f"- {item}" for item in payload["wins"])
    lines.append("\n## Misses")
    lines.extend(f"- {item}" for item in payload["misses"] or ["No misses recorded."])
    lines.append("\n## Handoff actions")
    lines.extend(f"- [ ] {item}" for item in payload["handoff_actions"] or ["No handoff actions required."])
    return "\n".join(lines) + "\n"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _emit_pack(root: Path, payload: dict[str, Any], pack_dir: Path) -> None:
    target = (root / pack_dir).resolve() if not pack_dir.is_absolute() else pack_dir
    target.mkdir(parents=True, exist_ok=True)
    _write(target / "day31-phase2-kickoff-summary.json", json.dumps(payload, indent=2) + "\n")
    _write(target / "day31-phase2-kickoff-summary.md", _to_markdown(payload))
    _write(target / "day31-weekly-targets-checklist.md", "# Day 31 weekly targets\n\n- [ ] Activation score remains >= 95\n- [ ] 3 external-facing assets planned for this week\n- [ ] 1 KPI checkpoint artifact generated\n")
    _write(target / "day31-validation-commands.md", "# Day 31 validation commands\n\n```bash\n" + "\n".join(_REQUIRED_COMMANDS) + "\n```\n")


def _run_execution(root: Path, evidence_dir: Path) -> None:
    target = (root / evidence_dir).resolve() if not evidence_dir.is_absolute() else evidence_dir
    target.mkdir(parents=True, exist_ok=True)
    logs: list[dict[str, Any]] = []
    for command in _EXECUTION_COMMANDS:
        proc = subprocess.run(shlex.split(command), cwd=root, text=True, capture_output=True, check=False)
        logs.append({"command": command, "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr})
    summary = {
        "name": "day31-phase2-kickoff-execution",
        "total_commands": len(logs),
        "failed_commands": [log["command"] for log in logs if log["returncode"] != 0],
        "commands": logs,
    }
    _write(target / "day31-execution-summary.json", json.dumps(summary, indent=2) + "\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Day 31 phase-2 kickoff baseline scorer.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--output")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--emit-pack-dir")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--evidence-dir")
    parser.add_argument("--write-defaults", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    ns = parser.parse_args(argv)
    root = Path(ns.root).resolve()

    if ns.write_defaults:
        page = root / _PAGE_PATH
        if not page.exists():
            _write(page, _DAY31_DEFAULT_PAGE)

    payload = build_day31_phase2_kickoff_summary(root)

    if ns.emit_pack_dir:
        _emit_pack(root, payload, Path(ns.emit_pack_dir))
    if ns.execute:
        ev_dir = Path(ns.evidence_dir) if ns.evidence_dir else Path("docs/artifacts/day31-phase2-pack/evidence")
        _run_execution(root, ev_dir)

    if ns.format == "json":
        rendered = json.dumps(payload, indent=2) + "\n"
    elif ns.format == "markdown":
        rendered = _to_markdown(payload)
    else:
        rendered = _to_text(payload)

    if ns.output:
        _write((root / ns.output).resolve() if not Path(ns.output).is_absolute() else Path(ns.output), rendered)
    else:
        print(rendered, end="")

    if ns.strict and (payload["summary"]["failed_checks"] > 0 or payload["summary"]["critical_failures"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
