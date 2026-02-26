# Day 33 validation commands

```bash
python -m sdetkit day33-demo-asset --format json --strict
python -m sdetkit day33-demo-asset --emit-pack-dir docs/artifacts/day33-demo-asset-pack --format json --strict
python -m sdetkit day33-demo-asset --execute --evidence-dir docs/artifacts/day33-demo-asset-pack/evidence --format json --strict
python scripts/check_day33_demo_asset_contract.py
```
