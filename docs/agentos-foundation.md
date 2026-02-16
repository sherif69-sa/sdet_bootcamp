# AgentOS foundation

`sdetkit agent` adds a production-safe, deterministic agent runtime that works without paid LLM APIs.

## Why this design

- **No paid API required**: default provider is `none`, so tasks run deterministically.
- **Optional local provider**: set `provider.type: local` to use localhost-only HTTP endpoints (for example, Ollama).
- **Safety-first actions**: writes are blocked unless target paths are explicitly allowlisted.

## Commands

- `sdetkit agent init`
  - Creates `.sdetkit/agent/config.yaml`
  - Creates `.sdetkit/agent/history/` and `.sdetkit/agent/workdir/`
- `sdetkit agent run "<task>"`
  - Runs manager/worker/reviewer flow
  - Stores canonical JSON run record under `.sdetkit/agent/history/<sha>.json`
- `sdetkit agent doctor`
  - Validates config, provider mode, budgets, and safety allowlists
- `sdetkit agent history`
  - Lists recent recorded runs

## Config (`.sdetkit/agent/config.yaml`)

```yaml
roles:
  manager: planner
  worker: executor
  reviewer: verifier
budgets:
  max_steps: 8
  max_actions: 4
  token_budget: 0
provider:
  type: none
  endpoint: http://127.0.0.1:11434/api/generate
  model: llama3
safety:
  write_allowlist:
    - .sdetkit/agent/workdir
  shell_allowlist:
    - python
```

`provider.type` supports:

- `none` (default, deterministic)
- `local` (optional local HTTP endpoint)
