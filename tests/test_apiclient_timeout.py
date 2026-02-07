import httpx
import pytest

from sdetkit.apiclient import fetch_json_dict, fetch_json_list


def test_fetch_json_dict_passes_timeout_to_client_get():
    seen: list[object] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.extensions.get("timeout"))
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport, base_url="https://example.test") as client:
        out = fetch_json_dict(client, "/x", timeout=0.2)

    assert out == {"ok": True}
    assert seen and seen[0] is not None


def test_fetch_json_list_passes_timeout_to_client_get():
    seen: list[object] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.extensions.get("timeout"))
        return httpx.Response(200, json=[1])

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport, base_url="https://example.test") as client:
        out = fetch_json_list(client, "/x", timeout=0.3)

    assert out == [1]
    assert seen and seen[0] is not None


def test_timeout_none_is_allowed_and_does_not_crash():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport, base_url="https://example.test") as client:
        assert fetch_json_dict(client, "/x", timeout=None) == {"ok": True}


def test_invalid_retries_still_errors_first():
    with pytest.raises(ValueError):
        fetch_json_dict(httpx.Client(), "https://example.test", retries=0)
