# Ready-to-use quickstart (after install)

Use this guide when you want a practical start to release confidence without learning the entire repository first.

If you need a 30-second rollout self-selection first, use [Choose your path](choose-your-path.md).

## Install SDETKit

Use the canonical install guide first: [install.md](install.md).

Recommended for external users:

- `python -m pip install "git+https://github.com/sherif69-sa/DevS69-sdetkit.git"`

Optional extras (`dev`, `test`, `docs`, `packaging`, `telegram`, `whatsapp`) are not required for the core release-confidence path.

## Verify your install

Run this right after installation:

```bash
python -m sdetkit --help
python -m sdetkit gate --help
```

Expected result: both commands print help text and exit with code `0`.

## Fast start (repository helper lane, optional)

```bash
bash scripts/ready_to_use.sh quick
```

What this does:

1. Bootstraps the local environment.
2. Verifies the SDETKit CLI is available.
3. Runs the CI quick lane.
4. Leaves you with a working repo and a clear next step.

For external repositories (without this repo's helper scripts), use this as the primary command:

```bash
python -m sdetkit gate fast
```

## Full release-confidence start (repository helper lane, optional)

```bash
bash scripts/ready_to_use.sh release
```

In addition to the fast start, this mode runs:

- `bash quality.sh cov`
- `python -m sdetkit security enforce --format json --max-error 0 --max-warn 0 --max-info 0`
- `python -m sdetkit gate release`

Use this when you need production-quality release evidence.

## Command behavior

- Exit code `0`: setup/checks completed successfully.
- Non-zero exit code: setup or checks failed; review the command output and fix the first failing step.

## Recommended first 10 minutes

1. Install SDETKit.
2. Verify install with `python -m sdetkit --help`.
3. Run quick confidence (`python -m sdetkit gate fast`).
4. Run strict release checks (`python -m sdetkit gate release`).
5. If you are working inside this repository, you can optionally use `scripts/ready_to_use.sh` wrappers.
6. Use [cli.md](cli.md) to discover core command families.
7. Use [adoption.md](adoption.md) to roll the same path into CI.
8. Pick a realistic rollout shape in [adoption-examples.md](adoption-examples.md).
9. Use [choose-your-path.md](choose-your-path.md) when deciding rollout order across teams.

## Next actions after setup

Follow the core path:

1. `python -m sdetkit gate fast`
2. `python -m sdetkit gate release`
3. Adopt in another repository with [adoption.md](adoption.md)

If you are inside this repository and prefer wrappers, you can run `bash scripts/ready_to_use.sh quick` and `bash scripts/ready_to_use.sh release`.

Then explore broader commands if needed:

- Explore command groups: `python -m sdetkit --help`
- See playbooks: `python -m sdetkit playbooks`
- Read release-confidence narrative: [release-confidence.md](release-confidence.md)
- Understand ecosystem scope: [integrations-and-extension-boundary.md](integrations-and-extension-boundary.md)

## Using this in another repository

If you are integrating SDETKit into an external repo (not this one), use [Adopt SDETKit in your repository](adoption.md).

That guide includes:

- Installation from GitHub
- Copy-paste GitHub Actions workflows
- A staged path from `gate fast` to stricter release gating
- Scenario-based rollout examples in [adoption-examples.md](adoption-examples.md)

If quick or release checks fail, start with [First-failure triage](first-failure-triage.md), then use the [remediation cookbook](remediation-cookbook.md) for copy-paste next steps.

If you want compact, realistic output examples before your first run, see [Sample outputs](sample-outputs.md).
