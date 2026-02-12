from __future__ import annotations

import socket

import pytest


@pytest.fixture(autouse=True)
def _offline_guard(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> None:
    if request.node.get_closest_marker("network"):
        return

    def _blocked(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError(
            "Network access is blocked in tests. Mark test with @pytest.mark.network if required."
        )

    monkeypatch.setattr(socket.socket, "connect", _blocked)
    monkeypatch.setattr(socket.socket, "connect_ex", _blocked)
