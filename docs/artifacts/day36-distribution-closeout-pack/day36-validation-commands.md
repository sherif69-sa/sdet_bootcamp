# Day 36 validation commands

```bash
python -m sdetkit day36-distribution-closeout --format json --strict
python -m sdetkit day36-distribution-closeout --emit-pack-dir docs/artifacts/day36-distribution-closeout-pack --format json --strict
python -m sdetkit day36-distribution-closeout --execute --evidence-dir docs/artifacts/day36-distribution-closeout-pack/evidence --format json --strict
python scripts/check_day36_distribution_closeout_contract.py
```
