```markdown
# Doctor

`doctor` is a single command that answers: "is this repo healthy?"

Run it via:

- `sdetkit doctor ...`
- `python -m sdetkit doctor ...`

Common usage:

```bash
sdetkit doctor --ascii
sdetkit doctor --all
sdetkit doctor --all --json
````

## What it checks

* `--ascii`: scans `src/` and `tools/` for non-ASCII bytes.

  * Skips `__pycache__/` and `.pyc` files.
* `--ci`: verifies required workflow files exist and runs YAML validation using pre-commit `check-yaml`.
* `--pre-commit`: validates pre-commit is available and the config can run.
* `--deps`: runs `pip check` to detect broken dependency resolution.
* `--clean-tree`: fails if `git status --porcelain` is not empty.
* `--dev`: checks for required local tools used by this repo.

Convenience flags:

* `--all`: runs the core checks in one go.
* `--release`: runs release-oriented checks (tag/version alignment and related validation).

## Output modes

Default output is human-friendly.

Use `--json` to print a stable machine-readable summary, suitable for CI or bots:

```bash
sdetkit doctor --all --json
```

Exit code behavior:

* `0` means no issues found.
* non-zero means at least one check failed.
