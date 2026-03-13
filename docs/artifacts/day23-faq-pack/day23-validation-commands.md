# Name 23 validation commands

```bash
python -m sdetkit faq-objections --format json --strict
python -m sdetkit faq-objections --emit-pack-dir docs/artifacts/name23-faq-pack --format json --strict
python -m sdetkit faq-objections --execute --evidence-dir docs/artifacts/name23-faq-pack/evidence --format json --strict
python scripts/check_name23_faq_objections_contract.py
```
