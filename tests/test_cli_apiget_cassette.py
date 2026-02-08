from __future__ import annotations

import httpx

from sdetkit import apiget, cli


def test_apiget_cassette_record_then_replay(tmp_path, capsys, monkeypatch):
    cassette = tmp_path / "apiget.cassette"
    url = "https://example.test/x"

    def ok_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"ok": True, "url": str(request.url)},
            request=request,
        )

    monkeypatch.setattr(
        apiget.httpx, "HTTPTransport", lambda *a, **k: httpx.MockTransport(ok_handler)
    )

    rc1 = cli.main(
        [
            "apiget",
            url,
            "--expect",
            "dict",
            "--cassette",
            str(cassette),
            "--cassette-mode",
            "record",
        ]
    )
    out1 = capsys.readouterr().out
    assert rc1 == 0
    assert cassette.exists()
    assert cassette.stat().st_size > 0
    assert "ok" in out1

    def bad_handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("network/transport used during replay")

    monkeypatch.setattr(
        apiget.httpx, "HTTPTransport", lambda *a, **k: httpx.MockTransport(bad_handler)
    )

    rc2 = cli.main(
        [
            "apiget",
            url,
            "--expect",
            "dict",
            "--cassette",
            str(cassette),
            "--cassette-mode",
            "replay",
        ]
    )
    out2 = capsys.readouterr().out
    assert rc2 == 0
    assert "ok" in out2
