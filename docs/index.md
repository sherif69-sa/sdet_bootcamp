# DevS69 SDETKit

DevS69 SDETKit is a platform for:

1. **release decision-making**
2. **deterministic evidence**
3. **test intelligence**
4. **integration assurance**
5. **failure forensics**

The first 30-second path is the flagship kit surface, not generic utilities.

## Start with flagship kits

- [Release Decision Kit](kits/release-confidence.md)
- [Test Intelligence Kit](kits/test-intelligence.md)
- [Integration Assurance Kit](kits/integration-assurance.md)
- [Failure Forensics Kit](kits/failure-forensics.md)

## Primary operator flow

1. `sdetkit release gate release`
2. `sdetkit release doctor`
3. `sdetkit release security scan`
4. `sdetkit release evidence pack`
5. `sdetkit forensics compare --from <prev> --to <current>`

## Supporting surfaces (demoted)

Utility commands such as `kv`, `apiget`, and `cassette-get` remain available for compatibility and composition, but are intentionally secondary in product positioning.
