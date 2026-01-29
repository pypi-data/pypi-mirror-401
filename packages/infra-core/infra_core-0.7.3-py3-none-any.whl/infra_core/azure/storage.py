"""Opinionated Azure Blob Storage helpers shared across infra_core.

This module layers on top of the official Azure SDK to provide:

- Configuration glue (`AzureStorageSettings.from_env`) so every package reads
  container/connection-string/prefix env vars the same way.
- Cached `AzureStorageClient` instances (sync + async) with proper disposal of
  service clients and credentials via `close()` / `aclose()`.
- Thin module-level helpers (`upload_text`, `download_tree_async`, etc.) that
  delegate to the shared client for legacy callers.
- Mode-aware behaviour (strict by default) that raises on missing configuration,
  with explicit `best-effort` / `dev-skip` options for development-only skips.
- Prefix resolution and screenshot defaults.

Use `get_client(settings=...)` when you need long-lived control, or call the
module helpers for convenience; both paths share the same cached client.
"""

from __future__ import annotations

import asyncio
import contextlib
import errno
import inspect
import json
import logging
import os
import shutil
import tempfile
from collections.abc import AsyncIterable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from types import TracebackType
from typing import Any, Literal, Protocol, TypeAlias, runtime_checkable
from urllib.parse import quote

from azure.core.exceptions import AzureError, ResourceExistsError, ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.identity.aio import DefaultAzureCredential as AsyncDefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.storage.blob.aio import (
    BlobServiceClient as AsyncBlobServiceClient,
)
from azure.storage.blob.aio import (
    ContainerClient as AsyncContainerClient,
)

from ..logging_utils import sanitize_url


@runtime_checkable
class StorageBackend(Protocol):
    def ensure_parent(self, path: Path) -> None: ...

    def write_json(self, path: Path, data: Mapping[str, Any]) -> Path: ...

    def write_text(self, path: Path, text: str) -> Path: ...

    def upload_file(self, path: Path) -> None: ...


logger = logging.getLogger(__name__)

_CONNECTION_STRING_ENV = "AZURE_STORAGE_CONNECTION_STRING"
_CONTAINER_ENV = "AZURE_STORAGE_CONTAINER"
_PREFIX_ENV = "AZURE_STORAGE_BLOB_PREFIX"
_ACCOUNT_ENV = "AZURE_STORAGE_ACCOUNT"
_ENDPOINT_ENV = "AZURE_STORAGE_BLOB_ENDPOINT"
_MODE_ENV = "AZURE_STORAGE_MODE"


class ConfigurationError(RuntimeError):
    """Raised when Azure storage configuration is invalid for the selected mode."""


def _blob_name_for_path(path: Path, *, prefix: str | None = None, base_path: Path | None = None) -> str:
    """Normalise a filesystem path into a blob-compatible name.

    Args:
        path: Filesystem path to convert to blob name.
        prefix: Optional blob prefix to prepend.
        base_path: Optional base directory to make path relative to.
            When provided, the path is made relative to this base before
            conversion to blob name.

    Returns:
        Blob name suitable for Azure Blob Storage, with temp directory
        prefixes stripped and optional prefix prepended.
    """
    # First, try to make path relative to base_path if provided
    if base_path:
        with contextlib.suppress(ValueError):
            # path not under base_path, continue with full path
            path = path.relative_to(base_path)

    blob = path.as_posix().lstrip("/")

    # Safety net: Strip common temp directory prefixes
    # This handles cases where base_path wasn't set or path wasn't relative
    for temp_prefix in ["tmp/", "temp/", "var/tmp/"]:
        if blob.startswith(temp_prefix):
            blob = blob[len(temp_prefix) :]
            break

    if prefix:
        prefix = prefix.rstrip("/")
        return f"{prefix}/{blob}" if blob else prefix
    return blob


StorageMode: TypeAlias = Literal["strict", "best-effort", "dev-skip"]


def _normalize_mode(mode: str | None) -> StorageMode:
    """Normalize mode string to canonical StorageMode value.

    Args:
        mode: Raw mode string from env or parameter.

    Returns:
        Canonical StorageMode ("strict", "best-effort", or "dev-skip").

    Raises:
        ValueError: If mode is not recognized.
    """
    if mode is None:
        return "strict"
    normalized = mode.strip().lower().replace("_", "-")
    if normalized in {"strict"}:
        return "strict"
    if normalized in {"best-effort", "best", "warn"}:
        return "best-effort"
    if normalized in {"dev-skip", "dev", "dev-no-upload", "local-dev-no-upload"}:
        return "dev-skip"
    raise ValueError(f"Unknown Azure storage mode: {mode!r}")


