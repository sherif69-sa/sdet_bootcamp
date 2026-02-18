from __future__ import annotations

import argparse
import os
import sys


class StdoutAdapter:
    name = "stdout"

    def send(self, args: argparse.Namespace) -> int:
        sys.stdout.write(str(args.message) + "\n")
        return 0


class TelegramAdapter:
    name = "telegram"

    def send(self, args: argparse.Namespace) -> int:
        # Optional runtime dependency may be required by downstream implementation.
        token = os.environ.get("SDETKIT_TELEGRAM_TOKEN")
        chat_id = os.environ.get("SDETKIT_TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            sys.stdout.write(
                "telegram adapter not configured: set SDETKIT_TELEGRAM_TOKEN and SDETKIT_TELEGRAM_CHAT_ID.\n"
            )
            return 2
        sys.stdout.write("telegram adapter configured; use --dry-run in offline mode.\n")
        return 0


class WhatsAppAdapter:
    name = "whatsapp"

    def send(self, args: argparse.Namespace) -> int:
        # Optional runtime dependency may be required by downstream implementation.
        api_key = os.environ.get("SDETKIT_WHATSAPP_API_KEY")
        if not api_key:
            sys.stdout.write("whatsapp adapter not configured: set SDETKIT_WHATSAPP_API_KEY.\n")
            return 2
        sys.stdout.write("whatsapp adapter configured; use --dry-run in offline mode.\n")
        return 0


def stdout_adapter() -> StdoutAdapter:
    return StdoutAdapter()


def telegram_adapter() -> TelegramAdapter:
    return TelegramAdapter()


def whatsapp_adapter() -> WhatsAppAdapter:
    return WhatsAppAdapter()
