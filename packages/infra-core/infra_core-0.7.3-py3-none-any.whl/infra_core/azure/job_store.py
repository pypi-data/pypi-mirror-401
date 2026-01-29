"""Shared Azure Table Storage helpers for service job stores."""

from __future__ import annotations

import logging
import os
from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast

from .exceptions import AzureTableError

if TYPE_CHECKING:  # pragma: no cover - for type checkers
    from azure.core.exceptions import ResourceNotFoundError
else:  # pragma: no cover - runtime fallback
    try:
        from azure.core.exceptions import ResourceNotFoundError  # type: ignore
    except Exception:

        class ResourceNotFoundError(Exception):
            """Fallback when Azure SDK is unavailable."""


logger = logging.getLogger(__name__)

RecordT = TypeVar("RecordT", bound="AzureTableRecordProtocol")


class AzureTableRecordProtocol:
    """Protocol describing the record interface required by the job store."""

    batch_id: str
    job_id: str
    updated_at: str | None

    def to_entity(self) -> Mapping[str, Any]:  # pragma: no cover - Protocol stub
        raise NotImplementedError

    @classmethod
    def from_entity(cls, entity: Mapping[str, Any]) -> AzureTableRecordProtocol:  # pragma: no cover - Protocol stub
        raise NotImplementedError


@dataclass(frozen=True)
class TableConfig:
    """Resolved configuration for connecting to an Azure Table."""

    connection_string: str
    table_name: str

    @classmethod
    def from_env(
        cls,
        *,
        connection_var: str,
        table_var: str,
        fallback_connection_var: str = "AZURE_STORAGE_CONNECTION_STRING",
        env: Mapping[str, str] | None = None,
    ) -> TableConfig:
        source = env or os.environ
        connection = (source.get(connection_var) or source.get(fallback_connection_var) or "").strip()
        if not connection:
            raise AzureTableError(
                f"{connection_var} (or {fallback_connection_var}) must be configured for Azure job tracking"
            )
        table_name = (source.get(table_var) or "").strip()
        if not table_name:
            raise AzureTableError(f"{table_var} environment variable must be set for Azure job tracking")
        return cls(connection_string=connection, table_name=table_name)


@lru_cache(maxsize=16)
def _table_client(config: TableConfig) -> Any:
    try:
        from azure.data.tables import TableServiceClient
    except ImportError as exc:  # pragma: no cover - optional dependency missing
        raise AzureTableError(
            "azure-data-tables package is required for Azure job tracking. "
            "Install it with `pip install azure-data-tables`."
        ) from exc

    service = TableServiceClient.from_connection_string(config.connection_string)
    table_client = service.create_table_if_not_exists(config.table_name)
    if table_client is None:
        table_client = service.get_table_client(config.table_name)
    return table_client


def reset_table_client_cache() -> None:
    """Clear the cached table clients.

    Use this to force reconnection after configuration changes or in tests
    to ensure isolation between test cases. Existing AzureTableJobStore
    instances will continue using their cached client references.
    """
    _table_client.cache_clear()


class AzureTableJobStore(Generic[RecordT]):
    """Generic wrapper around Azure Table Storage for run metadata."""

    def __init__(
        self,
        *,
        record_type: type[RecordT],
        connection_string_var: str,
        table_name_var: str,
        fallback_connection_var: str = "AZURE_STORAGE_CONNECTION_STRING",
        config: TableConfig | None = None,
        env: Mapping[str, str] | None = None,
    ) -> None:
        self._record_type = record_type
        self._config = config or TableConfig.from_env(
            connection_var=connection_string_var,
            table_var=table_name_var,
            fallback_connection_var=fallback_connection_var,
            env=env,
        )
        self._client = _table_client(self._config)

    # ------------------------------------------------------------------
    # CRUD helpers
    # ------------------------------------------------------------------

    def create(self, record: RecordT) -> RecordT:
        self._client.upsert_entity(record.to_entity())
        return record

    def save(self, record: RecordT) -> RecordT:
        self._client.upsert_entity(record.to_entity())
        return record

    def fetch(self, batch_id: str, job_id: str) -> RecordT | None:
        try:
            entity = self._client.get_entity(batch_id, job_id)
        except (ResourceNotFoundError, KeyError):  # pragma: no cover - SDK raises on missing entities
            return None
        except Exception:
            logger.exception("Failed to fetch table entity", extra={"batch_id": batch_id, "job_id": job_id})
            raise
        return cast(RecordT, self._record_type.from_entity(entity))

    # ------------------------------------------------------------------
    # Listing helpers
    # ------------------------------------------------------------------

    def list_runs(
        self,
        batch_id: str,
        *,
        limit: int = 50,
        continuation_token: str | None = None,
    ) -> tuple[list[RecordT], str | None]:
        filter_expr = f"PartitionKey eq '{batch_id}'"
        query_fn = getattr(self._client, "query_entities", None)

        if callable(query_fn):
            pager = query_fn(query_filter=filter_expr, results_per_page=limit).by_page(
                continuation_token=continuation_token
            )

            try:
                page = next(pager)
            except StopIteration:  # pragma: no cover - empty dataset
                return [], None

            collected = [cast(RecordT, self._record_type.from_entity(entity)) for entity in page]
            next_token = getattr(pager, "continuation_token", None)

            collected.sort(key=lambda rec: rec.updated_at or "", reverse=True)
            return collected, next_token

        raise AzureTableError(
            "query_entities is unavailable on the configured Table client; upgrade azure-data-tables "
            "or provide a client with query_entities to avoid unfiltered scans."
        )

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    @property
    def client(self) -> Any:
        """Expose the underlying TableClient for advanced scenarios (e.g., aggregation)."""

        return self._client


__all__ = ["AzureTableError", "AzureTableJobStore", "TableConfig", "reset_table_client_cache"]