@dataclass(frozen=True)
class AzureStorageSettings:
    """Configuration for Azure Blob Storage from environment variables.

    Either connection_string OR (account_name + blob_endpoint) must be provided.

    Attributes:
        container: Azure storage container name (required).
        connection_string: Full connection string (recommended for local dev).
        account_name: Storage account name (for production with managed identity).
        blob_endpoint: Custom blob endpoint URL (optional, auto-generated from account_name).
        prefix: Blob name prefix for all operations (e.g., "screenshots/").
    """

    container: str | None
    connection_string: str | None = None
    account_name: str | None = None
    blob_endpoint: str | None = None
    prefix: str | None = None

    @classmethod
    def from_env(
        cls,
        *,
        container_var: str = _CONTAINER_ENV,
        connection_string_var: str = _CONNECTION_STRING_ENV,
        account_var: str = _ACCOUNT_ENV,
        endpoint_var: str = _ENDPOINT_ENV,
        prefix_var: str = _PREFIX_ENV,
        mode_var: str = _MODE_ENV,
        env: Mapping[str, str] = os.environ,
    ) -> tuple[AzureStorageSettings, StorageMode]:
        """Load settings and mode from environment variables.

        Args:
            container_var: Env var name for container (default: AZURE_STORAGE_CONTAINER).
            connection_string_var: Env var name for connection string.
            account_var: Env var name for account name.
            endpoint_var: Env var name for blob endpoint.
            prefix_var: Env var name for blob prefix.
            mode_var: Env var name for storage mode (default: AZURE_STORAGE_MODE).
            env: Environment dict (default: os.environ).

        Returns:
            Tuple of (AzureStorageSettings, StorageMode). Settings fields are None
            if corresponding env vars are empty/missing. Mode defaults to "strict".
        """
        settings = cls(
            container=(env.get(container_var) or "").strip() or None,
            connection_string=(env.get(connection_string_var) or "").strip() or None,
            account_name=(env.get(account_var) or "").strip() or None,
            blob_endpoint=(env.get(endpoint_var) or "").strip() or None,
            prefix=(env.get(prefix_var) or "").strip() or None,
        )
        mode = _normalize_mode((env.get(mode_var) or "").strip() or None)
        return settings, mode

    @classmethod
    def from_env_with_prefix(
        cls,
        prefix: str,
        *,
        env: Mapping[str, str] = os.environ,
    ) -> tuple[AzureStorageSettings, StorageMode]:
        """Load settings from prefixed environment variables.

        Convenience method that prepends a service-specific prefix to all
        standard env var names, ensuring isolated configuration per service.

        Args:
            prefix: Service prefix (e.g., "CRAWLER" reads CRAWLER_AZURE_STORAGE_CONTAINER).
            env: Environment dict (default: os.environ).

        Returns:
            Tuple of (AzureStorageSettings, StorageMode).

        Example:
            >>> settings, mode = AzureStorageSettings.from_env_with_prefix("CRAWLER")
            # Reads: CRAWLER_AZURE_STORAGE_CONTAINER, CRAWLER_AZURE_STORAGE_CONNECTION_STRING,
            # CRAWLER_AZURE_STORAGE_ACCOUNT, CRAWLER_AZURE_STORAGE_BLOB_ENDPOINT,
            # CRAWLER_AZURE_STORAGE_BLOB_PREFIX, CRAWLER_AZURE_STORAGE_MODE
        """
        return cls.from_env(
            container_var=f"{prefix}_AZURE_STORAGE_CONTAINER",
            connection_string_var=f"{prefix}_AZURE_STORAGE_CONNECTION_STRING",
            account_var=f"{prefix}_AZURE_STORAGE_ACCOUNT",
            endpoint_var=f"{prefix}_AZURE_STORAGE_BLOB_ENDPOINT",
            prefix_var=f"{prefix}_AZURE_STORAGE_BLOB_PREFIX",
            mode_var=f"{prefix}_AZURE_STORAGE_MODE",
            env=env,
        )


@dataclass(frozen=True)
class _AzureStorageConfig:
    """Internal validated config with guaranteed non-None container.

    This is created from AzureStorageSettings only when container is present.
    Separates "settings from env" from "validated config ready to use".
    """

    container: str
    connection_string: str | None = None
    account_name: str | None = None
    blob_endpoint: str | None = None
    prefix: str | None = None

    @classmethod
    def from_settings(cls, settings: AzureStorageSettings) -> _AzureStorageConfig | None:
        if not settings.container:
            return None
        return cls(
            container=settings.container,
            connection_string=settings.connection_string,
            account_name=settings.account_name,
            blob_endpoint=settings.blob_endpoint,
            prefix=settings.prefix,
        )

    def create_service_client(
        self,
    ) -> tuple[BlobServiceClient, DefaultAzureCredential | None]:
        if self.connection_string:
            logger.debug(
                "Creating BlobServiceClient from connection string",
                extra={"container": self.container},
            )
            client = BlobServiceClient.from_connection_string(self.connection_string)
            return client, None

        account_url = self.blob_endpoint
        if not account_url:
            if not self.account_name:
                raise RuntimeError(
                    "Azure storage credentials are not configured. Provide connection string or account name/endpoint."
                )
            account_url = f"https://{self.account_name}.blob.core.windows.net"

        credential = DefaultAzureCredential()
        logger.debug(
            "Creating BlobServiceClient for account URL",
            extra={
                "container": self.container,
                "account_url": sanitize_url(account_url),
            },
        )
        client = BlobServiceClient(account_url=account_url, credential=credential)
        return client, credential

    def create_container_client(
        self,
    ) -> tuple[ContainerClient, BlobServiceClient, DefaultAzureCredential | None]:
        service, credential = self.create_service_client()
        container = service.get_container_client(self.container)
        try:
            with contextlib.suppress(ResourceExistsError):
                container.create_container()
        except AzureError:
            logger.debug(
                "Container creation skipped due to Azure error (proceeding with existing container)",
                extra={"container": self.container},
                exc_info=True,
            )

        return container, service, credential

    def create_async_service_client(
        self,
    ) -> tuple[AsyncBlobServiceClient, AsyncDefaultAzureCredential | None]:
        if self.connection_string:
            client = AsyncBlobServiceClient.from_connection_string(self.connection_string)
            logger.debug(
                "Creating AsyncBlobServiceClient from connection string",
                extra={"container": self.container},
            )
            return client, None

        account_url = self.blob_endpoint
        if not account_url:
            if not self.account_name:
                raise RuntimeError(
                    "Azure storage credentials are not configured. Provide connection string or account name/endpoint."
                )
            account_url = f"https://{self.account_name}.blob.core.windows.net"

        credential = AsyncDefaultAzureCredential()
        logger.debug(
            "Creating AsyncBlobServiceClient for account URL",
            extra={
                "container": self.container,
                "account_url": sanitize_url(account_url),
            },
        )
        client = AsyncBlobServiceClient(account_url=account_url, credential=credential)
        return client, credential

    def blob_name_for_path(self, path: Path) -> str:
        return _blob_name_for_path(path, prefix=self.prefix)


