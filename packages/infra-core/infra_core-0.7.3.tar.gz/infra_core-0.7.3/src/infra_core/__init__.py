"""Expose runtime, storage, and HTTP helpers for automation pipelines.

This package centralizes the public surface of infra_core so downstream
projects can import stable symbols without relying on internal layout. It
re-exports runtime orchestration primitives, Azure Storage clients, filesystem
utilities, and both sync/async HTTP helpers.

Example:
    >>> from infra_core import (
    ...     TaskRuntime,
    ...     RuntimeConfig,
    ...     azure_is_enabled,
    ...     fetch_async,
    ... )
    >>> runtime = TaskRuntime(config=RuntimeConfig())
    >>> if azure_is_enabled():
    ...     print("Azure storage configured")
    >>> async def ping() -> int:
    ...     response = await fetch_async("https://example.com/status")
    ...     return response.status
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from . import polling as polling
from .asset_client import (
    AssetDownloadClient,
    DownloadResult,
    download_asset,
    download_asset_async,
)
from .fs_utils import compute_checksum, ensure_parent, hashed_asset_path
from .http import DEFAULT_HEADERS as http_default_headers
from .http import fetch
from .http_async import (
    DEFAULT_HEADERS as http_async_default_headers,
)
from .http_async import (
    fetch_async,
    request_async,
)
from .polling import (
    PollingConfig,
    PollingError,
    PollingFailureError,
    PollingTimeoutError,
    StatusPoller,
    poll_until,
    poll_until_async,
)
from .task_runtime import RuntimeCancellationError, RuntimeConfig, TaskRuntime

logging.getLogger(__name__).addHandler(logging.NullHandler())

AzureStorageClient: Any
AzureStorageSettings: Any
ConfigurationError: Any
StorageMode: Any
get_client: Any
get_shared_client: Any
is_configured: Any
reset_all_clients: Any
blob_path_for: Any
download_to_path: Any
download_to_path_async: Any
download_tree: Any
download_tree_async: Any
get_azure_storage_client: Any
azure_is_enabled: Any
list_tree: Any
list_tree_async: Any
upload_file: Any
upload_file_async: Any
upload_text: Any
upload_text_async: Any

_AZURE_IMPORT_ERROR: ModuleNotFoundError | None = None


def _missing_azure_dependency(name: str) -> Callable[..., None]:
    """Return a callable that raises an informative error for optional Azure helpers."""

    def _missing(*_args: object, **_kwargs: object) -> None:
        if _AZURE_IMPORT_ERROR is not None:
            raise ModuleNotFoundError(
                f"{name} requires optional Azure dependencies. Install 'infra-core[azure]' to enable Azure helpers."
            ) from _AZURE_IMPORT_ERROR
        raise ModuleNotFoundError(f"{name} requires optional Azure dependencies that failed to import.")

    _missing.__name__ = name
    return _missing


try:
    from .azure.storage import (
        AzureStorageClient,
        AzureStorageSettings,
        ConfigurationError,
        StorageMode,
        get_client,
        get_shared_client,
        is_configured,
        reset_all_clients,
    )
except ModuleNotFoundError as exc:
    if exc.name and not exc.name.startswith("azure"):
        raise
    _AZURE_IMPORT_ERROR = exc
    AzureStorageClient = _missing_azure_dependency("AzureStorageClient")
    AzureStorageSettings = _missing_azure_dependency("AzureStorageSettings")
    ConfigurationError = _missing_azure_dependency("ConfigurationError")
    StorageMode = _missing_azure_dependency("StorageMode")
    get_client = _missing_azure_dependency("get_client")
    get_shared_client = _missing_azure_dependency("get_shared_client")
    is_configured = _missing_azure_dependency("is_configured")
    reset_all_clients = _missing_azure_dependency("reset_all_clients")

__all__ = [
    # Runtime
    "TaskRuntime",
    "RuntimeConfig",
    "RuntimeCancellationError",
    # Polling
    "PollingConfig",
    "PollingError",
    "PollingFailureError",
    "PollingTimeoutError",
    "StatusPoller",
    "poll_until",
    "poll_until_async",
    "polling",
    # Asset downloading
    "AssetDownloadClient",
    "DownloadResult",
    "download_asset",
    "download_asset_async",
    # Azure storage
    "AzureStorageClient",
    "AzureStorageSettings",
    "ConfigurationError",
    "StorageMode",
    "get_client",
    "get_shared_client",
    "is_configured",
    "reset_all_clients",
    # Filesystem
    "ensure_parent",
    "hashed_asset_path",
    "compute_checksum",
    # HTTP
    "fetch",
    "fetch_async",
    "request_async",
    "http_default_headers",
    "http_async_default_headers",
]
