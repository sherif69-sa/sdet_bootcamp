# Automation OS

Automation OS adds deterministic workflow execution to `sdetkit ops`.

## Why

- Enterprise-safe policy defaults.
- Offline-first execution model.
- Repeatable run history + replay + diff.

## Workflow format

Use TOML (preferred) or JSON. Required keys:

- `workflow.name`
- `workflow.version`
- `workflow.steps[]`

Step fields:

- `id`
- `type`
- `inputs`
- `outputs`
- `depends_on`
- `policy`

Variables support:

- `${input.<name>}`
- `${step.<id>.<output>}`

## Execution model

A manager validates the DAG, computes a topological plan, and dispatches steps to worker threads.
Results are always materialized in deterministic step order.

## Run history

Each run creates:

- `.sdetkit/ops-history/<run_id>/run.json`
- `.sdetkit/ops-history/<run_id>/events.jsonl`
- `.sdetkit/ops-history/<run_id>/results.json`
- `.sdetkit/ops-history/<run_id>/artifacts/`

## Replay and diff

- `sdetkit ops replay <run_id>` re-runs with captured inputs and workflow path.
- `sdetkit ops diff <run_a> <run_b>` compares step outputs and artifact checksums.
