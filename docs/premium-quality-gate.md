# Premium Quality Gate Guidelines

This guide defines the **premium bar** for contributions in this repository.

## Core principle

Every change should be:

1. **Correct** (tests prove behavior),
2. **Safe** (security + dependency checks),
3. **Maintainable** (readable code, docs, and changelog quality),
4. **Operationally clear** (CI output and PR comments are actionable).

## Required local checks before opening a PR

Run these from repo root:

```bash
python -m ruff format --check .
python -m pre_commit run -a
bash quality.sh cov
python -m build
python -m twine check dist/*
mkdocs build
```

## Coverage expectations

- The repository-wide gate is controlled by `COV_FAIL_UNDER`.
- For premium quality, prioritize adding tests in low-coverage modules before adding new features.
- If behavior changes, include at least one failing-path test and one happy-path test.

## PR checklist (premium)

- [ ] Clear summary of what changed and why.
- [ ] Risks/edge cases called out.
- [ ] Tests added/updated with meaningful assertions.
- [ ] Docs updated for user-facing behavior.
- [ ] Changelog updated when behavior changed.
- [ ] CI and quality gates green.

## Bot helpers available

The repository supports helper comment commands on PRs:

- `/doctor` — run doctor checks and return a report.
- `/check` — run validation checks.
- `/quality` — run full coverage gate (`bash quality.sh cov`) and report coverage.
- `/hint` — post premium guideline hints and high-impact next actions.

Use these commands to quickly diagnose PR quality issues and unblock reviews.

## One-command premium gate

Use `bash premium-gate.sh` locally and in CI. It runs quality, explicit ruff checks, CI, doctor (ASCII + JSON), full maintenance checks, baseline-aware security triage, security SARIF export, control-plane ops, and evidence pack generation.

The script now also emits **real-time step recommendations**, writes per-step logs under `.sdetkit/out/`, and runs a top-level connector intelligence engine (`python3 -m sdetkit.premium_gate_engine --double-check --min-score 70 --auto-fix --fix-root .`) that unifies step logs, doctor, maintenance, and security triage artifacts into one scored control-plane summary with warnings, hotspot ranking, and prioritized recommendations.
