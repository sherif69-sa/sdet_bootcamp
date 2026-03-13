# Name 38 validation commands

```bash
python -m sdetkit name38-distribution-batch --format json --strict
python -m sdetkit name38-distribution-batch --emit-pack-dir docs/artifacts/name38-distribution-batch-pack --format json --strict
python -m sdetkit name38-distribution-batch --execute --evidence-dir docs/artifacts/name38-distribution-batch-pack/evidence --format json --strict
python scripts/check_name38_distribution_batch_contract.py
```