def _config_from_settings(settings: AzureStorageSettings, mode: StorageMode) -> _AzureStorageConfig | None:
    if mode == "dev-skip":
        return None

    config = _AzureStorageConfig.from_settings(settings)
    if config is None:
        if mode == "best-effort":
            return None
        raise ConfigurationError("Azure storage container is not configured.")

    if not (config.connection_string or config.account_name or config.blob_endpoint):
        if mode == "best-effort":
            return None
        raise ConfigurationError(
            "Azure storage credentials are not configured. Provide a connection string or account name/endpoint."
        )

    return config


class AzureStorageClient(StorageBackend):
    """Azure Blob Storage client with sync/async helpers and StorageBackend support.

    Manages lifecycle of Azure SDK clients (BlobServiceClient, ContainerClient)
    and credentials. Lazily creates clients on first use and caches them. The
    default mode is ``strict``: missing container/credentials will raise a
    ``ConfigurationError``. Explicit opt-outs are available via
    ``mode="best-effort"`` (log+skip when unconfigured) or ``mode="dev-skip"``
    (always skip uploads) for local development.

    Supports both sync and async operations. The async client is created
    independently from the sync client and must be closed with aclose().

    Usage::

        # Sync operations
        client = AzureStorageClient(config, settings=settings)
        client.upload_text(Path("test.txt"), "hello")
        client.close()

        # Async operations
        async with client:
            await client.upload_text_async(Path("test.txt"), "hello")
        # Auto-closes on exit

        # Or use context manager for sync
        with AzureStorageClient(config, settings=settings) as client:
            client.upload_text(Path("test.txt"), "hello")

    Args:
        config: Internal validated config (None only when using dev-skip/best-effort).
        settings: Original settings from env (for logging/prefix fallback).
        enabled: Deprecated toggle; if False, maps to ``mode="dev-skip"``.
        mode: StorageMode (`strict` default, `best-effort`, or `dev-skip`).
        swallow_errors: If True, upload errors are logged and swallowed; otherwise raised.
        base_path: Optional base directory to strip from blob names.
        log: Optional logger override.
    """

    __slots__ = (
        "_config",
        "_settings",
        "_swallow_errors",
        "_logger",
        "_base_path",
        "_service",
        "_credential",
        "_container",
        "_async_service",
        "_async_container",
        "_async_credential",
        "_async_lock",
        "_async_lock_loop",
        "_async_clients_loop",
        "_mode",
        "_unconfigured_logged_actions",
    )

    def __init__(
        self,
        config: _AzureStorageConfig | None,
        *,
        settings: AzureStorageSettings,
        mode: StorageMode,
        swallow_errors: bool = False,
        base_path: Path | None = None,
        log: logging.Logger | None = None,
    ) -> None:
        self._config = config
        self._settings = settings
        self._mode = mode
        self._swallow_errors = swallow_errors
        self._base_path = base_path
        self._logger = log or logger
        self._service: BlobServiceClient | None = None
        self._credential: DefaultAzureCredential | None = None
        self._container: ContainerClient | None = None
        self._async_service: AsyncBlobServiceClient | None = None
        self._async_container: AsyncContainerClient | None = None
        self._async_credential: AsyncDefaultAzureCredential | None = None
        self._async_lock: asyncio.Lock | None = None
        self._async_lock_loop: asyncio.AbstractEventLoop | None = None
        self._async_clients_loop: asyncio.AbstractEventLoop | None = None
        self._unconfigured_logged_actions: set[str] = set()

    @classmethod
    def from_settings(
        cls,
        settings: AzureStorageSettings,
        mode: StorageMode,
        *,
        swallow_errors: bool = False,
        base_path: Path | None = None,
        log: logging.Logger | None = None,
    ) -> AzureStorageClient:
        """Create client from settings and mode.

        Args:
            settings: Storage settings (from from_env or from_env_with_prefix).
            mode: Storage mode ("strict", "best-effort", or "dev-skip").
            swallow_errors: If True, upload errors are logged and swallowed.
            base_path: Optional base directory to strip from blob names.
            log: Optional logger override.

        Returns:
            Configured AzureStorageClient instance.

        Raises:
            ConfigurationError: In strict mode when container/credentials missing.
        """
        config = _config_from_settings(settings, mode)
        return cls(
            config=config,
            settings=settings,
            mode=mode,
            swallow_errors=swallow_errors,
            base_path=base_path,
            log=log,
        )

    @property
    def config(self) -> _AzureStorageConfig | None:
        return self._config

    @property
    def settings(self) -> AzureStorageSettings | None:
        return self._settings

    def is_configured(self) -> bool:
        return self._config is not None

    def _current_prefix(self) -> str | None:
        if self._config and self._config.prefix:
            return self._config.prefix
        if self._settings and self._settings.prefix:
            return self._settings.prefix
        return None

    def _log_unconfigured(self, action: str, *, level: int = logging.DEBUG, reason: str | None = None) -> None:
        container = self._settings.container if self._settings else None
        message = "Azure storage not configured; skipping action"
        if reason:
            message = f"{message} ({reason})"
        self._logger.log(
            level,
            message,
            extra={
                "container": container or "default",
                "action": action,
                "mode": self._mode,
                "reason": reason,
            },
        )

    def _log_unconfigured_once(self, action: str, *, reason: str | None = None) -> None:
        if action in self._unconfigured_logged_actions:
            return
        self._unconfigured_logged_actions.add(action)
        self._log_unconfigured(action, level=logging.WARNING, reason=reason)

    def blob_name_for_path(self, path: Path) -> str:
        prefix = self._current_prefix()
        return _blob_name_for_path(path, prefix=prefix, base_path=self._base_path)

    def blob_url_for_name(self, blob_name: str) -> str | None:
        """Construct full HTTPS URL for a blob name.

        Args:
            blob_name: Blob name (including any prefix).

        Returns:
            Full HTTPS URL to the blob, or None if not configured.

        Example:
            >>> client.blob_url_for_name("runs/batch/file.png")
            'https://account.blob.core.windows.net/container/runs/batch/file.png'
        """
        settings = self.settings
        if not settings or not settings.container:
            return None

        def _parse_connection_string(conn_str: str) -> dict[str, str]:
            parts: dict[str, str] = {}
            for segment in conn_str.split(";"):
                if not segment or "=" not in segment:
                    continue
                key, _, value = segment.partition("=")
                parts[key.strip()] = value.strip()
            return parts

        base_url: str | None = None
        sas_token: str | None = None

        if settings.blob_endpoint:
            base_url = settings.blob_endpoint.rstrip("/")
        elif settings.account_name:
            base_url = f"https://{settings.account_name}.blob.core.windows.net"
        else:
            conn_parts = _parse_connection_string(settings.connection_string or "")
            blob_endpoint = conn_parts.get("BlobEndpoint") or conn_parts.get("Blobendpoint")
            account_name = conn_parts.get("AccountName") or conn_parts.get("Accountname")

            if blob_endpoint:
                base_url = blob_endpoint.rstrip("/")
            elif account_name:
                base_url = f"https://{account_name}.blob.core.windows.net"
            else:
                return None

            sas_token = conn_parts.get("SharedAccessSignature") or conn_parts.get("Sharedaccesssignature")
            if sas_token:
                sas_token = sas_token.lstrip("?")

        if base_url is None:
            return None

        blob_name_encoded = quote(blob_name, safe="/")
        url = f"{base_url}/{settings.container}/{blob_name_encoded}"
        if sas_token:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}{sas_token}"
        return url

    def _should_upload(self, action: str) -> bool:
        if self._mode == "dev-skip":
            self._log_unconfigured_once(action, reason="mode=dev-skip")
            return False

        if not self.is_configured():
            if self._mode == "best-effort":
                self._log_unconfigured_once(action, reason="mode=best-effort")
                return False
            raise ConfigurationError(
                "Azure storage is not configured. Provide container and credentials or set mode='dev-skip' to skip."
            )

        return True

    def _handle_upload_error(self, path: Path, exc: Exception, *, raise_on_error: bool) -> None:
        if raise_on_error or not self._swallow_errors:
            raise
        self._logger.warning(
            "Azure upload failed; retaining local copy",
            extra={
                "path": str(path),
                "blob_name": self.blob_name_for_path(path),
                "error": type(exc).__name__,
            },
            exc_info=True,
        )

    def ensure_parent(self, path: Path) -> None:
        """Create parent directories for a path if needed."""
        path.parent.mkdir(parents=True, exist_ok=True)

    def write_text(self, path: Path, text: str, *, raise_on_error: bool = False) -> Path:
        """Write text locally and mirror to Azure when enabled."""
        self.ensure_parent(path)
        path.write_text(text, encoding="utf-8")
        try:
            self.upload_text(path, text, raise_on_error=raise_on_error)
        except TypeError:
            # Backwards compatibility with tests that monkeypatch upload_text without kwargs
            self.upload_text(path, text)
        return path

    def write_json(self, path: Path, data: Mapping[str, Any], *, raise_on_error: bool = False) -> Path:
        """Serialize data as JSON, write locally, and mirror to Azure."""
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        try:
            return self.write_text(path, text, raise_on_error=raise_on_error)
        except TypeError:
            return self.write_text(path, text)

    async def write_text_async(self, path: Path, text: str, *, raise_on_error: bool = False) -> Path:
        """Async variant of write_text using thread offload for disk I/O."""
        self.ensure_parent(path)
        await asyncio.to_thread(path.write_text, text, encoding="utf-8")
        try:
            await self.upload_text_async(path, text, raise_on_error=raise_on_error)
        except TypeError:
            await self.upload_text_async(path, text)
        return path

    async def write_json_async(self, path: Path, data: Mapping[str, Any], *, raise_on_error: bool = False) -> Path:
        """Async JSON writer that mirrors to Azure when enabled."""
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        return await self.write_text_async(path, text, raise_on_error=raise_on_error)

    def __enter__(self) -> AzureStorageClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    async def __aenter__(self) -> AzureStorageClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    def _get_async_lock(self) -> asyncio.Lock:
        """Get or create async lock bound to current event loop."""
        loop = asyncio.get_running_loop()
        if self._async_lock is None or self._async_lock_loop is not loop:
            self._async_lock = asyncio.Lock()
            self._async_lock_loop = loop
        return self._async_lock

    def container(self) -> ContainerClient | None:
        if not self._config:
            return None
        if self._container is None:
            container, service, credential = self._config.create_container_client()
            self._container = container
            self._service = service
            self._credential = credential
        return self._container

    async def _close_async_clients(self) -> None:
        """Close async clients without acquiring lock (call within lock context).

        This is separate from aclose() to allow closing stale clients when
        event loop changes, without waiting for explicit aclose() call.
        """
        # Only await close() if the clients' loop is still open
        if self._async_clients_loop is not None and not self._async_clients_loop.is_closed():
            if self._async_container is not None:
                await self._async_container.close()
                self._async_container = None
            if self._async_service is not None:
                await self._async_service.close()
                self._async_service = None
            if self._async_credential is not None:
                await self._async_credential.close()
                self._async_credential = None
        else:
            # Loop is closed - just discard references
            self._async_container = None
            self._async_service = None
            self._async_credential = None
        self._async_clients_loop = None

    async def container_async(self) -> AsyncContainerClient | None:
        if not self._config:
            return None
        lock = self._get_async_lock()
        current_loop = asyncio.get_running_loop()

        async with lock:
            # Check 1: Loop is closed - just discard without awaiting
            if self._async_clients_loop is not None and self._async_clients_loop.is_closed():
                self._async_container = None
                self._async_service = None
                self._async_credential = None
                self._async_clients_loop = None

            # Check 2: Loop changed - await close from new loop (safe)
            if self._async_clients_loop is not None and self._async_clients_loop is not current_loop:
                self._logger.debug(
                    "Event loop changed; closing stale async clients",
                    extra={"container": self._config.container},
                )
                await self._close_async_clients()

            if self._async_service is None:
                service, credential = self._config.create_async_service_client()
                self._async_service = service
                self._async_credential = credential
                self._async_clients_loop = current_loop
            if self._async_container is None:
                container_async = self._async_service.get_container_client(self._config.container)
                try:
                    with contextlib.suppress(ResourceExistsError):
                        await container_async.create_container()
                except AzureError:
                    self._logger.debug(
                        "Async container creation skipped due to Azure error (proceeding with existing container)",
                        extra={"container": self._config.container},
                        exc_info=True,
                    )
                self._async_container = container_async
        return self._async_container

    def upload_text(self, path: Path, text: str, *, raise_on_error: bool = False) -> None:
        """Upload text content to blob storage.

        Args:
            path: Filesystem path that determines blob name (with prefix applied).
            text: Text content to upload (will be UTF-8 encoded).

        Note:
            Mode-dependent: ``strict`` raises ``ConfigurationError`` when unconfigured;
            ``best-effort``/``dev-skip`` log-and-skip uploads.
        """
        if not self._should_upload("upload_text"):
            return
        container = self.container()
        if not container:
            self._log_unconfigured("upload_text")
            return
        blob_name = self.blob_name_for_path(path)
        try:
            _upload_text_sync(container, blob_name, text.encode("utf-8"))
        except (OSError, AzureError) as exc:
            self._handle_upload_error(path, exc, raise_on_error=raise_on_error)
        except Exception as exc:  # pragma: no cover - defensive logging
            self._logger.error(
                "Unexpected failure uploading text to Azure",
                extra={"blob_name": blob_name, "path": str(path)},
                exc_info=True,
            )
            self._handle_upload_error(path, exc, raise_on_error=raise_on_error)

    async def upload_text_async(self, path: Path, text: str, *, raise_on_error: bool = False) -> None:
        if not self._should_upload("upload_text_async"):
            return
        container = await self.container_async()
        if not container:
            self._log_unconfigured("upload_text_async")
            return
        blob_name = self.blob_name_for_path(path)
        try:
            await container.upload_blob(name=blob_name, data=text.encode("utf-8"), overwrite=True)
        except (OSError, AzureError) as exc:
            self._handle_upload_error(path, exc, raise_on_error=raise_on_error)
        except Exception as exc:  # pragma: no cover - defensive logging
            self._logger.error(
                "Unexpected failure uploading text to Azure (async)",
                extra={"blob_name": blob_name, "path": str(path)},
                exc_info=True,
            )
            self._handle_upload_error(path, exc, raise_on_error=raise_on_error)

    def upload_file(self, path: Path, *, blob_path: str | None = None, raise_on_error: bool = False) -> None:
        if not self._should_upload("upload_file"):
            return
        container = self.container()
        if not container:
            self._log_unconfigured("upload_file")
            return
        blob_name = blob_path or self.blob_name_for_path(path)
        try:
            _upload_file_sync(container, blob_name, path)
        except (OSError, AzureError) as exc:
            self._handle_upload_error(path, exc, raise_on_error=raise_on_error)
        except Exception as exc:  # pragma: no cover - defensive logging
            self._logger.error(
                "Unexpected failure uploading file to Azure",
                extra={"blob_name": blob_name, "path": str(path)},
                exc_info=True,
            )
            self._handle_upload_error(path, exc, raise_on_error=raise_on_error)

    async def upload_file_async(
        self, path: Path, *, blob_path: str | None = None, raise_on_error: bool = False
    ) -> None:
        if not self._should_upload("upload_file_async"):
            return
        container = await self.container_async()
        if not container:
            self._log_unconfigured("upload_file_async")
            return
        blob_name = blob_path or self.blob_name_for_path(path)
        try:
            with path.open("rb") as handle:
                await container.upload_blob(name=blob_name, data=handle, overwrite=True)
        except (OSError, AzureError) as exc:
            self._handle_upload_error(path, exc, raise_on_error=raise_on_error)
        except Exception as exc:  # pragma: no cover - defensive logging
            self._logger.error(
                "Unexpected failure uploading file to Azure (async)",
                extra={"blob_name": blob_name, "path": str(path)},
                exc_info=True,
            )
            self._handle_upload_error(path, exc, raise_on_error=raise_on_error)

    def download_to_path(self, path: Path) -> bool:
        container = self.container()
        if not container:
            return False
        blob_name = self.blob_name_for_path(path)
        try:
            downloader = container.download_blob(blob_name)
        except ResourceNotFoundError:
            return False
        _stream_blob_to_path(downloader, path)
        return True

    def download_tree(self, path: Path) -> bool:
        """Download blob tree to local filesystem.

        Downloads the blob at the given path plus all blobs with that path as prefix.
        For example, if path is "screenshots/site1", downloads:
        - screenshots/site1 (if exists as blob)
        - screenshots/site1/* (all blobs with this prefix)

        Args:
            path: Local filesystem path (also used to determine blob prefix).

        Returns:
            True if any blobs were downloaded, False otherwise.

        Note:
            Creates parent directories as needed.
        """
        container = self.container()
        if not container:
            return False
        prefix = self.blob_name_for_path(path)
        downloaded_any = False
        if self.download_to_path(path):
            downloaded_any = True
        if not prefix.endswith("/"):
            prefix = f"{prefix}/"
        for blob in container.list_blobs(name_starts_with=prefix):
            name = getattr(blob, "name", "")
            if not name.startswith(prefix):
                continue
            relative = name[len(prefix) :]
            if not relative:
                continue
            target = path / relative
            try:
                downloader = container.download_blob(name)
            except ResourceNotFoundError:
                continue
            _stream_blob_to_path(downloader, target)
            downloaded_any = True
        return downloaded_any

    def list_tree(self, path: Path) -> list[tuple[str, int]]:
        container = self.container()
        if not container:
            return []
        prefix = self.blob_name_for_path(path)
        if not prefix.endswith("/"):
            prefix = f"{prefix}/"
        results: list[tuple[str, int]] = []
        for blob in container.list_blobs(name_starts_with=prefix):
            name = getattr(blob, "name", "")
            if not name.startswith(prefix):
                continue
            relative = name[len(prefix) :]
            if not relative or relative.endswith("/"):
                continue
            size = getattr(blob, "size", 0) or 0
            results.append((relative, int(size)))
        return results

    async def download_to_path_async(self, path: Path) -> bool:
        container = await self.container_async()
        if not container:
            return False
        blob_name = self.blob_name_for_path(path)
        try:
            downloader = await container.download_blob(blob_name)
        except ResourceNotFoundError:
            return False
        await _stream_blob_to_path_async(downloader, path)
        return True

    async def download_tree_async(self, path: Path) -> bool:
        container = await self.container_async()
        if not container:
            return False
        prefix = self.blob_name_for_path(path)
        downloaded_any = False
        if await self.download_to_path_async(path):
            downloaded_any = True
        if not prefix.endswith("/"):
            prefix = f"{prefix}/"
        async for blob in container.list_blobs(name_starts_with=prefix):
            name = getattr(blob, "name", "")
            if not name.startswith(prefix):
                continue
            relative = name[len(prefix) :]
            if not relative:
                continue
            target = path / relative
            try:
                downloader = await container.download_blob(name)
            except ResourceNotFoundError:
                continue
            await _stream_blob_to_path_async(downloader, target)
            downloaded_any = True
        return downloaded_any

    async def list_tree_async(self, path: Path) -> list[tuple[str, int]]:
        container = await self.container_async()
        if not container:
            return []
        prefix = self.blob_name_for_path(path)
        if not prefix.endswith("/"):
            prefix = f"{prefix}/"
        results: list[tuple[str, int]] = []
        async for blob in container.list_blobs(name_starts_with=prefix):
            name = getattr(blob, "name", "")
            if not name.startswith(prefix):
                continue
            relative = name[len(prefix) :]
            if not relative or relative.endswith("/"):
                continue
            size = getattr(blob, "size", 0) or 0
            results.append((relative, int(size)))
        return results

    def close(self) -> None:
        if self._container is not None:
            self._container.close()
            self._container = None
        if self._service is not None:
            self._service.close()
            self._service = None
        if self._credential is not None:
            self._credential.close()
            self._credential = None

    async def aclose(self) -> None:
        """Close async resources (sync resources are closed for completeness)."""
        self.close()
        lock = self._get_async_lock()
        async with lock:
            await self._close_async_clients()


