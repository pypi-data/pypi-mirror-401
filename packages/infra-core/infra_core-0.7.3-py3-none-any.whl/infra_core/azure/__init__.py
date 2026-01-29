"""Azure integration helpers shared across infra_core.

This package centralises all Azure-specific modules (storage, monitoring,
function helpers, clients, etc.) so downstream services can import from
`infra_core.azure.*` without guessing module names at the top level.
"""

from __future__ import annotations

from . import (
    client,  # re-export module for monkeypatching
    monitoring,  # re-export module for monkeypatching
)
from .client import AzureFunctionAsyncClient, AzureFunctionSyncClient, RequestOptions
from .exceptions import (
    AzureServiceError,
    AzureTableError,
    JobNotFoundError,
    JobTimeoutError,
    ResumeSourceActive,
    ResumeSourceNotFound,
    RunNotFound,
    RunServiceError,
)
from .function_cli import add_azure_service_arguments
from .job_store import AzureTableJobStore, TableConfig, reset_table_client_cache
from .monitoring import HeartbeatMonitor, RunLogWriter, TelemetryClient, TelemetryConfig
from .run_service import RunStorageMixin
from .run_storage import (
    build_manifest,
    build_run_storage_path,
    collect_blob_files,
    collect_local_files,
    resolve_base_path,
)
from .storage import (
    AzureStorageClient,
    AzureStorageSettings,
    ConfigurationError,
    StorageMode,
    get_client,
    get_shared_client,
    is_configured,
    reset_all_clients,
    reset_shared_client,
    reset_shared_client_async,
    set_shared_client,
)

__all__ = [
    # Storage
    "AzureStorageClient",
    "AzureStorageSettings",
    "ConfigurationError",
    "StorageMode",
    "get_client",
    "get_shared_client",
    "is_configured",
    "reset_all_clients",
    "reset_shared_client",
    "reset_shared_client_async",
    "set_shared_client",
    # Monitoring
    "RunLogWriter",
    "HeartbeatMonitor",
    "TelemetryClient",
    "TelemetryConfig",
    # Job store
    "AzureTableError",
    "AzureTableJobStore",
    "TableConfig",
    "reset_table_client_cache",
    # HTTP clients
    "AzureFunctionAsyncClient",
    "AzureFunctionSyncClient",
    "RequestOptions",
    # Run storage
    "build_manifest",
    "build_run_storage_path",
    "collect_blob_files",
    "collect_local_files",
    "resolve_base_path",
    # Exceptions
    "AzureServiceError",
    "RunServiceError",
    "RunNotFound",
    "ResumeSourceNotFound",
    "ResumeSourceActive",
    "JobNotFoundError",
    "JobTimeoutError",
    # Service mixin
    "RunStorageMixin",
    # Modules
    "monitoring",
    "client",
    # CLI
    "add_azure_service_arguments",
]
