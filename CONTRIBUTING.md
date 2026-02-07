

Contributing
Thanks for helping improve sdetkit. This repo is meant to be a long-running, production-style training project.

Development setup
cd sdet_bootcamp
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-test.txt -r requirements-docs.txt -e .
Quality gates (same as CI)
bash scripts/check.sh all
Individual modes:

bash scripts/check.sh lint
bash scripts/check.sh types
bash scripts/check.sh tests
bash scripts/check.sh coverage
bash scripts/check.sh docs
Running CLIs locally
./.venv/bin/sdetkit --help
./.venv/bin/kvcli --help
./.venv/bin/apigetcli --help
Optional (current shell):

source scripts/env.sh
kvcli --help
apigetcli --help
Style and rules
Keep changes small and focused.

Add tests for behavior changes and bug fixes.

Prefer deterministic tests (no flaky timing, no external network).

Follow ruff formatting and linting.

Keep types clean (mypy passes).

Adding a new module
Add code under src/sdetkit/.

Add tests under tests/.

Ensure bash scripts/check.sh all passes.

Adding a new CLI command
Implement logic in a module under src/sdetkit/.

Wire the command in src/sdetkit/cli.py (or the current CLI router).

Add tests in tests/:

Unit tests for parsing/options

Smoke test for --help

Update README docs if the command is user-facing.

Pull request checklist
 bash scripts/check.sh all passes locally

 Tests added/updated

 Docs updated if needed (README/docs/)

 Clear PR title and description
