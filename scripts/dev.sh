#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'USAGE'
usage: scripts/dev.sh <cmd> [--fast]

Commands:
  bootstrap   Create/refresh the pinned toolchain (.venv, deps)
  quality     Run quality gate (quality.sh all)
  security    Run security gate (security.sh)
  test        Run pytest (full suite unless --fast)
  all         Run quality + security + tests

Flags:
  --fast      For "test": run a smaller smoke set (no full suite)
  -h,--help   Show help
USAGE
}

cmd="${1:-}"
case "${cmd}" in
  -h|--help|"")
    usage
    exit 0
    ;;
esac
shift || true

fast=0
for a in "$@"; do
  case "$a" in
    --fast) fast=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $a" >&2; usage; exit 2 ;;
  esac
done

bootstrap() {
  bash "$root/scripts/bootstrap.sh"
}

activate() {
  if [[ ! -f "$root/.venv/bin/activate" ]]; then
    bootstrap
  fi
  # shellcheck disable=SC1091
  . "$root/.venv/bin/activate"
}

run_quality() {
  activate
  bash "$root/quality.sh" all
}

run_security() {
  activate
  bash "$root/security.sh"
}

run_test() {
  activate
  if [[ "$fast" -eq 1 ]]; then
    python -m pytest -q tests/test_security_info_default.py tests/test_ci_templates_bootstrap.py tests/test_gate_scripts_auto_bootstrap.py
  else
    python -m pytest -q
  fi
}

case "$cmd" in
  bootstrap) bootstrap ;;
  quality) run_quality ;;
  security) run_security ;;
  test) run_test ;;
  all)
    run_quality
    run_security
    run_test
    ;;
  *)
    echo "unknown cmd: $cmd" >&2
    usage
    exit 2
    ;;
esac
