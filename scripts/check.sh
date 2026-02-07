#!/usr/bin/env bash
set -euo pipefail

py=python
if ! command -v "$py" >/dev/null 2>&1; then
  py=python3
fi

mode=${1:-all}

run_lint() {
  ruff format --check .
  ruff check .
}

run_types() {
  mypy src/sdetkit
}

run_tests() {
  "$py" -m pytest -q
}

run_cov() {
  cov_fail_under=${COV_FAIL_UNDER:-0}
  "$py" -m pytest -q --cov=src/sdetkit --cov-report=term-missing --cov-report=xml --cov-fail-under="$cov_fail_under"
}

run_docs() {
  mkdocs build --strict
}

case "$mode" in
  lint) run_lint ;;
  types) run_types ;;
  test|tests) run_tests ;;
  cov|coverage) run_cov ;;
  docs) run_docs ;;
  all)
    run_lint
    run_types
    run_tests
    run_cov
    run_docs
    ;;
  *)
    echo "Usage: bash scripts/check.sh {lint|types|tests|coverage|docs|all}" >&2
    exit 2
    ;;
esac
