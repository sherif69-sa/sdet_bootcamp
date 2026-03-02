# Day 75 validation commands

```bash
python -m sdetkit day75-trust-assets-refresh-closeout --format json --strict
python -m sdetkit day75-trust-assets-refresh-closeout --emit-pack-dir docs/artifacts/day75-trust-assets-refresh-closeout-pack --format json --strict
python scripts/check_day75_trust_assets_refresh_closeout_contract.py --skip-evidence
```
