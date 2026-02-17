from __future__ import annotations

import subprocess
import sys

import pytest

from sdetkit import cli


def test_python_m_sdetkit_help_lists_unified_commands() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "sdetkit", "--help"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0
    out = proc.stdout
    for token in ("doctor", "patch", "repo", "cassette-get", "agent", "maintenance"):
        assert token in out


def test_sdetkit_entrypoint_help_lists_unified_commands(capsys: pytest.CaptureFixture[str]) -> None:
    rc = cli.main(["--help"])
    out = capsys.readouterr().out
    assert rc == 0
    for token in ("doctor", "patch", "repo", "cassette-get", "agent", "maintenance"):
        assert token in out


def test_representative_subcommand_smoke() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "sdetkit", "kv", "--text", "a=1"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0
    assert proc.stdout.strip() == '{"a": "1"}'
