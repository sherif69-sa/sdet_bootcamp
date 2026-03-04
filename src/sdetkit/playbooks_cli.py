from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path


def _is_hidden_cmd(name: str) -> bool:
    if name.startswith("day") and len(name) > 3 and name[3].isdigit():
        return True
    if name.endswith("-closeout"):
        return True
    return False


def _discover_playbooks() -> list[str]:
    root = Path(__file__).resolve().parent
    names: set[str] = set()

    for p in root.glob("day*.py"):
        n = p.stem.replace("_", "-")
        if _is_hidden_cmd(n):
            names.add(n)

    aliases = {
        "day72-case-study-prep4-closeout": ["case-study-prep4-closeout"],
        "day73-case-study-launch-closeout": ["case-study-launch-closeout"],
        "day74-distribution-scaling-closeout": ["distribution-scaling-closeout"],
        "day75-trust-assets-refresh-closeout": ["trust-assets-refresh-closeout"],
        "day76-contributor-recognition-closeout": ["contributor-recognition-closeout"],
    }
    for k, vs in aliases.items():
        if k in names:
            names.update(vs)

    return sorted(names)


def _print_text(names: list[str]) -> None:
    print("Playbooks (hidden from main --help):")
    for n in names:
        print(f"  {n}")
    print("")
    print("Run: sdetkit playbooks run <name>")
    print("Tip: these commands still run directly, e.g. sdetkit <name> --help")


def _cmd_list(argv: Sequence[str], names: list[str]) -> int:
    p = argparse.ArgumentParser(prog="sdetkit playbooks list")
    p.add_argument("--format", choices=["text", "json"], default="text")
    ns = p.parse_args(list(argv))

    if ns.format == "json":
        out = {"count": len(names), "playbooks": names}
        sys.stdout.write(json.dumps(out, sort_keys=True) + "\n")
        return 0

    _print_text(names)
    return 0


def _cmd_run(argv: Sequence[str], names: list[str]) -> int:
    p = argparse.ArgumentParser(prog="sdetkit playbooks run")
    p.add_argument("name")
    p.add_argument("args", nargs=argparse.REMAINDER)
    ns = p.parse_args(list(argv))

    if ns.name not in names:
        sys.stderr.write("playbooks: unknown name\n")
        return 2

    from . import cli as root_cli

    try:
        return root_cli.main([ns.name, *list(ns.args)])
    except SystemExit as e:
        code = e.code
        if isinstance(code, int):
            return code
        return 2


def main(argv: Sequence[str] | None = None) -> int:
    import sys as _sys

    try:
        if argv is None:
            argv = _sys.argv[1:]

        names = _discover_playbooks()

        if not argv:
            return _cmd_list([], names)

        if argv[0] == "list":
            return _cmd_list(argv[1:], names)

        if argv[0] == "run":
            return _cmd_run(argv[1:], names)

        p = argparse.ArgumentParser(prog="sdetkit playbooks")
        sub = p.add_subparsers(dest="cmd", required=True)
        sub.add_parser("list")
        sub.add_parser("run")
        p.parse_args(list(argv))
        return 2
    except SystemExit as e:
        code = e.code
        if isinstance(code, int):
            return code
        return 2
