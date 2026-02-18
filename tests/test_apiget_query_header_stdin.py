from __future__ import annotations

import io
import json
from pathlib import Path

import httpx

_REAL_HTTPX_CLIENT = httpx.Client


def _client_factory(handler):
    def _mk(*a, **k):
        return _REAL_HTTPX_CLIENT(transport=httpx.MockTransport(handler))

    return _mk


def test_apiget_query_appends_to_url(monkeypatch, capsys):
    from sdetkit import apiget, cli

    url = "https://example.test/x?base=1"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params.get("base") == "1"
        assert request.url.params.get("a") == "1"
        assert request.url.params.get("b") == "two"
        return httpx.Response(200, json={"ok": True}, request=request)

    monkeypatch.setattr(apiget.httpx, "Client", _client_factory(handler))

    rc = cli.main(["apiget", url, "--query", "a=1", "--query", "b=two", "--expect", "dict"])
    out = capsys.readouterr()
    assert rc == 0
    assert json.loads(out.out) == {"ok": True}
    assert out.err.strip() == ""


def test_apiget_header_at_file(monkeypatch, capsys, tmp_path: Path):
    from sdetkit import apiget, cli

    url = "https://example.test/x"
    hf = tmp_path / "headers.txt"
    hf.write_text(
        "X-Test: 1\nX-Other: two\n\n# ignored\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("x-test") == "1"
        assert request.headers.get("x-other") == "two"
        return httpx.Response(200, json={"ok": True}, request=request)

    monkeypatch.setattr(apiget.httpx, "Client", _client_factory(handler))

    rc = cli.main(["apiget", url, "--header", "@headers.txt", "--expect", "dict"])
    out = capsys.readouterr()
    assert rc == 0
    assert json.loads(out.out) == {"ok": True}
    assert out.err.strip() == ""


def test_apiget_data_stdin_at_dash(monkeypatch, capsys):
    from sdetkit import apiget, cli

    url = "https://example.test/x"
    monkeypatch.setattr(apiget.sys, "stdin", io.StringIO("hello"))

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.content == b"hello"
        return httpx.Response(200, json={"ok": True}, request=request)

    monkeypatch.setattr(apiget.httpx, "Client", _client_factory(handler))

    rc = cli.main(["apiget", url, "--method", "POST", "--data", "@-", "--expect", "dict"])
    out = capsys.readouterr()
    assert rc == 0
    assert json.loads(out.out) == {"ok": True}
    assert out.err.strip() == ""


def test_apiget_json_stdin_at_dash(monkeypatch, capsys):
    from sdetkit import apiget, cli

    url = "https://example.test/x"
    monkeypatch.setattr(apiget.sys, "stdin", io.StringIO('{"a": 1}'))

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload == {"a": 1}
        return httpx.Response(200, json={"ok": True}, request=request)

    monkeypatch.setattr(apiget.httpx, "Client", _client_factory(handler))

    rc = cli.main(["apiget", url, "--method", "POST", "--json", "@-", "--expect", "dict"])
    out = capsys.readouterr()
    assert rc == 0
    assert json.loads(out.out) == {"ok": True}
    assert out.err.strip() == ""
