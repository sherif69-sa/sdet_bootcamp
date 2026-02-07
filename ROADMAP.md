

Roadmap
This roadmap is intentionally practical: ship small, testable improvements that build real SDET skills.

Vision
A compact toolkit + training ground for:

CLI tooling used in real projects

Quality gates (lint, types, tests, coverage, docs)

Robust test design (including mutation testing)

Now (stabilize + polish)
Improve docs and examples for existing CLIs (kv, apiget)

More end-to-end CLI tests (help, exit codes, common failure modes)

Expand docs site content (guides, examples, patterns)

Next (capability upgrades)
Add structured logging and request tracing patterns

Add configurable retry/backoff strategies and better error classification

Add fixtures and helpers for testing APIs (mock servers, recorded responses)

Later (bigger features)
Add a small "kata" folder with graded exercises

Add a plugin system for extending sdetkit commands

Add performance-oriented testing examples (profiling, load patterns)

Definition of done
A feature is "done" when:

Tests cover behavior and edge cases

bash scripts/check.sh all is green

Docs/examples are updated for user-facing changes
