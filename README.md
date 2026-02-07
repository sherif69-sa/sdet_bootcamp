<div align="center">

# SDET Bootcamp (sdetkit)

Production-style SDET utilities + exercises: CLI tools, quality gates, and testable modules.

[![Quality](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/quality.yml/badge.svg?branch=main)](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/quality.yml)
[![Pages](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/pages.yml/badge.svg?branch=main)](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/pages.yml)
[![Release](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/release.yml)
[![Mutation Tests](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/mutmut.yml/badge.svg?branch=main)](https://github.com/sherif69-sa/sdet_bootcamp/actions/workflows/mutmut.yml)

[![Latest Release](https://img.shields.io/github/v/release/sherif69-sa/sdet_bootcamp?sort=semver)](https://github.com/sherif69-sa/sdet_bootcamp/releases)
[![License](https://img.shields.io/github/license/sherif69-sa/sdet_bootcamp)](LICENSE)

</div>

## Features

- CLI tools:
  - `sdetkit kv` / `kvcli`: parse `key=value` input and output JSON
  - `sdetkit apiget` / `apigetcli`: fetch JSON with pagination/retries/timeouts
- Quality gates (same ones CI runs): formatting, lint, types, tests, coverage, docs
- Small modules meant for exercises and kata-style tasks

## Install (dev)

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-test.txt -r requirements-docs.txt -e .
Quickstart
./.venv/bin/python -m sdetkit --help
./.venv/bin/python -m sdetkit kv --help
./.venv/bin/python -m sdetkit apiget --help
Run console scripts directly:

./.venv/bin/kvcli --help
./.venv/bin/apigetcli --help
If you want kvcli and apigetcli available without typing ./.venv/bin/:

bash scripts/shell.sh
Development
bash scripts/check.sh all
Documentation
mkdocs serve
License
MIT. See LICENSE.
