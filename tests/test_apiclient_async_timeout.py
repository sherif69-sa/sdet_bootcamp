import httpx
import pytest

from sdetkit.apiclient import fetch_json_dict_async, fetch_json_list_async


@pytest.mark.asyncio
async def test_fetch_json_dict_async_passes_timeout_to_client_get():
    seen: list[object] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.extensions.get("timeout"))
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="https://example.test") as client:
        out = await fetch_json_dict_async(client, "/x", timeout=0.2)

    assert out == {"ok": True}
    assert seen and seen[0] is not None


@pytest.mark.asyncio
async def test_fetch_json_list_async_passes_timeout_to_client_get():
    seen: list[object] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.extensions.get("timeout"))
        return httpx.Response(200, json=[1])

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="https://example.test") as client:
        out = await fetch_json_list_async(client, "/x", timeout=0.3)

    assert out == [1]
    assert seen and seen[0] is not None
