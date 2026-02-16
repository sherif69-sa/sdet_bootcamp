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
    echo "How to fix: run the same command locally, inspect logs under .sdetkit/out/, and remediate before re-running premium-gate.sh."
    exit 1
  fi
}

run_step "Quality" bash quality.sh
run_step "CI" bash ci.sh
run_step "Doctor ASCII" python3 -m sdetkit doctor --ascii
run_step "Security Scan (offline SARIF)" python3 -m sdetkit security scan --fail-on none --format sarif --output .sdetkit/out/security.sarif
run_step "Control Plane Ops (CI profile)" python3 -m sdetkit ops run --profile ci --jobs 2
run_step "Evidence Pack" python3 -m sdetkit evidence pack --output .sdetkit/out/evidence.zip

echo "Premium gate passed. Artifacts: .sdetkit/out/security.sarif and .sdetkit/out/evidence.zip"
