
<div align="center">

# SDET Bootcamp (sdetkit)

Production-style SDET utilities + exercises (CLI tools, quality gates, and testable modules).

[![Quality](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/quality.yml/badge.svg?branch=main)](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/quality.yml)
[![Pages](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/pages.yml/badge.svg?branch=main)](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/pages.yml)
[![Release](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/release.yml)
[![Mutation Tests](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/mutmut.yml/badge.svg?branch=main)](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/mutmut.yml)

[![Latest Release](https://img.shields.io/github/v/release/sherif69-sa/sdet_bootcamp?sort=semver)](https://github.com/sherif69-sa/sdet_bootcamp/releases)
[![License](https://img.shields.io/github/license/sherif69-sa/sdet_bootcamp)](LICENSE)

</div>

## What you get

- **CLI tools**
  - `sdetkit kv` / `kvcli`: parse `key=value` input and output JSON
  - `sdetkit apiget` / `apigetcli`: fetch JSON with pagination, retries, and timeouts
- **Library modules**
  - `sdetkit.atomicio`: atomic write helpers
  - `sdetkit.textutil`: small text utilities
  - `sdetkit.apiclient` / `sdetkit.netclient`: HTTP client utilities (sync + async)

## Quickstart

```bash
cd sdet_bootcamp

python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-test.txt -r requirements-docs.txt -e .

# Run the same checks as CI
bash scripts/check.sh all

# Run tests only
./.venv/bin/python -m pytest
CLI usage
./.venv/bin/sdetkit --help
./.venv/bin/python -m sdetkit --help

./.venv/bin/kvcli --help
./.venv/bin/apigetcli --help
If you want kvcli/apigetcli available without prefixing .venv/bin/, use one of:

# One-shot shell
bash scripts/shell.sh
apigetcli --help
kvcli --help
# Current shell only
source scripts/env.sh
apigetcli --help
kvcli --help
Project structure
.
├─ src/sdetkit/              # Package source (importable modules + CLI entrypoints)
├─ tests/                    # Unit tests + mutation killers
├─ scripts/
│  ├─ check.sh               # Quality gate runner (lint/types/tests/coverage/docs)
│  ├─ env.sh                 # Add .venv/bin to PATH (current shell)
│  └─ shell.sh               # Start a subshell with .venv/bin on PATH
├─ docs/                     # MkDocs content (published on Pages)
├─ mkdocs.yml                # Docs build config
├─ pyproject.toml            # Build + tooling config
├─ requirements-test.txt     # Dev/test tools (pytest, ruff, mypy, mutmut, ...)
└─ requirements-docs.txt     # Docs tools (mkdocs, theme)
Roadmap
See: ROADMAP.md

Contributing
See: CONTRIBUTING.md

License
MIT. See LICENSE.
