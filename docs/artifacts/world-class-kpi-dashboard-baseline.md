# World-Class KPI Dashboard Baseline

This baseline is the first implementation pass for the "Stand up a KPI dashboard" item in the World-Class Quality Program.

## Ownership

| KPI lane | Primary owner | Backup owner | Review cadence |
| --- | --- | --- | --- |
| Reliability | QA Platform Lead | Release Manager | Weekly quality review |
| Velocity | Dev Experience Lead | Engineering Manager | Weekly quality review |
| Trust/Security | Security Champion | QA Platform Lead | Monthly trust review |
| Release readiness | Release Manager | QA Platform Lead | Per release candidate |

## KPI definitions

| KPI | Definition | Target | Source command / artifact |
| --- | --- | --- | --- |
| Mainline unit+integration pass rate | Passed test jobs / total test jobs on default branch over rolling 30 days | `>= 99%` | CI run history and test summaries |
| Change failure rate | Releases requiring rollback or hotfix / total releases in rolling 30 days | `< 5%` | Release board + changelog incidents |
| MTTR for release regression | Time from regression detection to verified recovery | `< 60 minutes` | Incident timeline artifacts |
| First successful local run | Time from clone to first successful `make test` for new contributor cohort | `< 30 minutes` | Onboarding diary samples |
| PR cycle time | Median time from PR open to merge | `< 24 hours` | SCM analytics export |
| Doc freshness SLA | Critical docs updated within 48h of behavior changes | `100%` compliance | Docs PR labels + merged timestamps |
| Critical vulns on default branch | Open critical vulnerabilities affecting supported branch | `0` | Security scan reports |
| Security drift remediation | Time from baseline drift detection to fix merge | `< 72 hours` | Security baseline incidents |
| Release evidence pack coverage | Releases that include evidence pack artifacts | `100%` | Release candidate artifact inventory |
| Rollback rate | Rolled back releases / total releases | `< 2%` | Release notes + incident logs |
| Merge-ready to release tag | Time from release-ready approval to tag creation | `< 2 hours` | Release timeline |

## Data collection contract (v0)

1. Collect weekly snapshots every Monday before quality review.
2. Publish a markdown summary in `docs/artifacts/` for auditability.
3. Keep raw exports (JSON/CSV) attached to CI artifacts for 90 days.
4. Escalate any KPI that breaches target for 2 consecutive snapshots.

## Immediate next actions

- Automate extraction for CI pass rate and PR cycle time.
- Add an evidence-pack coverage check to the release workflow.
- Backfill last 4 weeks of KPI values to establish trend lines.
