# Name 32 validation commands

```bash
python -m sdetkit name32-release-cadence --format json --strict
python -m sdetkit name32-release-cadence --emit-pack-dir docs/artifacts/name32-release-cadence-pack --format json --strict
python -m sdetkit name32-release-cadence --execute --evidence-dir docs/artifacts/name32-release-cadence-pack/evidence --format json --strict
python scripts/check_name32_release_cadence_contract.py
```