_CLIENT_LOCK = Lock()
SettingsKey = tuple[str | None, str | None, str | None, str | None, str | None, StorageMode]
_CLIENT_CACHE: dict[SettingsKey, AzureStorageClient] = {}
_PENDING_ASYNC_DISPOSALS: set[asyncio.Task[None]] = set()

# Async lock for async client operations (avoids blocking event loop)
_ASYNC_CLIENT_LOCK: asyncio.Lock | None = None
_ASYNC_CLIENT_LOCK_LOOP: asyncio.AbstractEventLoop | None = None


def _get_async_client_lock() -> asyncio.Lock:
    """Get async lock for async client cache operations.

    Creates a new lock if the current event loop differs from the one
    where the lock was created.
    """
    global _ASYNC_CLIENT_LOCK, _ASYNC_CLIENT_LOCK_LOOP
    loop = asyncio.get_running_loop()
    if _ASYNC_CLIENT_LOCK is None or _ASYNC_CLIENT_LOCK_LOOP is not loop:
        _ASYNC_CLIENT_LOCK = asyncio.Lock()
        _ASYNC_CLIENT_LOCK_LOOP = loop
    return _ASYNC_CLIENT_LOCK


def _settings_cache_key(settings: AzureStorageSettings, mode: StorageMode) -> SettingsKey:
    return (
        settings.container,
        settings.connection_string,
        settings.account_name,
        settings.blob_endpoint,
        settings.prefix,
        mode,
    )


