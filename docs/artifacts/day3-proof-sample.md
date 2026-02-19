# Day 3 proof pack

| Artifact | Step | Command | Expected snippets | Purpose |
| --- | --- | --- | --- | --- |
| `doctor-proof` | Doctor proof snapshot | `python -m sdetkit doctor --format text` | `doctor score:` + `recommendations:` | Captures repo health evidence for the Day 3 proof pack. |
| `repo-audit-proof` | Repo audit proof snapshot | `python -m sdetkit repo audit --format text` | `Repo audit:` + `Result:` | Captures governance/policy output for trust and release reviews. |
| `security-proof` | Security proof snapshot | `python -m sdetkit security report --format text` | `security scan:` + `top findings:` | Captures security findings evidence for operational handoff. |

## Execution results

| Artifact | Status | Exit code | Duration (s) | Missing snippets | Error |
| --- | --- | --- | --- | --- | --- |
| `doctor-proof` | pass | 0 | 0.58 | - | - |
| `repo-audit-proof` | pass | 0 | 1.228 | - | - |
| `security-proof` | pass | 0 | 1.947 | - | - |

## Day 3 boost hints

- Capture terminal screenshots immediately after each successful proof command.
- Use --strict in CI to enforce that all three Day 3 proof snapshots are valid.
- Use --format markdown --output docs/artifacts/day3-proof-sample.md to publish a shareable evidence bundle.
