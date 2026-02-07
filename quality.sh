#!/usr/bin/env bash
set -euo pipefail

mode=${1:-all}
cov_fail_under=${COV_FAIL_UNDER:-68}

run_fmt()     { ruff format .; }
run_lint()    { ruff check .; }
run_type()    { mypy src; }
run_test()    { pytest; }
run_cov()     { pytest --cov=sdetkit --cov-report=term-missing --cov-fail-under="$cov_fail_under"; }
run_mut()     { mutmut run; }
run_muthtml() { mutmut html; }

case "$mode" in
  fmt) run_fmt ;;
  lint) run_lint ;;
  type) run_type ;;
  test) run_test ;;
  cov) run_cov ;;
  mut) run_mut ;;
  muthtml) run_muthtml ;;
  all)
    run_fmt
    run_lint
    run_type
    run_test
    run_cov
    ;;
  *)
    echo "Usage: bash quality.sh {all|fmt|lint|type|test|cov|mut|muthtml}" >&2
    exit 2
    ;;
esac
