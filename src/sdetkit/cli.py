from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Callable, Sequence
from importlib import metadata

from . import apiget, evidence, kvcli, notify, ops, patch, policy, repo, report
from .agent.cli import main as agent_main
from .doctor import main as doctor_main
from .maintenance import main as maintenance_main
from .security_gate import main as security_main

RunCommand = Callable[[list[str]], int]


class _CliParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: error: {message}\n")


def _tool_version() -> str:
    try:
        return metadata.version("sdetkit")
    except metadata.PackageNotFoundError:
        return "0+unknown"


def _run_apiget(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="sdetkit apiget", add_help=False)
    apiget._add_apiget_args(p)
    p.add_argument("--cassette", default=None, help="Cassette file path (enables record/replay).")
    p.add_argument(
        "--cassette-mode",
        choices=["auto", "record", "replay"],
        default=None,
        help="Cassette mode: auto, record, or replay.",
    )
    ns, _ = p.parse_known_args(argv)
    cassette = getattr(ns, "cassette", None)
    cassette_mode = getattr(ns, "cassette_mode", None) or "auto"

    clean: list[str] = []
    it = iter(argv)
    for item in it:
        if item.startswith("--cassette="):
            continue
        if item == "--cassette":
            next(it, None)
            continue
        if item.startswith("--cassette-mode="):
            continue
        if item == "--cassette-mode":
            next(it, None)
            continue
        clean.append(item)

    if not cassette:
        return apiget.main(clean)

    old_cassette = os.environ.get("SDETKIT_CASSETTE")
    old_mode = os.environ.get("SDETKIT_CASSETTE_MODE")
    try:
        os.environ["SDETKIT_CASSETTE"] = str(cassette)
        os.environ["SDETKIT_CASSETTE_MODE"] = str(cassette_mode)
        return apiget.main(clean)
    finally:
        if old_cassette is None:
            os.environ.pop("SDETKIT_CASSETTE", None)
        else:
            os.environ["SDETKIT_CASSETTE"] = old_cassette
        if old_mode is None:
            os.environ.pop("SDETKIT_CASSETTE_MODE", None)
        else:
            os.environ["SDETKIT_CASSETTE_MODE"] = old_mode


def _run_cassette_get(argv: list[str]) -> int:
    from .__main__ import _cassette_get

    return _cassette_get(argv)


def _command_registry() -> dict[str, RunCommand]:
    return {
        "kv": kvcli.main,
        "apiget": _run_apiget,
        "doctor": doctor_main,
        "patch": patch.main,
        "cassette-get": _run_cassette_get,
        "repo": repo.main,
        "dev": lambda argv: repo.main(["dev", *argv]),
        "report": report.main,
        "maintenance": maintenance_main,
        "agent": agent_main,
        "security": security_main,
        "ops": ops.main,
        "notify": notify.main,
        "policy": policy.main,
        "evidence": evidence.main,
    }


def _build_parser() -> tuple[_CliParser, dict[str, RunCommand]]:
    registry = _command_registry()
    parser = _CliParser(prog="sdetkit", add_help=True)
    parser.add_argument("--version", action="version", version=_tool_version())
    sub = parser.add_subparsers(dest="cmd")

    for name in registry:
        sub.add_parser(name, help=f"Run the {name} command")

    return parser, registry


def main(
    argv: Sequence[str] | None = None,
    *,
    cassette_compat_fallback: bool = False,
) -> int:
    if argv is None:
        argv = sys.argv[1:]
    raw = list(argv)
    parser, registry = _build_parser()
    known = set(registry)

    if cassette_compat_fallback and raw and raw[0] not in known and not raw[0].startswith("-"):
        try:
            return _run_cassette_get(raw)
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            return 2

    try:
        ns, rest = parser.parse_known_args(raw)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        return 2

    cmd = getattr(ns, "cmd", None)
    if not cmd:
        if rest:
            print(f"sdetkit: error: unrecognized arguments: {' '.join(rest)}", file=sys.stderr)
            return 2
        parser.print_help(sys.stdout)
        return 0

    handler = registry.get(cmd)
    if handler is None:
        print(f"sdetkit: error: unknown command: {cmd}", file=sys.stderr)
        return 2

    try:
        return int(handler(rest) or 0)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        return 2
    except Exception as exc:
        print(f"runtime error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
