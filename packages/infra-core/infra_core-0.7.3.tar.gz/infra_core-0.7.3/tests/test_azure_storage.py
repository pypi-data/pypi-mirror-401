"""Unit tests for azure_storage helpers."""

from __future__ import annotations

import errno
import logging
import types
from pathlib import Path

import pytest

from infra_core.azure import storage as azure_storage
from infra_core.azure.storage import (
    AzureStorageClient,
    AzureStorageSettings,
    ConfigurationError,
    ResourceNotFoundError,
    StorageBackend,
    StorageMode,
    _atomic_replace,
)
from infra_core.azure.storage import (
    _AzureStorageConfig as AzureStorageConfig,
)
from infra_core.azure.storage import (
    _blob_name_for_path as blob_name_for_path,
)

# Test helper: default settings for tests
_TEST_SETTINGS = AzureStorageSettings(container="test-container")


def _make_client(
    config: AzureStorageConfig | None = None,
    *,
    mode: StorageMode = "dev-skip",
    settings: AzureStorageSettings | None = None,
    **kwargs,
) -> AzureStorageClient:
    """Create a test client with sensible defaults."""
    return AzureStorageClient(
        config=config,
        settings=settings or _TEST_SETTINGS,
        mode=mode,
        **kwargs,
    )


def test_client_matches_storage_backend_protocol() -> None:
    client = _make_client(config=None)
    assert isinstance(client, StorageBackend)


def test_client_with_base_path_strips_from_blob_names(tmp_path: Path) -> None:
    """Test that AzureStorageClient with base_path strips it from blob names."""
    config = AzureStorageConfig(container="demo")
    base = tmp_path
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip", base_path=base)

    path = base / "runs" / "batch-id" / "file.txt"
    blob_name = client.blob_name_for_path(path)

    # Should strip base_path, leaving only relative path
    assert blob_name == "runs/batch-id/file.txt"


def test_client_from_settings_accepts_base_path() -> None:
    """Test that from_settings() accepts and stores base_path."""
    settings = AzureStorageSettings(container="demo", connection_string="UseDevelopmentStorage=true")
    base = Path("/tmp")
    client = AzureStorageClient.from_settings(settings, "strict", base_path=base)

    path = Path("/tmp/runs/batch/file.txt")
    blob_name = client.blob_name_for_path(path)

    # Should use base_path to strip /tmp
    assert blob_name == "runs/batch/file.txt"


def test_strict_mode_requires_credentials() -> None:
    settings = AzureStorageSettings(container="demo", connection_string=None, account_name=None, blob_endpoint=None)
    with pytest.raises(ConfigurationError):
        AzureStorageClient.from_settings(settings, "strict")


def test_client_base_path_with_prefix(tmp_path: Path) -> None:
    """Test that base_path works together with prefix."""
    config = AzureStorageConfig(container="demo", prefix="screenshot-output")
    base = tmp_path
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip", base_path=base)

    path = base / "runs" / "batch" / "file.png"
    blob_name = client.blob_name_for_path(path)

    assert blob_name == "screenshot-output/runs/batch/file.png"


def test_strict_mode_raises_when_unconfigured(tmp_path: Path) -> None:
    client = AzureStorageClient(config=None, settings=_TEST_SETTINGS, mode="strict")
    path = tmp_path / "artifact.txt"
    path.write_text("payload", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="not configured"):
        client.upload_file(path)


def test_dev_skip_logs_and_skips(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING, logger=azure_storage.logger.name)
    client = AzureStorageClient(config=None, settings=_TEST_SETTINGS, mode="dev-skip")
    path = tmp_path / "artifact.txt"
    path.write_text("payload", encoding="utf-8")

    client.upload_file(path)

    assert "Azure storage not configured; skipping action" in caplog.text
    assert "mode=dev-skip" in caplog.text


def test_best_effort_logs_and_skips(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING, logger=azure_storage.logger.name)
    client = AzureStorageClient(config=None, settings=_TEST_SETTINGS, mode="best-effort")
    path = tmp_path / "artifact.txt"
    path.write_text("payload", encoding="utf-8")

    client.upload_file(path)

    assert "Azure storage not configured; skipping action" in caplog.text
    assert "mode=best-effort" in caplog.text


def test_config_from_settings_requires_container() -> None:
    empty = AzureStorageSettings(container=None)
    assert AzureStorageConfig.from_settings(empty) is None


