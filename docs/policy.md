# Policy-as-Code

- `sdetkit policy snapshot --output .sdetkit/policies/baseline.json`
- `sdetkit policy check --baseline .sdetkit/policies/baseline.json`
- `sdetkit policy diff --baseline .sdetkit/policies/baseline.json --format sarif`

Exit codes: `0` clean, `1` regression, `2` usage/config error.
