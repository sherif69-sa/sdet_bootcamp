# Choose your path: compact adoption and rollout guide

Use this page to pick the safest rollout path after the core story is clear: **deterministic release-confidence checks and evidence-backed shipping decisions**.

## Core command set (same in all paths)

- `python -m sdetkit gate fast`
- `python -m sdetkit gate release`
- `python -m sdetkit doctor`
- `python -m sdetkit evidence --help`
- `python -m sdetkit report --help`

## If this sounds like you, start here

| Repo situation | Choose this path | First command(s) | Add next | Postpone for now |
| --- | --- | --- | --- | --- |
| Small or clean repo, want fast signal in minutes | **Path A — Fast signal first** | `python -m sdetkit gate fast` | Add CI `gate fast` and collect JSON evidence (`--format json --stable-json --out build/gate-fast.json`). | Strict enforcement on every branch. |
| Existing repo has CI, but quality/security discipline is uneven | **Path B — Stabilize baseline, then tighten** | `python -m sdetkit gate fast --format json --stable-json --out build/gate-fast.json` | Add `python -m sdetkit gate release`, keep evidence artifacts in CI, and use `doctor` in triage loops. | Broad integration/playbook expansion before core gates are stable. |
| Team needs strict release approvals now | **Path C — Release confidence first** | `python -m sdetkit gate release` | Keep `gate fast` on PRs, run `doctor` before release windows, and standardize evidence/report review in release sign-off. | Non-core taxonomy exploration during initial rollout. |

## Minimal rollout order (safe default)

1. Start with **Path A** for first signal.
2. Move to **Path B** when recurring failures and uneven discipline appear.
3. Apply **Path C** when release approvals need strict, auditable confidence.

## Curated lanes after path selection

- **Beginner lane**: [Ready-to-use setup](ready-to-use.md), [Release confidence](release-confidence.md), [Doctor](doctor.md)
- **Team adoption lane**: [Adopt SDETKit in your repository](adoption.md), [Example adoption flow](example-adoption-flow.md)
- **CI lane**: [Recommended CI flow](recommended-ci-flow.md), [CI contract](ci-contract.md), [CI artifact walkthrough](ci-artifact-walkthrough.md)
- **Advanced/extensions lane**: [CLI reference](cli.md), [API](api.md), [Plugins](plugins.md), [Tool server](tool-server.md)

Need historical context or transition-era chronology? Use [Archive and history](archive/index.md) instead of starting with day-by-day or closeout docs.
