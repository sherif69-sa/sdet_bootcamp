# Name 22 validation commands

```bash
python -m sdetkit trust-signal-upgrade --format json --strict
python -m sdetkit trust-signal-upgrade --emit-pack-dir docs/artifacts/name22-trust-pack --format json --strict
python -m sdetkit trust-signal-upgrade --execute --evidence-dir docs/artifacts/name22-trust-pack/evidence --format json --strict
python scripts/check_name22_trust_signal_upgrade_contract.py
```