def get_shared_client(
    settings: AzureStorageSettings,
    mode: StorageMode,
) -> AzureStorageClient:
    """Get or create cached Azure storage client.

    Returns a cached client if settings match the cache. If settings changed,
    disposes the old client and creates a new one.

    Args:
        settings: Storage settings (from from_env or from_env_with_prefix).
        mode: Storage mode ("strict", "best-effort", or "dev-skip").

    Returns:
        Cached AzureStorageClient instance. In ``strict`` mode, missing config
        raises ``ConfigurationError``; ``best-effort``/``dev-skip`` may return
        an unconfigured client that logs-and-skips uploads.

    Raises:
        ConfigurationError: In strict mode when container/credentials missing.
    """
    key = _settings_cache_key(settings, mode)
    with _CLIENT_LOCK:
        cached = _CLIENT_CACHE.get(key)
        config = _config_from_settings(settings, mode)
        if cached is None or cached.config != config or cached._mode != mode:
            if cached is not None:
                _dispose_client(cached)
            cached = AzureStorageClient(config=config, settings=settings, mode=mode)
            _CLIENT_CACHE[key] = cached
        return cached


def get_client(
    settings: AzureStorageSettings,
    mode: StorageMode,
) -> AzureStorageClient:
    """Alias for get_shared_client."""
    return get_shared_client(settings, mode)


