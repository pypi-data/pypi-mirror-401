"""Regression tests to ensure sync wrappers don't close their event loops."""

from __future__ import annotations

import asyncio
import json
import sys
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from infra_core.asset_client import download_asset, reset_shared_client  # noqa: E402
from infra_core.azure.client import AzureFunctionSyncClient  # noqa: E402


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):  # noqa: N802 - http.server naming
        data = json.dumps({"path": self.path, "ok": True}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args, **kwargs):  # noqa: ARG002 - suppress noisy logs
        pass


@contextmanager
def _run_server() -> str:
    """Start a local HTTP server on an ephemeral port."""
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    host, port = httpd.server_address
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://{host}:{port}"
    try:
        yield base_url
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2.0)


def test_azure_sync_client_reuses_event_loop():
    with _run_server() as base_url:
        client = AzureFunctionSyncClient(base_url)
        try:
            for i in range(5):
                resp = client.get_json(f"/api/ping/{i}")
                assert resp == {"path": f"/api/ping/{i}", "ok": True}
        finally:
            client.close()


def test_asset_sync_helper_reuses_event_loop(tmp_path: Path):
    dest = tmp_path / "payload.json"
    with _run_server() as base_url:
        first = download_asset(f"{base_url}/asset/1", dest)
        second = download_asset(f"{base_url}/asset/1", dest)
    assert first.path == dest
    assert second.path == dest
    assert second.reused is True
    assert dest.read_text()
    # Cleanup shared singleton used by download_asset to avoid leaking across tests.
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(reset_shared_client())
    else:
        # If a loop is already running (unlikely in this test), schedule and wait briefly.
        loop = asyncio.get_running_loop()
        fut = asyncio.run_coroutine_threadsafe(reset_shared_client(), loop)
        fut.result(timeout=2.0)
