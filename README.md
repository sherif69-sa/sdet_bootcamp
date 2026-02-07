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

- CLI tools
  - `sdetkit kv` / `kvcli`: parse `key=value` input and output JSON
  - `sdetkit apiget` / `apigetcli`: fetch JSON with pagination/retries/timeouts
- A small Python library you can import in exercises:
  - `sdetkit.apiclient`, `sdetkit.netclient`, `sdetkit.atomicio`, `sdetkit.textutil`

## Quick start

One-time setup:

```bash
cd ~/sdet_bootcamp
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-test.txt -r requirements-docs.txt -e .
Daily commands (no need to "activate" venv):

./.venv/bin/python -m pytest
bash scripts/check.sh all
./.venv/bin/sdetkit --help
./.venv/bin/python -m sdetkit --help
./.venv/bin/kvcli --help
./.venv/bin/apigetcli --help
Optional: run CLIs without prefix:

cd ~/sdet_bootcamp
source scripts/env.sh
apigetcli --help
kvcli --help
Docs
Build locally:

./.venv/bin/python -m pip install -r requirements-docs.txt
bash scripts/check.sh docs
License
MIT. See LICENSE.
