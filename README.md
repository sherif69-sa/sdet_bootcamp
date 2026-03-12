# DevS69 SDETKit

DevS69 SDETKit is an operator-grade **release confidence + test intelligence platform**.
It turns go/no-go decisions into deterministic, machine-readable contracts with actionable next steps.

## Flagship kits

- **Release Decision Kit** (`sdetkit release ...`)
  - Gate, doctor, security, evidence, and repo governance for release decisions.
- **Test Intelligence Kit** (`sdetkit intelligence ...`)
  - Flake classification, impacted-tests mapping, deterministic env capture, failure fingerprinting, and mutation governance.
- **Integration Assurance Kit** (`sdetkit integration ...`)
  - Environment readiness profiles, integration matrix outputs, and cassette contract validation for replay safety.
- **Failure Forensics Kit** (`sdetkit forensics ...`)
  - Run-to-run regression analysis, stable fingerprints, deterministic repro bundles, and evidence-pack diffs.

```bash
python -m sdetkit kits list --format json
```

## Hero journeys

```bash
python -m sdetkit release gate release
python -m sdetkit intelligence flake classify --history examples/kits/intelligence/flake-history.json
python -m sdetkit intelligence failure-fingerprint --failures examples/kits/intelligence/failures.json
python -m sdetkit integration check --profile examples/kits/integration/profile.json
python -m sdetkit forensics compare --from examples/kits/forensics/run-a.json --to examples/kits/forensics/run-b.json --fail-on error
```

## Product boundary

Utilities remain for compatibility (`kv`, `apiget`, `cassette-get`, docs helpers), but they are **supporting surfaces** and no longer define the primary product path.

## Backward compatibility

Existing commands and aliases remain supported (`gate`, `doctor`, `security`, `repo`, `evidence`, `report`, etc.).
Kit commands are additive product grouping aliases.

## Kit docs

- `docs/kits/release-confidence.md`
- `docs/kits/test-intelligence.md`
- `docs/kits/integration-assurance.md`
- `docs/kits/failure-forensics.md`
