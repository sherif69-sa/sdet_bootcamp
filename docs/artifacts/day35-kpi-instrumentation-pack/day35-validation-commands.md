# Day 35 validation commands

```bash
python -m sdetkit day35-kpi-instrumentation --format json --strict
python -m sdetkit day35-kpi-instrumentation --emit-pack-dir docs/artifacts/day35-kpi-instrumentation-pack --format json --strict
python -m sdetkit day35-kpi-instrumentation --execute --evidence-dir docs/artifacts/day35-kpi-instrumentation-pack/evidence --format json --strict
python scripts/check_day35_kpi_instrumentation_contract.py
```
