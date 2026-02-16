#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

section() {
  printf '\n==> %s\n' "$1"
}

run_step() {
  local title="$1"
  shift
  section "$title"
  if ! "$@"; then
    echo "ERROR: step failed: $title"
    echo "How to fix: run the command locally, review output, and address findings before re-running premium-gate.sh"
    exit 1
  fi
}

run_step "Quality" bash quality.sh
run_step "CI" bash ci.sh
run_step "Doctor ASCII" python3 -m sdetkit doctor --ascii
run_step "Repository audit" python3 -m sdetkit repo audit . --format text --fail-on medium
run_step "Security scan (offline default + SARIF)" \
  python3 -m sdetkit security scan --fail-on medium --format sarif --output security.sarif

echo "\nPremium gate passed. SARIF written to security.sarif"
