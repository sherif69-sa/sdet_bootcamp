from __future__ import annotations

from sdetkit.maintenance.types import CheckAction, CheckResult, MaintenanceContext
from sdetkit.maintenance.utils import run_cmd

CHECK_NAME = "deps"
CHECK_MODES = {"quick", "full"}


def run(ctx: MaintenanceContext) -> CheckResult:
    pip_check = run_cmd([ctx.python_exe, "-m", "pip", "check"], cwd=ctx.repo_root)
    pip_check_ok = pip_check.returncode == 0

    allow_network = ctx.env.get("SDETKIT_ALLOW_NETWORK") == "1"
    pip_outdated_info: dict[str, object] = {
        "ok": True,
        "skipped": True,
        "note": "Skipped by default. Use --allow-network to run pip list --outdated.",
    }

    if allow_network:
        pip_outdated = run_cmd(
            [ctx.python_exe, "-m", "pip", "list", "--outdated"], cwd=ctx.repo_root
        )
        pip_outdated_info = {
            "ok": pip_outdated.returncode == 0,
            "rc": pip_outdated.returncode,
            "out": pip_outdated.stdout.strip(),
            "err": pip_outdated.stderr.strip(),
        }

    details = {
        "pip_check": {
            "ok": pip_check_ok,
            "rc": pip_check.returncode,
            "out": pip_check.stdout.strip(),
            "err": pip_check.stderr.strip(),
        },
        "pip_outdated": pip_outdated_info,
    }

    pip_outdated = details.get("pip_outdated")

    if isinstance(pip_outdated, dict):
        pip_outdated.setdefault("skipped", False)

    return CheckResult(
        ok=pip_check_ok,
        summary="pip dependency graph is consistent"
        if pip_check_ok
        else "pip dependency graph has issues",
        details=details,
        actions=[
            CheckAction(
                id="pip-check",
                title="Run pip check and resolve dependency conflicts",
                notes="Try: python -m pip check (and reconcile version constraints).",
            ),
        ],
    )
