# Contributing

Use the repository root guide (`CONTRIBUTING.md`) for the full contributor workflow.

Quick start:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .[dev,test,docs]
pre-commit install
pre-commit run -a
bash quality.sh cov
mkdocs build
```
