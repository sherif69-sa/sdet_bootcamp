# Test Intelligence Kit

## Purpose
Turn test execution noise into deterministic release intelligence.

## Inputs
- Flake history JSON
- Changed files list + test map
- Mutation policy JSON
- Failure event list for fingerprinting

## Outputs / artifacts
- `sdetkit.intelligence.flake.v1`
- `sdetkit.intelligence.impact.v1`
- `sdetkit.intelligence.env-capture.v1`
- `sdetkit.intelligence.mutation-policy.v1`
- `sdetkit.intelligence.failure-fingerprint.v1`

## Exit-code contract
- `0`: successful command and pass state (if applicable)
- `1`: policy-style failure (`passed=false`)
- `2`: invalid input/contract error

## CI role
Classify flakiness, scope impacted tests, enforce mutation governance, and capture deterministic failure fingerprints.

## Example
```bash
sdetkit intelligence failure-fingerprint --failures examples/kits/intelligence/failures.json
```

```json
{"schema_version":"sdetkit.intelligence.failure-fingerprint.v1","summary":{"total":2,"with_nondeterminism_hints":2}}
```
