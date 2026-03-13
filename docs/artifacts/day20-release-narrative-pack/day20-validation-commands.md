# Name 20 validation commands

```bash
python -m sdetkit release-narrative --format json --strict
python -m sdetkit release-narrative --emit-pack-dir docs/artifacts/name20-release-narrative-pack --format json --strict
python -m sdetkit release-narrative --execute --evidence-dir docs/artifacts/name20-release-narrative-pack/evidence --format json --strict
python scripts/check_name20_release_narrative_contract.py
```
