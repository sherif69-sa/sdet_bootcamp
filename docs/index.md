<div class="hero-panel" markdown>

# DevS69 SDETKit

Ship trusted software faster with deterministic SDET + DevOps workflows: repository diagnostics, API validation, policy gates, and release evidence packs.

<div class="hero-actions" markdown>

[Get started](#fast-start){ .md-button .md-button--primary }
[Open command reference](cli.md){ .md-button }

</div>

</div>

<div class="kpi-strip" markdown>

- **Deterministic by default** — stable output and CI-safe exit codes.
- **Release ready** — quality, security, and governance gates in one toolkit.
- **Operator friendly** — practical commands, docs, and artifacts for handoffs.

</div>

## Product vision

SDETKit is built for teams that need to move quickly **without sacrificing trust**. The platform centers on three outcomes:

1. **Reliability** — repeatable checks from laptop to CI.
2. **Readiness** — objective go/no-go evidence for release decisions.
3. **Adoption UX** — role-based onboarding and clear workflows.

## Fast start

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-test.txt -r requirements-docs.txt -e .
bash ci.sh quick --skip-docs
```

!!! tip "First 10-minute path"
    Run **CLI help** → **Doctor** → **Gate fast** to validate environment, repository hygiene, and baseline quality posture.

## Platform capabilities

<div class="grid cards" markdown>

- [**Repository diagnostics**](doctor.md)
  Detect hygiene, policy, and reliability gaps with actionable remediation guidance.

- [**Deterministic API validation**](api.md)
  Execute and replay API checks with cassettes for stable test behavior.

- [**Policy + security enforcement**](security-gate.md)
  Enforce deterministic thresholds and prevent drift in quality/security posture.

- [**Release evidence packs**](evidence.md)
  Export machine-readable artifacts for audits, handoffs, and governance reviews.

- [**Patch-safe change workflows**](patch-harness.md)
  Apply controlled updates with validation hooks to reduce merge risk.

- [**Scalable delivery operations**](production-readiness.md)
  Standardize CI lanes and release controls for enterprise-ready execution.

</div>

## UX-ready navigation by role

<div class="grid cards" markdown>

- **SDET / QA engineers**
  Start with [CLI](cli.md), [Doctor](doctor.md), and [API](api.md).

- **Platform / DevOps teams**
  Start with [Production readiness](production-readiness.md), [Security gate](security-gate.md), and [Patch harness](patch-harness.md).

- **Tech leads / maintainers**
  Start with [Repo tour](repo-tour.md), [Project structure](project-structure.md), and [Design](design.md).

</div>

## Readiness scorecard model

| Area | What good looks like | Primary command |
| --- | --- | --- |
| Quality | CI-equivalent checks are green and reproducible | `bash ci.sh quick --skip-docs` |
| Coverage | Coverage gate meets release threshold | `bash quality.sh cov` |
| Security | Policy budgets are enforced with zero drift | `python -m sdetkit security enforce --format json --max-error 0 --max-warn 0 --max-info 0` |
| Evidence | Artifacts are generated and stored for review | `python -m sdetkit evidence --help` |

## Continue exploring

- [Repo tour](repo-tour.md)
- [Contributing](contributing.md)
- [Security policy](security.md)
- [Releasing](releasing.md)
