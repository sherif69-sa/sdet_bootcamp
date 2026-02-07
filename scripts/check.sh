#!/usr/bin/env bash

set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

if [ -d ".venv/bin" ]; then
  PATH="$root/.venv/bin:$PATH"
  export PATH
fi

mode=${1:-}

case "$mode" in
  lint)
    ruff check .
    ruff format --check .
    ;;
  types)
    mypy src
    ;;
  tests)
    ./.venv/bin/python -m pytest
    ;;
  coverage)
    ./.venv/bin/python -m pytest --cov=src --cov-report=term-missing --cov-report=xml
    ;;
  docs)
    mkdocs build
    ;;
  all)
    "$0" lint
    "$0" types
    "$0" tests
    "$0" coverage
    "$0" docs
    ;;
  *)
    echo "Usage: bash scripts/check.sh {lint|types|tests|coverage|docs|all}" >&2
    exit 2
    ;;
esac
