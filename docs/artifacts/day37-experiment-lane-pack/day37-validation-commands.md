# Day 37 validation commands

```bash
python -m sdetkit day37-experiment-lane --format json --strict
python -m sdetkit day37-experiment-lane --emit-pack-dir docs/artifacts/day37-experiment-lane-pack --format json --strict
python -m sdetkit day37-experiment-lane --execute --evidence-dir docs/artifacts/day37-experiment-lane-pack/evidence --format json --strict
python scripts/check_day37_experiment_lane_contract.py
```