def set_shared_client(
    client: AzureStorageClient,
    settings: AzureStorageSettings,
    mode: StorageMode,
) -> None:
    """Replace the cached client with a custom instance.

    Args:
        client: Custom AzureStorageClient to use.
        settings: Settings key to associate with this client.
        mode: Storage mode for cache key.
    """
    key = _settings_cache_key(settings, mode)
    with _CLIENT_LOCK:
        cached = _CLIENT_CACHE.get(key)
        if cached is not None:
            _dispose_client(cached)
        _CLIENT_CACHE[key] = client


def reset_shared_client(
    settings: AzureStorageSettings,
    mode: StorageMode,
) -> None:
    """Clear cached client and create fresh instance on next access.

    Args:
        settings: Settings key to reset.
        mode: Storage mode for cache key.
    """
    key = _settings_cache_key(settings, mode)
    with _CLIENT_LOCK:
        cached = _CLIENT_CACHE.pop(key, None)
        if cached is not None:
            _dispose_client(cached)


async def reset_shared_client_async(
    settings: AzureStorageSettings,
    mode: StorageMode,
) -> None:
    """Async variant ensuring all resources (sync + async) are released.

    Uses an async lock to avoid blocking the event loop during cache access.
    """
    key = _settings_cache_key(settings, mode)
    lock = _get_async_client_lock()
    async with lock:
        # Use sync lock briefly just to pop from cache (fast operation)
        with _CLIENT_LOCK:
            cached = _CLIENT_CACHE.pop(key, None)
        if cached is None:
            return
        # Async close outside sync lock to avoid blocking
        await cached.aclose()


