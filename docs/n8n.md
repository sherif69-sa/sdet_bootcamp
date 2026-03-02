# n8n Integration (PR Webhook Automation)

This repository includes a GitHub-native PR quality workflow (`pr-quality-comment.yml`) that
runs `quality.sh cov` on PR open/update and posts a PR comment.

If you want an n8n production vibe, connect GitHub webhooks to n8n and mirror the same flow:

1. GitHub webhook (`pull_request` events) → n8n Webhook node.
2. n8n triggers a runner/container job that executes:
   - `python -m pip install -U pip`
   - `python -m pip install -r requirements-test.txt -r requirements-docs.txt -e .`
   - `bash quality.sh cov`
3. n8n posts the result back using GitHub API:
   - commit status/check run
   - PR comment summary

## Minimal payload strategy

Use PR number, repo owner/name, head SHA, and workflow URL in your status/comment payload.

## Suggested comment template

```markdown
### SDET Quality Gate
- result: PASS/FAIL
- command: `bash quality.sh cov`
- details: <link to logs>
```

This keeps signal high and matches the same quick-feedback style as `sdetkit doctor --pr`.

## Recommended alignment: GitHub Actions + n8n (hybrid model)

If your goal is to make automation "work better together", the most reliable pattern is:

- Keep **required quality/security gates** in GitHub Actions (deterministic, branch-protected).
- Use **n8n for orchestration and notifications** (cross-system glue, ticketing, chat, approvals).

### What should run where

| Capability | GitHub Actions | n8n |
| --- | --- | --- |
| PR test/quality gate (`quality.sh cov`) | ✅ required check | optional mirror/comment |
| Repository audit (`sdetkit repo audit`) | ✅ required or nightly | trigger remediation workflow |
| Release/tag flow | ✅ source of truth | notify changelog + downstream systems |
| External approvals (Jira/ServiceNow/Slack) | limited | ✅ best place |
| Multi-repo portfolio dashboarding | basic artifacts | ✅ aggregate and route |

This split avoids drift while still giving you flexible enterprise automation.

## Additional workflows worth enabling

If you want stronger alignment, these are usually the highest ROI additions:

1. **`workflow_run` bridge**
   - Trigger n8n only after `ci.yml`/`quality.yml` succeeds.
   - Prevents noisy automations on failing commits.
2. **Nightly audit + drift digest**
   - Keep `repo-audit.yml` scheduled.
   - Send a single daily n8n summary to Slack/Teams instead of per-PR spam.
3. **Auto-remediation proposal path**
   - On audit/security warnings, call `sdetkit repo pr-fix` in controlled mode.
   - n8n can enrich with ticket metadata before opening/labeling PRs.
4. **Manual approval gate for production-impacting actions**
   - Use GitHub Environments for deploy constraints.
   - Use n8n for business approvers and evidence trail.

## n8n workflow blueprint (practical)

1. **Webhook (GitHub events)**
2. **Filter node** (`pull_request` + branch policy)
3. **Execute Command / CI runner trigger** (`bash quality.sh cov` and optional `sdetkit repo check --format json`)
4. **Function node** normalize to `{status, pr, sha, findings, url}`
5. **GitHub node** post check status + concise PR comment
6. **ChatOps node** (Slack/Teams) only on fail/warn

Design tip: keep one canonical JSON shape across all n8n branches so adding new automations stays low-friction.


## Example: gate on repository audit JSON

1. Add an Execute Command node:

```bash
sdetkit repo check --format json --out report.json --force
```

2. Add a Read Binary/File node to load `report.json`.
3. Add a Function node:

```javascript
const report = JSON.parse($json.data);
if (!report.summary.ok) {
  throw new Error(`Repo findings: ${report.summary.findings}`);
}
return [{ json: report.summary }];
```

This gives CI/n8n-friendly deterministic machine output.


## Production-readiness baseline (recommended)

Use this as a minimum gate before enabling broad automations:

1. Dependency bootstrap is explicit and repeatable:
   - `python -m pip install -U pip`
   - `bash scripts/bootstrap.sh
. .venv/bin/activate`
2. Core validation passes cleanly:
   - `pytest -q`
   - `bash quality.sh cov`
3. PR automation posts only on deterministic states:
   - PASS: short success note + links
   - FAIL: concise failure summary + first actionable fix
4. Remediation automations are opt-in and traceable:
   - open PRs with labels + audit trail
   - never push directly to protected branches

This keeps the repository CI-ready and avoids production drift between local checks, GitHub Actions, and n8n orchestration.
