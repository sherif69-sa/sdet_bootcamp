.PHONY: venv test lint fmt quality

venv:
	python3 -m venv .venv

test:
	. .venv/bin/activate && pytest

lint:
	. .venv/bin/activate && ruff check .

fmt:
	. .venv/bin/activate && ruff format .

quality:
	bash quality.sh
