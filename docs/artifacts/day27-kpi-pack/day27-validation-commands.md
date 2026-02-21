# Day 27 validation commands

```bash
python -m sdetkit kpi-audit --format json --strict
python -m sdetkit kpi-audit --emit-pack-dir docs/artifacts/day27-kpi-pack --format json --strict
python -m sdetkit kpi-audit --execute --evidence-dir docs/artifacts/day27-kpi-pack/evidence --format json --strict
python scripts/check_day27_kpi_audit_contract.py
```
