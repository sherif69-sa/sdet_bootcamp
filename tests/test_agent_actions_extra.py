from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from sdetkit.agent.actions import ActionRegistry, maybe_parse_action_task


def test_maybe_parse_action_task_variants() -> None:
    assert maybe_parse_action_task("noop") is None
    assert maybe_parse_action_task("action fs.read") == ("fs.read", {})
    assert maybe_parse_action_task("action x 1") == ("x", {"value": 1})
    assert maybe_parse_action_task("action x [1,2]") == ("x", {"value": [1, 2]})


def test_action_registry_error_paths(tmp_path: Path, monkeypatch) -> None:
    reg = ActionRegistry(
        root=tmp_path, write_allowlist=("allowed",), shell_allowlist=("python -c",)
    )

    assert reg.run("missing", {}).ok is False
    assert reg.run("fs.read", {"path": "/abs"}).ok is False
    assert reg.run("fs.write", {"path": "denied/out.txt", "content": "x"}).ok is False
    assert reg.run("shell.run", {"cmd": ""}).ok is False
    assert reg.run("shell.run", {"cmd": 'python -c "x'}).ok is False

    class _P:
        returncode = 1
        stdout = ""
        stderr = "bad"

    monkeypatch.setattr("subprocess.run", lambda *a, **k: _P())
    res = reg.run("shell.run", {"cmd": 'python -c "print(1)"'})
    assert res.ok is False

    import pytest

    with pytest.raises(ValueError):
        reg.run("report.build", {"output": "/abs/path.html", "format": "html"})


def test_action_registry_success_paths(tmp_path: Path, monkeypatch) -> None:
    reg = ActionRegistry(
        root=tmp_path,
        write_allowlist=("allowed", "nested/dir"),
        shell_allowlist=("python -c", "bad ["),
    )
    (tmp_path / "allowed").mkdir()
    (tmp_path / "allowed" / "in.txt").write_text("hello", encoding="utf-8")

    read_res = reg.run("fs.read", {"path": "allowed/in.txt"})
    assert read_res.ok is True
    assert read_res.payload["content"] == "hello"

    write_res = reg.run("fs.write", {"path": "nested/dir/out.txt", "content": "abc"})
    assert write_res.ok is True
    assert write_res.payload["bytes"] == 3
    assert (tmp_path / "nested" / "dir" / "out.txt").read_text(encoding="utf-8") == "abc"

    monkeypatch.setattr(
        "subprocess.run",
        lambda *a, **k: SimpleNamespace(returncode=0, stdout="ok", stderr=""),
    )
    shell_res = reg.run("shell.run", {"cmd": 'python -c "print(1)"'})
    assert shell_res.ok is True
    assert shell_res.payload["stdout"] == "ok"


def test_action_registry_repo_audit_and_report_build(tmp_path: Path, monkeypatch) -> None:
    reg = ActionRegistry(root=tmp_path, write_allowlist=(".sdetkit",), shell_allowlist=("python",))

    monkeypatch.setattr(
        "sdetkit.repo.run_repo_audit",
        lambda root, profile="default": {"findings": [1, 2], "checks": ["a"]},
    )
    seen: dict[str, object] = {}

    def _fake_build_dashboard(*, history_dir, output, fmt, since):
        seen["history_dir"] = history_dir
        seen["output"] = output
        seen["fmt"] = fmt
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("dashboard", encoding="utf-8")

    monkeypatch.setattr("sdetkit.agent.actions.build_dashboard", _fake_build_dashboard)

    audit_res = reg.run("repo.audit", {"profile": "strict"})
    assert audit_res.ok is True
    assert audit_res.payload == {"profile": "strict", "findings": 2, "checks": 1}

    report_res = reg.run("report.build", {"output": ".sdetkit/out.html", "format": "html"})
    assert report_res.ok is True
    assert seen["fmt"] == "html"
    assert str(seen["history_dir"]).endswith(".sdetkit/agent/history")
    assert (tmp_path / ".sdetkit" / "out.html").read_text(encoding="utf-8") == "dashboard"