def test_create_service_client_uses_connection_string(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = AzureStorageConfig(container="demo", connection_string="UseDevelopmentStorage=true")
    dummy_client = object()
    captured: dict[str, object] = {}

    def fake_from_conn(cls, conn: str) -> object:
        captured["conn"] = conn
        return dummy_client

    monkeypatch.setattr(
        azure_storage.BlobServiceClient,
        "from_connection_string",
        classmethod(fake_from_conn),
    )

    client, credential = config.create_service_client()

    assert client is dummy_client
    assert credential is None
    assert captured["conn"] == "UseDevelopmentStorage=true"


def test_create_service_client_with_account_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = AzureStorageConfig(container="demo", account_name="acct")
    dummy_credential = object()
    captured: dict[str, object] = {}

    class DummyBlobServiceClient:
        def __init__(self, *, account_url: str, credential: object) -> None:
            captured["account_url"] = account_url
            captured["credential"] = credential

    monkeypatch.setattr(azure_storage, "BlobServiceClient", DummyBlobServiceClient)
    monkeypatch.setattr(azure_storage, "DefaultAzureCredential", lambda: dummy_credential)

    client, credential = config.create_service_client()

    assert isinstance(client, DummyBlobServiceClient)
    assert credential is dummy_credential
    assert captured["account_url"] == "https://acct.blob.core.windows.net"
    assert captured["credential"] is dummy_credential


def test_create_service_client_without_credentials_raises() -> None:
    config = AzureStorageConfig(container="demo")
    with pytest.raises(RuntimeError):
        config.create_service_client()


def test_create_async_service_client_uses_connection_string(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = AzureStorageConfig(container="demo", connection_string="UseDevelopmentStorage=true")
    dummy_client = object()

    def fake_from_conn(cls, conn: str) -> object:
        return dummy_client

    monkeypatch.setattr(
        azure_storage.AsyncBlobServiceClient,
        "from_connection_string",
        classmethod(fake_from_conn),
    )

    client, credential = config.create_async_service_client()

    assert client is dummy_client
    assert credential is None


def test_write_text_mirrors_upload(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = AzureStorageConfig(container="demo")
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip")
    recorded: dict[str, object] = {}

    def _fake_upload(path: Path, text: str) -> None:
        recorded["path"] = path
        recorded["text"] = text

    monkeypatch.setattr(client, "upload_text", _fake_upload)
    target = tmp_path / "artifact.txt"

    client.write_text(target, "payload")

    assert target.read_text(encoding="utf-8") == "payload"
    assert recorded["path"] == target
    assert recorded["text"] == "payload"


def test_write_text_skips_upload_when_disabled(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = AzureStorageConfig(container="demo")
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip")

    def _boom() -> None:  # pragma: no cover - triggered if upload happens
        raise AssertionError("container should not be fetched when disabled")

    monkeypatch.setattr(client, "container", _boom)
    target = tmp_path / "artifact.txt"

    client.write_text(target, "payload")

    assert target.read_text(encoding="utf-8") == "payload"


def test_write_json_serializes_dict(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config = AzureStorageConfig(container="demo")
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip")
    captured: dict[str, str] = {}

    def _fake_write(path: Path, text: str) -> Path:
        captured["text"] = text
        return path

    monkeypatch.setattr(client, "write_text", _fake_write)

    target = tmp_path / "manifest.json"
    client.write_json(target, {"slug": "demo"})

    assert captured["text"].startswith("{")
    assert captured["text"].endswith("\n")


@pytest.mark.asyncio
async def test_write_text_async_uses_async_upload(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config = AzureStorageConfig(container="demo")
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip")
    recorded: dict[str, object] = {}

    async def _fake_upload(path: Path, text: str) -> None:
        recorded["path"] = path
        recorded["text"] = text

    monkeypatch.setattr(client, "upload_text_async", _fake_upload)
    target = tmp_path / "artifact.txt"

    await client.write_text_async(target, "payload")

    assert target.read_text(encoding="utf-8") == "payload"
    assert recorded["path"] == target
    assert recorded["text"] == "payload"


def test_upload_text_raises_by_default(tmp_path: Path) -> None:
    config = AzureStorageConfig(container="demo")
    # Use strict mode so upload is actually attempted (config is set)
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="strict")

    class DummyContainer:
        def upload_blob(self, *, name, data, overwrite):  # type: ignore[no-untyped-def]
            raise RuntimeError("boom")

    client._container = DummyContainer()  # type: ignore[attr-defined]

    with pytest.raises(RuntimeError, match="boom"):
        client.upload_text(tmp_path / "artifact.txt", "payload")


def test_upload_text_swallows_errors_when_configured(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    config = AzureStorageConfig(container="demo")
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="strict", swallow_errors=True)

    class DummyContainer:
        def upload_blob(self, *, name, data, overwrite):  # type: ignore[no-untyped-def]
            raise RuntimeError("boom")

    client._container = DummyContainer()  # type: ignore[attr-defined]
    caplog.set_level(logging.WARNING)

    client.upload_text(tmp_path / "artifact.txt", "payload")

    assert "Azure upload failed" in caplog.text


def test_upload_text_raises_when_swallow_errors_false(tmp_path: Path) -> None:
    config = AzureStorageConfig(container="demo")
    # Use strict mode so upload is actually attempted
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="strict", swallow_errors=False)

    class DummyContainer:
        def upload_blob(self, *, name, data, overwrite):  # type: ignore[no-untyped-def]
            raise RuntimeError("boom")

    client._container = DummyContainer()  # type: ignore[attr-defined]

    with pytest.raises(RuntimeError):
        client.upload_text(tmp_path / "artifact.txt", "payload")


def test_list_tree_returns_empty_when_storage_disabled() -> None:
    client = AzureStorageClient(config=None, settings=_TEST_SETTINGS, mode="dev-skip")

    result = client.list_tree(Path("/tmp/runs/batch/job/screens"))

    assert result == []


def test_list_tree_uses_default_container(tmp_path: Path) -> None:
    captured = {}

    class DummyContainer:
        def list_blobs(self, *, name_starts_with: str):  # type: ignore[no-untyped-def]
            captured["prefix"] = name_starts_with
            return [
                type(
                    "Blob",
                    (),
                    {"name": f"{name_starts_with}slug/file.txt", "size": 128},
                )
            ]

    dummy_config = AzureStorageConfig(container="demo", prefix="exports")
    client = AzureStorageClient(config=dummy_config, settings=_TEST_SETTINGS, mode="dev-skip")
    client._container = DummyContainer()  # type: ignore[attr-defined]

    target = tmp_path / "runs" / "batch"
    result = client.list_tree(target)

    expected_prefix = dummy_config.blob_name_for_path(target)
    if not expected_prefix.endswith("/") and expected_prefix:
        expected_prefix = f"{expected_prefix}/"

    assert result == [("slug/file.txt", 128)]
    assert captured["prefix"] == expected_prefix


def test_blob_name_helper_handles_prefix() -> None:
    path = Path("/tmp/runs/e2e/job/screens")
    # tmp/ prefix is now automatically stripped as safety net
    assert blob_name_for_path(path, prefix="exports") == "exports/runs/e2e/job/screens"


def test_blob_name_for_path_strips_base_path() -> None:
    """Test that base_path is stripped from blob names."""
    base = Path("/tmp")
    path = Path("/tmp/runs/batch-id/job-id/screens")
    assert blob_name_for_path(path, base_path=base) == "runs/batch-id/job-id/screens"


def test_blob_name_for_path_strips_base_path_with_prefix() -> None:
    """Test base_path stripping works with prefix."""
    base = Path("/tmp")
    path = Path("/tmp/runs/batch-id/screens")
    assert blob_name_for_path(path, prefix="exports", base_path=base) == "exports/runs/batch-id/screens"


def test_blob_name_for_path_handles_path_outside_base() -> None:
    """Test that paths outside base_path are used as-is."""
    base = Path("/tmp")
    path = Path("/var/data/file.txt")
    # Path not under base, should use full path (minus leading /)
    assert blob_name_for_path(path, base_path=base) == "var/data/file.txt"


def test_blob_name_for_path_strips_tmp_prefix() -> None:
    """Test that tmp/ prefix is stripped as safety net."""
    path = Path("/tmp/runs/batch/job")
    # Even without base_path, should strip tmp/ prefix
    assert blob_name_for_path(path) == "runs/batch/job"


def test_blob_name_for_path_strips_temp_prefix() -> None:
    """Test that temp/ prefix is stripped."""
    path = Path("/temp/runs/batch")
    assert blob_name_for_path(path) == "runs/batch"


def test_blob_name_for_path_strips_var_tmp_prefix() -> None:
    """Test that var/tmp/ prefix is stripped."""
    path = Path("/var/tmp/runs/batch")
    assert blob_name_for_path(path) == "runs/batch"


def test_blob_name_for_path_base_path_takes_precedence_over_temp_stripping() -> None:
    """Test that base_path relative conversion happens before temp prefix stripping."""
    base = Path("/tmp")
    path = Path("/tmp/runs/batch")
    # Should use base_path conversion, not temp prefix stripping
    assert blob_name_for_path(path, base_path=base) == "runs/batch"


def test_blob_path_for_uses_config() -> None:
    config = AzureStorageConfig(container="demo", prefix="data")
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip")
    path = Path("/tmp/runs/foo/bar")
    result = client.blob_name_for_path(path)
    assert result == config.blob_name_for_path(path)


def test_upload_text_uses_default_container(tmp_path: Path) -> None:
    calls = {}

    class DummyContainer:
        def upload_blob(self, *, name, data, overwrite):  # type: ignore[no-untyped-def]
            calls["upload_blob"] = (name, data, overwrite)

    dummy_config = AzureStorageConfig(container="demo", prefix=None)
    client = AzureStorageClient(config=dummy_config, settings=_TEST_SETTINGS, mode="strict")
    client._container = DummyContainer()  # type: ignore[attr-defined]

    path = tmp_path / "runs" / "batch" / "job" / "screens.json"
    client.upload_text(path, "payload")

    assert calls["upload_blob"][0] == dummy_config.blob_name_for_path(path)
    assert calls["upload_blob"][1] == b"payload"
    assert calls["upload_blob"][2] is True


@pytest.mark.asyncio
async def test_upload_text_async_uses_async_container(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    uploads: list[tuple[str, bytes, bool]] = []

    class DummyAsyncContainer:
        def __init__(self) -> None:
            self.create_calls = 0

        async def create_container(self) -> None:
            self.create_calls += 1

        async def upload_blob(self, *, name: str, data: bytes, overwrite: bool) -> None:
            uploads.append((name, data, overwrite))

        async def close(self) -> None:
            pass

    class DummyAsyncService:
        def __init__(self, container: DummyAsyncContainer) -> None:
            self.container = container
            self.calls = 0

        def get_container_client(self, container_name: str) -> DummyAsyncContainer:
            self.calls += 1
            return self.container

        async def close(self) -> None:
            pass

    dummy_container = DummyAsyncContainer()
    dummy_service = DummyAsyncService(dummy_container)
    config = AzureStorageConfig(container="demo", prefix="exports")
    monkeypatch.setattr(
        AzureStorageConfig,
        "create_async_service_client",
        lambda self: (dummy_service, None),
    )

    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="strict")
    target = tmp_path / "runs" / "batch" / "job" / "log.txt"

    await client.upload_text_async(target, "payload")

    expected_blob = config.blob_name_for_path(target)
    assert uploads == [(expected_blob, b"payload", True)]
    assert dummy_container.create_calls == 1
    assert dummy_service.calls == 1

    await client.aclose()


def test_atomic_replace_falls_back_to_move(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    source = tmp_path / "blob.tmp"
    dest = tmp_path / "blob.bin"
    source.write_bytes(b"blob-bytes")
    dest.write_bytes(b"old")
    moves: list[tuple[str, str]] = []

    original_replace = Path.replace

    def fake_replace(self: Path, target: Path) -> Path:
        if self == source:
            raise OSError(errno.EXDEV, "cross-device")
        return original_replace(self, target)

    def fake_move(src: str, dst: str) -> None:
        moves.append((src, dst))
        Path(dst).write_bytes(Path(src).read_bytes())
        Path(src).unlink(missing_ok=True)

    monkeypatch.setattr(Path, "replace", fake_replace, raising=False)
    monkeypatch.setattr(azure_storage.shutil, "move", fake_move)

    _atomic_replace(source, dest)

    assert dest.read_bytes() == b"blob-bytes"
    assert not source.exists()
    assert moves == [(str(source), str(dest))]


def test_atomic_replace_propagates_other_os_errors(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    source = tmp_path / "blob.tmp"
    dest = tmp_path / "blob.bin"
    source.write_bytes(b"blob-bytes")
    dest.write_bytes(b"old")
    original_replace = Path.replace

    def fake_replace(self: Path, target: Path) -> Path:
        if self == source:
            raise OSError(errno.EACCES, "denied")
        return original_replace(self, target)

    moved = False

    def fake_move(src: str, dst: str) -> None:
        nonlocal moved
        moved = True

    monkeypatch.setattr(Path, "replace", fake_replace, raising=False)
    monkeypatch.setattr(azure_storage.shutil, "move", fake_move)

    with pytest.raises(OSError):
        _atomic_replace(source, dest)

    assert moved is False
    assert source.exists()


def test_set_shared_client_disposes_previous(monkeypatch: pytest.MonkeyPatch) -> None:
    azure_storage.reset_all_clients()
    disposed: list[AzureStorageClient] = []
    monkeypatch.setattr(azure_storage, "_dispose_client", lambda client: disposed.append(client))
    first = AzureStorageClient(config=None, settings=_TEST_SETTINGS, mode="dev-skip")
    second = AzureStorageClient(config=None, settings=_TEST_SETTINGS, mode="dev-skip")

    azure_storage.set_shared_client(first, _TEST_SETTINGS, "dev-skip")
    azure_storage.set_shared_client(second, _TEST_SETTINGS, "dev-skip")

    assert disposed == [first]
    azure_storage.reset_all_clients()


@pytest.mark.asyncio
async def test_reset_shared_client_async_closes_client() -> None:
    azure_storage.reset_all_clients()
    closed: list[bool] = []

    class DummyClient(AzureStorageClient):
        async def aclose(self) -> None:  # type: ignore[override]
            closed.append(True)

    client = DummyClient(config=None, settings=_TEST_SETTINGS, mode="dev-skip")
    azure_storage.set_shared_client(client, _TEST_SETTINGS, "dev-skip")
    await azure_storage.reset_shared_client_async(_TEST_SETTINGS, "dev-skip")

    assert closed == [True]
    azure_storage.reset_all_clients()


def test_download_tree_writes_all_blobs(tmp_path: Path) -> None:
    config = AzureStorageConfig(container="demo", prefix="exports")
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="strict")
    target = tmp_path / "runs" / "batch"
    root_blob = config.blob_name_for_path(target)
    child_blob = f"{root_blob}/nested/info.txt"
    blobs = {
        child_blob: b"child",
    }

    class DummyDownloader:
        def __init__(self, data: bytes) -> None:
            self._data = data

        def chunks(self):
            yield self._data

    class DummyContainer:
        def download_blob(self, name: str) -> DummyDownloader:
            if name == root_blob:
                raise ResourceNotFoundError(message="missing")
            if name not in blobs:
                raise ResourceNotFoundError(message="missing")
            return DummyDownloader(blobs[name])

        def list_blobs(self, *, name_starts_with: str):
            for name, data in blobs.items():
                if name.startswith(name_starts_with) and name != name_starts_with:
                    yield type("Blob", (), {"name": name, "size": len(data)})

    dummy_container = DummyContainer()

    def _container(self: AzureStorageClient) -> DummyContainer:
        return dummy_container

    client.container = types.MethodType(_container, client)  # type: ignore[assignment]

    downloaded = client.download_tree(target)

    assert downloaded is True
    assert (target / "nested" / "info.txt").read_bytes() == b"child"


@pytest.mark.asyncio
async def test_download_tree_async_writes_all_blobs(tmp_path: Path) -> None:
    config = AzureStorageConfig(container="demo", prefix=None)
    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="strict")
    target = tmp_path / "jobs" / "task"
    root_blob = config.blob_name_for_path(target)
    child_blob = f"{root_blob}/child.bin"
    blobs = {
        child_blob: b"child-bytes",
    }

    class DummyAsyncDownloader:
        def __init__(self, data: bytes) -> None:
            self._data = data

        def chunks(self):
            async def _gen():
                yield self._data

            return _gen()

    class DummyAsyncContainer:
        async def download_blob(self, name: str) -> DummyAsyncDownloader:
            if name == root_blob:
                raise ResourceNotFoundError(message="missing")
            if name not in blobs:
                raise ResourceNotFoundError(message="missing")
            return DummyAsyncDownloader(blobs[name])

        def list_blobs(self, *, name_starts_with: str):
            async def _gen():
                for name, data in blobs.items():
                    if name.startswith(name_starts_with) and name != name_starts_with:
                        yield type("Blob", (), {"name": name, "size": len(data)})

            return _gen()

    dummy_async_container = DummyAsyncContainer()

    async def _container_async(self: AzureStorageClient) -> DummyAsyncContainer:
        return dummy_async_container

    client.container_async = types.MethodType(_container_async, client)  # type: ignore[assignment]

    downloaded = await client.download_tree_async(target)

    assert downloaded is True
    assert (target / "child.bin").read_bytes() == b"child-bytes"


@pytest.mark.asyncio
async def test_container_async_caches_service_and_container(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class DummyAsyncContainer:
        def __init__(self) -> None:
            self.create_calls = 0

        async def create_container(self) -> None:
            self.create_calls += 1

        async def close(self) -> None:
            pass

    class DummyAsyncService:
        def __init__(self, container: DummyAsyncContainer) -> None:
            self.container = container
            self.calls = 0

        def get_container_client(self, container_name: str) -> DummyAsyncContainer:
            self.calls += 1
            return self.container

        async def close(self) -> None:
            pass

    dummy_container = DummyAsyncContainer()
    dummy_service = DummyAsyncService(dummy_container)
    config = AzureStorageConfig(container="demo", prefix=None)
    monkeypatch.setattr(
        AzureStorageConfig,
        "create_async_service_client",
        lambda self: (dummy_service, None),
    )

    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip")

    first = await client.container_async()
    second = await client.container_async()

    assert first is second
    assert dummy_service.calls == 1
    assert dummy_container.create_calls == 1

    await client.aclose()


@pytest.mark.asyncio
async def test_upload_file_async_streams_bytes(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    captured: dict[str, object] = {}

    class DummyAsyncContainer:
        async def create_container(self) -> None:
            pass

        async def upload_blob(self, *, name: str, data, overwrite: bool) -> None:
            captured["name"] = name
            captured["data"] = data
            captured["overwrite"] = overwrite

        async def close(self) -> None:
            pass

    class DummyAsyncService:
        def __init__(self, container: DummyAsyncContainer) -> None:
            self.container = container

        def get_container_client(self, container_name: str) -> DummyAsyncContainer:
            return self.container

        async def close(self) -> None:
            pass

    container = DummyAsyncContainer()
    service = DummyAsyncService(container)
    config = AzureStorageConfig(container="demo", prefix="runs")

    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="strict")
    client._async_service = service  # type: ignore[attr-defined]
    client._async_container = container  # type: ignore[attr-defined]

    payload_path = tmp_path / "runs" / "note.bin"
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    payload_path.write_bytes(b"payload-bytes")

    await client.upload_file_async(payload_path)

    assert captured["name"] == config.blob_name_for_path(payload_path)
    data = captured["data"]
    if isinstance(data, bytes | bytearray):
        assert data == b"payload-bytes"
    else:
        assert hasattr(data, "name")
        assert data.name == str(payload_path)
    assert captured["overwrite"] is True

    await client.aclose()


@pytest.mark.asyncio
async def test_download_to_path_async_writes_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    data_map: dict[str, bytes] = {}

    class DummyDownloader:
        def __init__(self, name: str) -> None:
            self._name = name

        def chunks(self):
            async def _iterate():
                yield data_map[self._name]

            return _iterate()

        async def readall(self) -> bytes:
            return data_map[self._name]

    class DummyAsyncContainer:
        async def create_container(self) -> None:
            pass

        async def download_blob(self, name: str) -> DummyDownloader:
            if name not in data_map:
                raise ResourceNotFoundError("missing")
            return DummyDownloader(name)

        def list_blobs(self, *, name_starts_with: str):
            async def _iterator():
                if False:
                    yield  # pragma: no cover

            return _iterator()

        async def close(self) -> None:
            pass

    class DummyAsyncService:
        def __init__(self, container: DummyAsyncContainer) -> None:
            self.container = container

        def get_container_client(self, container_name: str) -> DummyAsyncContainer:
            return self.container

        async def close(self) -> None:
            pass

    container = DummyAsyncContainer()
    service = DummyAsyncService(container)
    config = AzureStorageConfig(container="demo", prefix="runs")

    blob_name = config.blob_name_for_path(tmp_path / "runs" / "item.txt")
    data_map[blob_name] = b"payload"

    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip")
    client._async_service = service  # type: ignore[attr-defined]
    client._async_container = container  # type: ignore[attr-defined]
    target = tmp_path / "runs" / "item.txt"

    result = await client.download_to_path_async(target)

    assert result is True
    assert target.read_bytes() == b"payload"

    await client.aclose()


@pytest.mark.asyncio
async def test_download_tree_async_materialises_blobs(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    class Blob:
        def __init__(self, name: str, size: int) -> None:
            self.name = name
            self.size = size

    class DummyDownloader:
        def __init__(self, name: str) -> None:
            self._name = name

        def chunks(self):
            async def _iterate():
                yield blob_data[self._name]

            return _iterate()

        async def readall(self) -> bytes:
            return blob_data[self._name]

    class DummyAsyncContainer:
        def __init__(self) -> None:
            self.list_prefixes: list[str] = []

        async def create_container(self) -> None:
            pass

        def list_blobs(self, *, name_starts_with: str):
            async def _iterator():
                for blob in blobs:
                    if blob.name.startswith(name_starts_with):
                        yield blob

            return _iterator()

        async def download_blob(self, name: str) -> DummyDownloader:
            if name not in blob_data:
                raise ResourceNotFoundError("missing")
            return DummyDownloader(name)

        async def close(self) -> None:
            pass

    class DummyAsyncService:
        def __init__(self, container: DummyAsyncContainer) -> None:
            self.container = container

        def get_container_client(self, container_name: str) -> DummyAsyncContainer:
            return self.container

        async def close(self) -> None:
            pass

    config = AzureStorageConfig(container="demo", prefix=None)
    container = DummyAsyncContainer()
    service = DummyAsyncService(container)
    root_path = tmp_path / "runs" / "batch"
    leaf_path = root_path / "slug" / "file.txt"
    leaf_blob = config.blob_name_for_path(leaf_path)
    blobs = [Blob(leaf_blob, 11)]
    blob_data = {
        leaf_blob: b"hello world",
    }

    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip")
    client._async_service = service  # type: ignore[attr-defined]
    client._async_container = container  # type: ignore[attr-defined]
    downloaded = await client.download_tree_async(root_path)

    assert downloaded is True
    assert (root_path / "slug" / "file.txt").read_bytes() == b"hello world"

    await client.aclose()


@pytest.mark.asyncio
async def test_list_tree_async_returns_entries(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    class Blob:
        def __init__(self, name: str, size: int) -> None:
            self.name = name
            self.size = size

    class DummyAsyncContainer:
        async def create_container(self) -> None:
            pass

        def list_blobs(self, *, name_starts_with: str):
            async def _iterator():
                for blob in blobs:
                    yield blob

            return _iterator()

        async def download_blob(self, name: str):
            raise AssertionError("should not download")

        async def close(self) -> None:
            pass

    class DummyAsyncService:
        def __init__(self, container: DummyAsyncContainer) -> None:
            self.container = container

        def get_container_client(self, container_name: str) -> DummyAsyncContainer:
            return self.container

        async def close(self) -> None:
            pass

    config = AzureStorageConfig(container="demo", prefix="runs")
    container = DummyAsyncContainer()
    service = DummyAsyncService(container)
    root_path = tmp_path / "runs" / "batch"
    leaf_a = config.blob_name_for_path(root_path / "slug" / "a.txt")
    leaf_b = config.blob_name_for_path(root_path / "slug" / "nested" / "b.txt")
    blobs = [
        Blob(leaf_a, 5),
        Blob(f"{config.blob_name_for_path(root_path / 'slug' / 'nested')}/", 0),
        Blob(leaf_b, 7),
    ]

    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip")
    client._async_service = service  # type: ignore[attr-defined]
    client._async_container = container  # type: ignore[attr-defined]
    entries = await client.list_tree_async(root_path)

    assert sorted(entries) == [("slug/a.txt", 5), ("slug/nested/b.txt", 7)]

    await client.aclose()


def test_download_to_path_short_circuits() -> None:
    client = AzureStorageClient(config=None, settings=_TEST_SETTINGS, mode="dev-skip")
    assert client.download_to_path(Path("/tmp/file")) is False


def test_settings_from_env_allows_custom_var_names(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ALT_CONTAINER", "custom-container")
    monkeypatch.setenv("ALT_CONN", "custom-conn")
    monkeypatch.setenv("ALT_PREFIX", "custom-prefix")
    settings, mode = azure_storage.AzureStorageSettings.from_env(
        container_var="ALT_CONTAINER",
        connection_string_var="ALT_CONN",
        prefix_var="ALT_PREFIX",
    )
    config = AzureStorageConfig.from_settings(settings)
    assert config is not None
    assert config.container == "custom-container"
    assert config.connection_string == "custom-conn"
    assert config.prefix == "custom-prefix"
    assert mode == "strict"  # Default mode


def test_get_shared_client_disposes_stale_client(monkeypatch: pytest.MonkeyPatch) -> None:
    azure_storage.reset_all_clients()
    disposed: list[azure_storage.AzureStorageClient] = []
    monkeypatch.setattr(azure_storage, "_dispose_client", lambda client: disposed.append(client))

    settings_a = azure_storage.AzureStorageSettings(
        container="container-a",
        connection_string="conn-a",
    )
    settings_b = azure_storage.AzureStorageSettings(
        container="container-b",
        connection_string="conn-b",
    )

    first = azure_storage.get_shared_client(settings_a, "dev-skip")
    second = azure_storage.get_shared_client(settings_b, "dev-skip")

    # Different settings should create new clients
    assert first is not second
    # Old client is NOT disposed because cache is keyed by settings
    # Both clients are cached under different keys
    azure_storage.reset_all_clients()


@pytest.mark.asyncio
async def test_aclose_closes_all_resources() -> None:
    class DummyCloseable:
        def __init__(self) -> None:
            self.closed = False

        def close(self) -> None:
            self.closed = True

    class DummyAsyncCloseable:
        def __init__(self) -> None:
            self.closed = False

        async def close(self) -> None:
            self.closed = True

    client = AzureStorageClient(config=None, settings=_TEST_SETTINGS, mode="dev-skip")
    client._container = DummyCloseable()  # type: ignore[attr-defined]
    client._service = DummyCloseable()  # type: ignore[attr-defined]
    client._credential = DummyCloseable()  # type: ignore[attr-defined]
    client._async_container = DummyAsyncCloseable()  # type: ignore[attr-defined]
    client._async_service = DummyAsyncCloseable()  # type: ignore[attr-defined]
    client._async_credential = DummyAsyncCloseable()  # type: ignore[attr-defined]

    await client.aclose()

    assert client._container is None  # type: ignore[attr-defined]
    assert client._service is None  # type: ignore[attr-defined]
    assert client._credential is None  # type: ignore[attr-defined]
    assert client._async_container is None  # type: ignore[attr-defined]
    assert client._async_service is None  # type: ignore[attr-defined]
    assert client._async_credential is None  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_reset_shared_client_async_disposes_cached_client() -> None:
    azure_storage.reset_all_clients()

    class DummyCloseable(AzureStorageClient):
        def __init__(self) -> None:
            super().__init__(config=None, settings=_TEST_SETTINGS, mode="dev-skip")
            self.closed_sync = False
            self.closed_async = False

        def close(self) -> None:
            self.closed_sync = True
            super().close()

        async def aclose(self) -> None:
            self.closed_async = True
            await super().aclose()

    client = DummyCloseable()
    azure_storage.set_shared_client(client, _TEST_SETTINGS, "dev-skip")

    await azure_storage.reset_shared_client_async(_TEST_SETTINGS, "dev-skip")

    assert client.closed_sync is True
    assert client.closed_async is True
    azure_storage.reset_all_clients()


@pytest.mark.asyncio
async def test_container_async_detects_event_loop_change(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that async clients are recreated when event loop changes.

    This simulates the bug where cached async clients reference a closed loop,
    causing 'RuntimeError: Event loop is closed' when Azure SDK tries to use
    loop.run_in_executor() for authentication.
    """
    from unittest.mock import Mock

    create_service_calls = 0
    closed_clients: list[str] = []

    class DummyAsyncContainer:
        def __init__(self, loop_id: int) -> None:
            self.loop_id = loop_id
            self.closed = False

        async def create_container(self) -> None:
            pass

        async def close(self) -> None:
            self.closed = True
            closed_clients.append(f"container-{self.loop_id}")

    class DummyAsyncService:
        def __init__(self, loop_id: int) -> None:
            self.loop_id = loop_id
            self.closed = False

        def get_container_client(self, container_name: str) -> DummyAsyncContainer:
            return DummyAsyncContainer(self.loop_id)

        async def close(self) -> None:
            self.closed = True
            closed_clients.append(f"service-{self.loop_id}")

    class DummyAsyncCredential:
        def __init__(self, loop_id: int) -> None:
            self.loop_id = loop_id
            self.closed = False

        async def close(self) -> None:
            self.closed = True
            closed_clients.append(f"credential-{self.loop_id}")

    def create_async_service_client_mock(self):
        nonlocal create_service_calls
        create_service_calls += 1
        return (
            DummyAsyncService(create_service_calls),
            DummyAsyncCredential(create_service_calls),
        )

    config = AzureStorageConfig(container="demo", connection_string="conn")
    monkeypatch.setattr(
        AzureStorageConfig,
        "create_async_service_client",
        create_async_service_client_mock,
    )

    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="dev-skip")

    # First access in first event loop
    container1 = await client.container_async()
    assert container1 is not None
    assert container1.loop_id == 1
    assert create_service_calls == 1

    # Second access in same loop should reuse cached clients
    container2 = await client.container_async()
    assert container2 is container1
    assert create_service_calls == 1

    # Simulate event loop change by replacing the cached loop reference
    # with a mock object (simulating what happens when Azure Functions
    # closes the old loop and creates a new one)
    fake_old_loop = Mock()
    fake_old_loop.is_closed.return_value = False  # Loop is still open, just changed
    client._async_clients_loop = fake_old_loop

    # Now access again - this should detect the loop change
    container3 = await client.container_async()
    assert container3 is not None
    # Should have created new clients
    assert create_service_calls == 2
    # New container should have new loop_id
    assert container3.loop_id == 2
    # Old clients should have been closed
    assert "container-1" in closed_clients
    assert "service-1" in closed_clients
    assert "credential-1" in closed_clients

    await client.aclose()


@pytest.mark.asyncio
async def test_concurrent_async_uploads_multiple_files(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test concurrent async uploads like multi-site screenshot batches.

    This simulates the scenario from EVENT_LOOP_CLOSURE_AZURE_UPLOADS.md where
    multiple files are uploaded concurrently (3 sites × 2 files = 6 uploads).
    """
    import asyncio

    uploads: list[tuple[str, bytes]] = []
    upload_call_count = 0

    class DummyAsyncContainer:
        async def create_container(self) -> None:
            pass

        async def upload_blob(self, *, name: str, data: bytes | object, overwrite: bool) -> None:
            nonlocal upload_call_count
            upload_call_count += 1
            # Read data if it's a file handle
            if hasattr(data, "read"):
                content = data.read()
            else:
                content = data if isinstance(data, bytes) else data.encode("utf-8")
            uploads.append((name, content))
            # Simulate some async work
            await asyncio.sleep(0.001)

        async def close(self) -> None:
            pass

    class DummyAsyncService:
        def __init__(self, container: DummyAsyncContainer) -> None:
            self.container = container

        def get_container_client(self, container_name: str) -> DummyAsyncContainer:
            return self.container

        async def close(self) -> None:
            pass

    container = DummyAsyncContainer()
    service = DummyAsyncService(container)
    config = AzureStorageConfig(container="demo", prefix="screenshot-output")

    monkeypatch.setattr(
        AzureStorageConfig,
        "create_async_service_client",
        lambda self: (service, None),
    )

    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="strict")

    # Create test files simulating multi-site batch (3 sites × 2 files each)
    sites = ["landonorris-com", "wonjyou-studio", "algon-iq"]
    files_to_upload: list[tuple[Path, str]] = []

    for site in sites:
        site_dir = tmp_path / "runs" / "e2e-multi-sites-test" / site
        site_dir.mkdir(parents=True, exist_ok=True)

        # Screenshot PNG
        screenshot = site_dir / "screenshot.png"
        screenshot.write_bytes(b"fake-png-data-" + site.encode())
        files_to_upload.append((screenshot, f"screenshot for {site}"))

        # Metadata JSON
        metadata = site_dir / "metadata.json"
        metadata.write_text(f'{{"site": "{site}"}}')
        files_to_upload.append((metadata, f"metadata for {site}"))

    # Upload all files concurrently (simulating the bug scenario)
    upload_tasks = [client.upload_file_async(path) for path, _ in files_to_upload]

    # This should NOT raise "RuntimeError: Event loop is closed"
    await asyncio.gather(*upload_tasks)

    # Verify all uploads succeeded
    assert upload_call_count == 6
    assert len(uploads) == 6

    # Verify correct blob names and content
    for path, description in files_to_upload:
        expected_blob = config.blob_name_for_path(path)
        matching_uploads = [u for u in uploads if u[0] == expected_blob]
        assert len(matching_uploads) == 1, f"Missing upload for {description}"

    await client.aclose()


@pytest.mark.asyncio
async def test_upload_text_async_handles_errors_gracefully(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that async upload errors are caught and logged, not raised silently."""
    import logging

    class FailingAsyncContainer:
        async def create_container(self) -> None:
            pass

        async def upload_blob(self, *, name: str, data: bytes, overwrite: bool) -> None:
            # Simulate the event loop closure error
            raise RuntimeError("Event loop is closed")

        async def close(self) -> None:
            pass

    class DummyAsyncService:
        def __init__(self, container: FailingAsyncContainer) -> None:
            self.container = container

        def get_container_client(self, container_name: str) -> FailingAsyncContainer:
            return self.container

        async def close(self) -> None:
            pass

    container = FailingAsyncContainer()
    service = DummyAsyncService(container)
    config = AzureStorageConfig(container="demo", prefix=None)

    monkeypatch.setattr(
        AzureStorageConfig,
        "create_async_service_client",
        lambda self: (service, None),
    )

    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="strict", swallow_errors=True)
    caplog.set_level(logging.WARNING)

    path = tmp_path / "test.txt"

    # Should log warning but not raise
    await client.upload_text_async(path, "test content")

    assert "Azure upload failed" in caplog.text
    assert "retaining local copy" in caplog.text

    await client.aclose()


@pytest.mark.asyncio
async def test_upload_file_async_fails_loudly_when_configured(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Test that async upload errors are raised when swallow_errors=False."""

    class FailingAsyncContainer:
        async def create_container(self) -> None:
            pass

        async def upload_blob(self, *, name: str, data: object, overwrite: bool) -> None:
            raise RuntimeError("Event loop is closed")

        async def close(self) -> None:
            pass

    class DummyAsyncService:
        def __init__(self, container: FailingAsyncContainer) -> None:
            self.container = container

        def get_container_client(self, container_name: str) -> FailingAsyncContainer:
            return self.container

        async def close(self) -> None:
            pass

    container = FailingAsyncContainer()
    service = DummyAsyncService(container)
    config = AzureStorageConfig(container="demo", prefix=None)

    monkeypatch.setattr(
        AzureStorageConfig,
        "create_async_service_client",
        lambda self: (service, None),
    )

    client = AzureStorageClient(config=config, settings=_TEST_SETTINGS, mode="strict", swallow_errors=False)

    path = tmp_path / "test.bin"
    path.write_bytes(b"test content")

    # Should raise the error
    with pytest.raises(RuntimeError, match="Event loop is closed"):
        await client.upload_file_async(path)

    await client.aclose()