def reset_all_clients() -> None:
    """Clear all cached clients. Useful for testing."""
    with _CLIENT_LOCK:
        for client in _CLIENT_CACHE.values():
            _dispose_client(client)
        _CLIENT_CACHE.clear()


def is_configured(settings: AzureStorageSettings, mode: StorageMode) -> bool:
    """Check if settings would result in a configured client.

    Args:
        settings: Storage settings to check.
        mode: Storage mode.

    Returns:
        True if client would be configured (has container and credentials).
        Always False for dev-skip mode. Always True if config is valid,
        False otherwise (doesn't raise even in strict mode).
    """
    try:
        return _config_from_settings(settings, mode) is not None
    except ConfigurationError:
        return False


def _upload_text_sync(container: ContainerClient, blob_name: str, data: bytes) -> None:
    container.upload_blob(name=blob_name, data=data, overwrite=True)


def _upload_file_sync(container: ContainerClient, blob_name: str, path: Path) -> None:
    with path.open("rb") as handle:
        container.upload_blob(name=blob_name, data=handle, overwrite=True)


def _iter_downloader_chunks(downloader: Any) -> Iterable[bytes]:
    chunk_method = getattr(downloader, "chunks", None)
    if callable(chunk_method):
        chunks = chunk_method()
        if isinstance(chunks, Iterable):
            yield from chunks
            return
    readall = getattr(downloader, "readall", None)
    if callable(readall):
        data = readall()
        if data:
            yield data
        return
    raise RuntimeError("Downloader does not support chunk iteration or readall()")


