# Failure Forensics Kit

## Purpose
Explain what changed between runs and preserve reproducible failure evidence.

## Inputs
- Two run records (`sdetkit.audit.run.v1`)
- Optional evidence files for deterministic bundle generation
- Two bundles for evidence-pack diff

## Outputs / artifacts
- `sdetkit.forensics.compare.v1`
- `sdetkit.forensics.bundle.v1`
- `sdetkit.forensics.bundle-diff.v1`

## Exit-code contract
- `compare`: `1` when `--fail-on` threshold is breached
- `bundle-diff`: `1` when added/removed/changed artifacts are detected
- `2`: invalid input

## CI role
Detect regressions/new failures/resolved failures and preserve minimal repro metadata bundles.

## Example
```bash
sdetkit forensics bundle-diff --from-bundle artifacts/prev.zip --to-bundle artifacts/new.zip
```
