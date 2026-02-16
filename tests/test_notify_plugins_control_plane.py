from __future__ import annotations

from pathlib import Path

from sdetkit import notify


def test_missing_optional_dependency_or_config_returns_2(monkeypatch) -> None:
    monkeypatch.delenv("SDETKIT_TELEGRAM_TOKEN", raising=False)
    monkeypatch.delenv("SDETKIT_TELEGRAM_CHAT_ID", raising=False)
    rc = notify.main(["telegram", "--message", "x"])
    assert rc == 2


def test_stub_stdout_available(capsys) -> None:
    assert notify.main(["stdout", "--message", "hello"]) == 0
    assert "hello" in capsys.readouterr().out


def test_registry_plugin_loads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    pkg = tmp_path / "myplug.py"
    pkg.write_text(
        "class X:\n"
        "    name='x'\n"
        "    def send(self,args):\n"
        "        print('x:' + args.message)\n"
        "        return 0\n"
        "def factory():\n"
        "    return X()\n",
        encoding="utf-8",
    )
    (tmp_path / ".sdetkit").mkdir()
    (tmp_path / ".sdetkit" / "plugins.toml").write_text(
        '[notify]\nx = "myplug:factory"\n', encoding="utf-8"
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    assert notify.main(["x", "--message", "ok"]) == 0
