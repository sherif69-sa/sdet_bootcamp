#!/usr/bin/env bash

set -euo pipefail

mode=${1:-all}
py=${PYTHON:-python}
if ! command -v "$py" >/dev/null 2>&1; then
  py=python3
fi

case "$mode" in
  lint)
    "$py" -m ruff check .
    "$py" -m ruff format --check .
    ;;
  types)
    "$py" -m mypy src/sdetkit
    ;;
  test)
    "$py" -m pytest -q
    ;;
  cov)
    "$py" -m pytest -q --cov=src/sdetkit --cov-report=term-missing --cov-report=xml --cov-fail-under="${COV_FAIL_UNDER:-0}"
    ;;
  docs)
    "$py" -m mkdocs build --strict
    ;;
  all)
    "$py" -m ruff check .
    "$py" -m ruff format --check .
    "$py" -m mypy src/sdetkit
    "$py" -m pytest -q --cov=src/sdetkit --cov-report=term-missing --cov-report=xml --cov-fail-under="${COV_FAIL_UNDER:-0}"
    "$py" -m mkdocs build --strict
    ;;
  *)
    echo "Usage: bash scripts/check.sh {all|lint|types|test|cov|docs}" >&2
    exit 2
    ;;
esac
