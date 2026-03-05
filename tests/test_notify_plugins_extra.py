from __future__ import annotations

import argparse

from sdetkit import notify_plugins


def test_stdout_adapter_send_writes_message(capsys) -> None:
    args = argparse.Namespace(message="hello")
    rc = notify_plugins.StdoutAdapter().send(args)
    assert rc == 0
    assert capsys.readouterr().out == "hello\n"


def test_telegram_adapter_configured_path(monkeypatch, capsys) -> None:
    monkeypatch.setenv("SDETKIT_TELEGRAM_TOKEN", "token")
    monkeypatch.setenv("SDETKIT_TELEGRAM_CHAT_ID", "chat")
    args = argparse.Namespace(message="ignored")
    rc = notify_plugins.TelegramAdapter().send(args)
    assert rc == 0
    assert "configured" in capsys.readouterr().out


def test_whatsapp_adapter_configured_path(monkeypatch, capsys) -> None:
    monkeypatch.setenv("SDETKIT_WHATSAPP_API_KEY", "k")
    args = argparse.Namespace(message="ignored")
    rc = notify_plugins.WhatsAppAdapter().send(args)
    assert rc == 0
    assert "configured" in capsys.readouterr().out


def test_adapter_factory_helpers_return_expected_types() -> None:
    assert isinstance(notify_plugins.stdout_adapter(), notify_plugins.StdoutAdapter)
    assert isinstance(notify_plugins.telegram_adapter(), notify_plugins.TelegramAdapter)
    assert isinstance(notify_plugins.whatsapp_adapter(), notify_plugins.WhatsAppAdapter)
