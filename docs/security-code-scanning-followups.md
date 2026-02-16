# Security code scanning follow-ups

Date: 2026-02-16

## GitHub Code Scanning API access limitation

`gh` CLI is not available in the execution environment, so GitHub Code Scanning alerts could not be fetched directly from:

- `/repos/sherif69-sa/DevS69-sdetkit/code-scanning/alerts`
- `/repos/sherif69-sa/DevS69-sdetkit/code-scanning/alerts/<N>/instances`

## Locally triaged findings to track

The local workflow run (`bash ci.sh`, `bash security.sh`) reported warning-class findings that need repository-owner triage in GitHub Code Scanning / issues:

1. `SEC_POTENTIAL_PATH_TRAVERSAL` in `src/sdetkit/apiget.py` (at-file support reads user-provided paths intentionally).
2. `SEC_POTENTIAL_PATH_TRAVERSAL` in `src/sdetkit/cassette.py` (CLI-configured cassette path handling).
3. `SEC_HIGH_ENTROPY_STRING` in docs/tests (likely false positives for documentation/test fixtures).

## Next actions for maintainers

1. Install/authenticate `gh` and fetch live alerts from GitHub.
2. Map each open alert to code location and severity.
3. For true positives that cannot be fixed quickly, create GitHub issues labeled `security` with alert links.
4. Close false positives with documented justification in alert dismissal comments.
