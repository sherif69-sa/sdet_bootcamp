# Doctor

`doctor` is a repo health command focused on practical, release-ready diagnostics.

Run it via:

- `sdetkit doctor ...`
- `python -m sdetkit doctor ...`

Common usage:

```bash
sdetkit doctor --ascii
sdetkit doctor --all
sdetkit doctor --all --json
```

## What it checks

- `--ascii`: scans `src/` and `tools/` for non-ASCII bytes.
  - Skips `__pycache__/` and `.pyc` files.
- `--ci`: verifies required workflow files exist and validates YAML with pre-commit `check-yaml`.
- `--pre-commit`: validates pre-commit is installed and config is valid.
- `--deps`: runs `pip check` to detect dependency issues.
- `--clean-tree`: fails if `git status --porcelain` is not empty.
- `--dev`: checks whether required local developer tools are installed.

Convenience flags:

- `--all`: runs the core checks in one command.
- `--release`: runs release-oriented checks (same core checks as `--all`).

## Score and recommendations

Every run computes a `score` (0–100) from enabled checks and generates actionable `recommendations`.

- In human mode, the command prints a compact report with score, per-check status, and next steps.
- In JSON mode, the report includes `checks`, `score`, `recommendations`, and `ok`.

Example:

```bash
sdetkit doctor --all --json
```

## Output and exit codes

- Exit code `0` means all enabled checks passed.
- Non-zero means at least one enabled check failed.

Use JSON output for CI bots and human output for local debugging.
