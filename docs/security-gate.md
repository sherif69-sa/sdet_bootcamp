# Security Gate

The `sdetkit security` command provides an offline, deterministic repository security scanner and CI gate.

## Commands

- `python -m sdetkit security scan`
  - scans repository and returns findings based on `--fail-on` threshold.
- `python -m sdetkit security check --baseline tools/security.baseline.json`
  - compares findings against a baseline and fails only on regressions.
- `python -m sdetkit security baseline --output tools/security.baseline.json`
  - writes a baseline snapshot.
- `python -m sdetkit security fix`
  - applies conservative autofixes for safe cases only.

## Output formats

Use `--format text|json|sarif` and optional `--output <path>`.

- `text`: concise developer summary (counts + top findings)
- `json`: machine-readable findings for tooling
- `sarif`: GitHub code-scanning compatible output

Example SARIF export:

```bash
python -m sdetkit security check \
  --baseline tools/security.baseline.json \
  --format sarif \
  --output build/security.sarif
```

## Regression baseline behavior

Baseline matching uses stable fingerprint attributes:

- `rule_id`
- `path`
- `line`
- `fingerprint` (`rule_id|path|line|normalized_message` hash)

Behavior:

- baseline present: fail only for **new** findings at/above threshold
- baseline missing: fail for all findings at/above threshold

## What is detected

Minimum red-flag coverage:

- dangerous execution (`eval`, `exec`, `compile`, `os.system`, `subprocess shell=True`)
- insecure deserialization (`pickle`, `dill`)
- unsafe YAML (`yaml.load` without safe loader)
- weak hashes (`md5`, `sha1`)
- obvious path traversal / unsafe writes
- secret patterns + high-entropy strings
- network calls without timeout (`requests`, `urllib`)
- `print(...)` debug leakage in `src/`

## Allowlists

Two allowlist mechanisms are supported:

1. inline allowlist comment:

```python
# sdetkit: allow-security SEC_WEAK_HASH
```

2. repository allowlist file: `tools/security_allowlist.json`

Use allowlists only for intentionally accepted risk and include rationale in code review.

## Auto-fix behavior

`python -m sdetkit security fix` only performs conservative transformations:

- `yaml.load(...)` → `yaml.safe_load(...)` when confidently matched
- adds `timeout=<N>` to simple one-line `requests.*(...)` calls missing timeout
- optionally runs `ruff --fix` when available (`--run-ruff`)

Not auto-fixed:

- `subprocess(..., shell=True)` is reported with a recommendation, not rewritten automatically.
