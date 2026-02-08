from __future__ import annotations

import json
from pathlib import Path

import httpx

from sdetkit import apiget, cli


def _client_factory(handler):
    orig = httpx.Client

    def make_client(*a, **k):
        if "transport" in k and k["transport"] is not None:
            return orig(*a, **k)
        return orig(*a, **k, transport=httpx.MockTransport(handler))

    return make_client


def test_apiget_method_header_json(monkeypatch, capsys):
    url = "https://example.test/x"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.headers.get("x-test") == "1"
        payload = json.loads(request.content.decode("utf-8"))
        assert payload == {"a": 1}
        return httpx.Response(200, json={"ok": True}, request=request)

    monkeypatch.setattr(apiget.httpx, "Client", _client_factory(handler))

    rc = cli.main(
        [
            "apiget",
            url,
            "--method",
            "POST",
            "--header",
            "X-Test: 1",
            "--json",
            '{"a": 1}',
            "--expect",
            "dict",
        ]
    )

    out = capsys.readouterr()
    assert rc == 0
    assert out.err.strip() == ""
    assert json.loads(out.out) == {"ok": True}


def test_apiget_data_body(monkeypatch, capsys):
    url = "https://example.test/x"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.content == b"hello"
        return httpx.Response(200, json={"ok": True}, request=request)

    monkeypatch.setattr(apiget.httpx, "Client", _client_factory(handler))

    rc = cli.main(["apiget", url, "--method", "POST", "--data", "hello", "--expect", "dict"])

    out = capsys.readouterr()
    assert rc == 0
    assert out.err.strip() == ""
    assert json.loads(out.out) == {"ok": True}


def test_apiget_out_writes_file(monkeypatch, capsys, tmp_path: Path):
    url = "https://example.test/x"
    out_path = tmp_path / "out.json"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"ok": True}, request=request)

    monkeypatch.setattr(apiget.httpx, "Client", _client_factory(handler))

    rc = cli.main(["apiget", url, "--expect", "dict", "--out", str(out_path)])

    captured = capsys.readouterr()
    assert rc == 0
    assert captured.out.strip() == ""
    assert captured.err.strip() == ""
    assert json.loads(out_path.read_text(encoding="utf-8")) == {"ok": True}
