"""Shared Azure Function HTTP clients (async + sync)."""

from __future__ import annotations

import asyncio
import atexit
import contextlib
import os
import threading
import weakref
from collections.abc import Awaitable, Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import httpx

from ..http_async import AsyncHttpClient, request_async
from ..http_utils import absolute_url

if TYPE_CHECKING:
    pass

# Track sync clients for cleanup on process exit
_SYNC_CLIENTS: weakref.WeakSet[AzureFunctionSyncClient] = weakref.WeakSet()


def _shutdown_sync_clients() -> None:
    """Clean up all tracked sync clients on process exit."""
    for client in list(_SYNC_CLIENTS):
        with contextlib.suppress(Exception):
            client.close()


atexit.register(_shutdown_sync_clients)


def _merge_headers(defaults: Mapping[str, str], overrides: Mapping[str, str] | None) -> dict[str, str]:
    merged = dict(defaults)
    if overrides:
        merged.update(overrides)
    return merged


@dataclass(frozen=True)
class RequestOptions:
    timeout: float | httpx.Timeout | None = None
    delay: float | None = None
    max_retries: int | None = None
    backoff: float | None = None
    max_backoff: float | None = None


class AzureFunctionAsyncClient:
    """Async HTTP client with retry/backoff tailored for Azure Function APIs."""

    def __init__(
        self,
        base_url: str,
        *,
        api_key: str | None = None,
        timeout: float = 30.0,
        http_client: AsyncHttpClient | None = None,
        default_headers: Mapping[str, str] | None = None,
    ) -> None:
        if not base_url:
            raise ValueError("base_url is required")
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout
        self._client = http_client or AsyncHttpClient()
        self._headers = dict(default_headers or {})

    async def request(
        self,
        method: str,
        path: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        data: Any = None,
        content: Any = None,
        options: RequestOptions | None = None,
    ) -> httpx.Response:
        url = self._url(path)
        merged_headers = _merge_headers(self._headers, headers)
        if self._api_key:
            merged_headers.setdefault("x-functions-key", self._api_key)
        opts = options or RequestOptions()
        timeout = opts.timeout if opts.timeout is not None else self._timeout
        return await request_async(
            method,
            url,
            headers=merged_headers,
            params=params,
            json=json,
            data=data,
            content=content,
            timeout=timeout,
            delay=opts.delay or 0.0,
            max_retries=opts.max_retries if opts.max_retries is not None else 2,
            backoff=opts.backoff if opts.backoff is not None else 1.0,
            max_backoff=opts.max_backoff if opts.max_backoff is not None else 60.0,
            client=self._client,
        )

    async def request_json(self, method: str, path: str, **kwargs: Any) -> Any:
        response = await self.request(method, path, **kwargs)
        if not response.content:
            return {}
        return response.json()

    async def get_json(self, path: str, **kwargs: Any) -> Any:
        return await self.request_json("GET", path, **kwargs)

    async def post_json(self, path: str, *, json: Any, **kwargs: Any) -> Any:
        return await self.request_json("POST", path, json=json, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> None:
        response = await self.request("DELETE", path, **kwargs)
        response.read()

    def _url(self, path: str) -> str:
        return absolute_url(self._base_url, path)

    @classmethod
    def from_env(
        cls,
        *,
        base_url_env: str,
        api_key_env: str | None = None,
        **kwargs: Any,
    ) -> AzureFunctionAsyncClient:
        base_url = os.getenv(base_url_env)
        if not base_url:
            raise RuntimeError(f"{base_url_env} environment variable is required")
        api_key = os.getenv(api_key_env) if api_key_env else None
        return cls(base_url, api_key=api_key, **kwargs)


class AzureFunctionSyncClient:
    """Synchronous wrapper around the async Azure Function client.

    Uses a background daemon thread to run an event loop. The client is
    automatically registered for cleanup on process exit via atexit.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._async_client = AzureFunctionAsyncClient(*args, **kwargs)
        self._loop = asyncio.new_event_loop()
        self._loop_ready = threading.Event()
        self._closed = False
        self._loop_thread = threading.Thread(target=self._run_loop, daemon=True)
        self._loop_thread.start()
        self._loop_ready.wait()
        # Register for cleanup on process exit
        _SYNC_CLIENTS.add(self)

    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        return self._run_async(self._async_client.request(method, path, **kwargs))

    def request_json(self, method: str, path: str, **kwargs: Any) -> Any:
        return self._run_async(self._async_client.request_json(method, path, **kwargs))

    def get_json(self, path: str, **kwargs: Any) -> Any:
        return self.request_json("GET", path, **kwargs)

    def post_json(self, path: str, *, json: Any, **kwargs: Any) -> Any:
        return self.request_json("POST", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> None:
        self._run_async(self._async_client.delete(path, **kwargs))

    def close(self) -> None:
        """Shut down the background event loop."""
        if self._closed:
            return
        self._closed = True
        if self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._loop_thread.is_alive():
            self._loop_thread.join(timeout=2.0)
        if not self._loop.is_closed():
            self._loop.close()

    @classmethod
    def from_env(
        cls,
        *,
        base_url_env: str,
        api_key_env: str | None = None,
        **kwargs: Any,
    ) -> AzureFunctionSyncClient:
        base_url = os.getenv(base_url_env)
        if not base_url:
            raise RuntimeError(f"{base_url_env} environment variable is required")
        api_key = os.getenv(api_key_env) if api_key_env else None
        return cls(base_url, api_key=api_key, **kwargs)

    def _run_async(self, coro: Awaitable[Any]) -> Any:
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)  # type: ignore[arg-type, var-annotated]
        return future.result()

    def _run_loop(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop_ready.set()
        self._loop.run_forever()

    def __del__(self) -> None:
        with contextlib.suppress(Exception):
            self.close()


__all__ = [
    "AzureFunctionAsyncClient",
    "AzureFunctionSyncClient",
    "RequestOptions",
]