async def _aiter_downloader_chunks(downloader: Any) -> AsyncIterable[bytes]:
    chunk_method = getattr(downloader, "chunks", None)
    if callable(chunk_method):
        chunks = chunk_method()
        if hasattr(chunks, "__aiter__"):
            async for chunk in chunks:
                yield chunk
            return
        if isinstance(chunks, Iterable):
            for chunk in chunks:
                yield chunk
            return
    readall = getattr(downloader, "readall", None)
    if callable(readall):
        result = readall()
        if inspect.isawaitable(result):
            data = await result
        else:
            data = result
        if data:
            yield data
        return
    raise RuntimeError("Downloader does not support async chunk iteration or readall()")


def _stream_blob_to_path(downloader: Any, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(destination.parent),
        prefix=f".{destination.name}.",
        suffix=".tmp",
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            for chunk in _iter_downloader_chunks(downloader):
                if not chunk:
                    continue
                handle.write(chunk)
            handle.flush()
            os.fsync(handle.fileno())
        _atomic_replace(tmp_path, destination)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


async def _stream_blob_to_path_async(downloader: Any, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(destination.parent),
        prefix=f".{destination.name}.",
        suffix=".tmp",
    )
    tmp_path = Path(tmp_name)
    loop = asyncio.get_running_loop()
    try:
        with os.fdopen(fd, "wb") as handle:
            async for chunk in _aiter_downloader_chunks(downloader):
                if not chunk:
                    continue
                await loop.run_in_executor(None, handle.write, chunk)
            await loop.run_in_executor(None, handle.flush)
            await loop.run_in_executor(None, os.fsync, handle.fileno())
        await loop.run_in_executor(None, _atomic_replace, tmp_path, destination)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def _atomic_replace(source: Path, destination: Path) -> None:
    """Replace destination with source, falling back to shutil.move across devices."""
    try:
        source.replace(destination)
    except OSError as exc:
        if exc.errno == errno.EXDEV:
            shutil.move(str(source), str(destination))
            return
        raise


def _dispose_client(client: AzureStorageClient) -> None:
    """Dispose client resources, awaiting async cleanup when feasible."""
    try:
        client.close()
    except Exception:  # pragma: no cover - defensive disposal
        logger.debug("Failed to close AzureStorageClient synchronously", exc_info=True)
    _schedule_async_disposal(client)


def _schedule_async_disposal(client: AzureStorageClient) -> None:
    """Best-effort async cleanup for callers without an event loop."""

    async def _dispose_async() -> None:
        try:
            await client.aclose()
        except Exception:  # pragma: no cover - defensive disposal
            logger.debug("Failed to close AzureStorageClient asynchronously", exc_info=True)

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        try:
            asyncio.run(client.aclose())
        except RuntimeError:
            logger.debug(
                "No running loop available to dispose AzureStorageClient async resources",
                exc_info=True,
            )
        except Exception:  # pragma: no cover - defensive disposal
            logger.debug("Failed to dispose AzureStorageClient async resources", exc_info=True)
        return

    task = loop.create_task(_dispose_async())
    _PENDING_ASYNC_DISPOSALS.add(task)

    def _clear(completed: asyncio.Task[None]) -> None:
        _PENDING_ASYNC_DISPOSALS.discard(completed)

    task.add_done_callback(_clear)
