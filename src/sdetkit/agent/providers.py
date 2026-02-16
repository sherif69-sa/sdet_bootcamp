from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from typing import Protocol, cast


class Provider(Protocol):
    def complete(self, *, role: str, task: str, context: dict[str, object]) -> str: ...


@dataclass(frozen=True)
class NoneProvider:
    def complete(self, *, role: str, task: str, context: dict[str, object]) -> str:
        return f"{role}: deterministic mode active for task={task}"


@dataclass(frozen=True)
class LocalHTTPProvider:
    endpoint: str
    model: str
    timeout_s: float = 20.0

    def complete(self, *, role: str, task: str, context: dict[str, object]) -> str:
        payload = {"model": self.model, "prompt": f"[{role}] {task}", "context": context}
        body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=body,
            headers={"content-type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout_s) as response:  # noqa: S310
            raw = cast(str, response.read().decode("utf-8"))
        try:
            data = json.loads(raw)
        except ValueError:
            return raw
        if isinstance(data, dict):
            text = data.get("response") or data.get("text") or data.get("output")
            if isinstance(text, str):
                return text
        return str(raw)


@dataclass(frozen=True)
class FakeProvider:
    suffix: str = "fake"

    def complete(self, *, role: str, task: str, context: dict[str, object]) -> str:
        return f"{role}:{task}:{self.suffix}"
