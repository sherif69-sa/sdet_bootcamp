from __future__ import annotations

from dataclasses import dataclass

import httpx
import pytest

import sdetkit.apiclient as ap


@dataclass
class StubClient:
    seq: list[object]
    i: int = 0

    def get(self, *_a: object, **_k: object) -> object:
        item = self.seq[self.i]
        self.i += 1
        if isinstance(item, BaseException):
            raise item
        return item


@dataclass
class StubAsyncClient:
    seq: list[object]
    i: int = 0

    async def get(self, *_a: object, **_k: object) -> object:
        item = self.seq[self.i]
        self.i += 1
        if isinstance(item, BaseException):
            raise item
        return item


def _resp(
    url: str, status: int, json_obj: object, headers: dict[str, str] | None = None
) -> httpx.Response:
    req = httpx.Request("GET", url)
    return httpx.Response(status, request=req, json=json_obj, headers=headers or {})


def test_fetch_json_dict_all_none_hits_r_none_continue_and_raises_request_failed_no_cause() -> None:
    c = StubClient([None, None])
    with pytest.raises(RuntimeError, match="request failed") as ei:
        ap.fetch_json_dict(c, "https://example.test/x", retries=2)
    assert ei.value.__cause__ is None


@pytest.mark.asyncio
async def test_fetch_json_dict_async_all_none_raises_request_failed_no_cause() -> None:
    c = StubAsyncClient([None, None])
    with pytest.raises(RuntimeError, match="request failed") as ei:
        await ap.fetch_json_dict_async(c, "https://example.test/x", retries=2)
    assert ei.value.__cause__ is None


def test_fetch_json_list_retries_must_be_ge_1() -> None:
    c = StubClient([])
    with pytest.raises(ValueError, match="retries must be >= 1"):
        ap.fetch_json_list(c, "https://example.test/x", retries=0)


def test_fetch_json_list_timeout_exception_is_wrapped() -> None:
    req = httpx.Request("GET", "https://example.test/t")
    c = StubClient([httpx.ReadTimeout("t", request=req)])
    with pytest.raises(TimeoutError, match="request timed out"):
        ap.fetch_json_list(c, "https://example.test/t", retries=1)


def test_fetch_json_list_request_error_backoff_sleeps_then_success() -> None:
    req = httpx.Request("GET", "https://example.test/r")
    sleep_calls: list[float] = []

    def sleep_fn(d: float) -> None:
        sleep_calls.append(d)

    c = StubClient(
        [
            httpx.ConnectError("c", request=req),
            _resp("https://example.test/r", 200, [1]),
        ]
    )

    out = ap.fetch_json_list(
        c,
        "https://example.test/r",
        retries=2,
        backoff_base=1.0,
        backoff_factor=1.0,
        backoff_jitter=0.0,
        sleep=sleep_fn,
    )
    assert out == [1]
    assert len(sleep_calls) == 1
    assert sleep_calls[0] > 0


def test_fetch_json_list_r_none_is_skipped_then_success() -> None:
    c = StubClient(
        [
            None,
            _resp("https://example.test/n", 200, [2]),
        ]
    )
    out = ap.fetch_json_list(c, "https://example.test/n", retries=2)
    assert out == [2]


def test_fetch_json_list_429_retry_uses_retry_after_and_sleeps_then_success() -> None:
    sleep_calls: list[float] = []

    def sleep_fn(d: float) -> None:
        sleep_calls.append(d)

    c = StubClient(
        [
            _resp("https://example.test/rl", 429, {}, headers={"Retry-After": "1"}),
            _resp("https://example.test/rl", 200, [3]),
        ]
    )

    out = ap.fetch_json_list(
        c,
        "https://example.test/rl",
        retries=2,
        retry_on_429=True,
        backoff_base=1.0,
        backoff_factor=1.0,
        backoff_jitter=0.0,
        sleep=sleep_fn,
    )
    assert out == [3]
    assert len(sleep_calls) == 1
    assert sleep_calls[0] > 0


def test_fetch_json_list_all_none_raises_request_failed_no_cause() -> None:
    c = StubClient([None, None])
    with pytest.raises(RuntimeError, match="request failed") as ei:
        ap.fetch_json_list(c, "https://example.test/z", retries=2)
    assert ei.value.__cause__ is None


@pytest.mark.asyncio
async def test_fetch_json_list_async_request_error_backoff_sleeps_then_success() -> None:
    req = httpx.Request("GET", "https://example.test/ar")
    sleep_calls: list[float] = []

    async def sleep_fn(d: float) -> None:
        sleep_calls.append(d)

    c = StubAsyncClient(
        [
            httpx.ConnectError("c", request=req),
            _resp("https://example.test/ar", 200, [4]),
        ]
    )

    out = await ap.fetch_json_list_async(
        c,
        "https://example.test/ar",
        retries=2,
        backoff_base=1.0,
        backoff_factor=1.0,
        backoff_jitter=0.0,
        sleep=sleep_fn,
    )
    assert out == [4]
    assert len(sleep_calls) == 1
    assert sleep_calls[0] > 0
