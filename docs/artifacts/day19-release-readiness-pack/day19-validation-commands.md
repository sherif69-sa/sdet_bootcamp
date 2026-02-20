# Day 19 validation commands

```bash
python -m sdetkit release-readiness-board --format json --strict
python -m sdetkit release-readiness-board --emit-pack-dir docs/artifacts/day19-release-readiness-pack --format json --strict
python -m sdetkit release-readiness-board --execute --evidence-dir docs/artifacts/day19-release-readiness-pack/evidence --format json --strict
python scripts/check_day19_release_readiness_board_contract.py
```
