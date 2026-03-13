# Name 24 validation commands

```bash
python -m sdetkit onboarding-time-upgrade --format json --strict
python -m sdetkit onboarding-time-upgrade --emit-pack-dir docs/artifacts/name24-onboarding-pack --format json --strict
python -m sdetkit onboarding-time-upgrade --execute --evidence-dir docs/artifacts/name24-onboarding-pack/evidence --format json --strict
python scripts/check_name24_onboarding_time_upgrade_contract.py
```
