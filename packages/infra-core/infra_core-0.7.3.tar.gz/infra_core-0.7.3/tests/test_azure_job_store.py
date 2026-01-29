from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

import pytest

from infra_core.azure import job_store
from infra_core.azure.job_store import AzureTableError, AzureTableJobStore, AzureTableRecordProtocol, TableConfig


class FakeRecord(AzureTableRecordProtocol):
    def __init__(self, batch_id: str, job_id: str, updated_at: str | None = None) -> None:
        self.batch_id = batch_id
        self.job_id = job_id
        self.updated_at = updated_at

    def to_entity(self) -> Mapping[str, Any]:
        return {}

    @classmethod
    def from_entity(cls, entity: Mapping[str, Any]) -> FakeRecord:
        return cls(
            cast(str, entity.get("PartitionKey")),
            cast(str, entity.get("RowKey")),
            cast(str | None, entity.get("updated_at")),
        )


class FakePager:
    def __init__(self, pages: list[dict[str, Any]]) -> None:
        self.pages = pages
        self.continuation_token: str | None = None

    def by_page(self, continuation_token: str | None = None):
        start_index = 0
        if continuation_token is not None:
            for idx, page in enumerate(self.pages):
                if page.get("token") == continuation_token:
                    start_index = idx
                    break
        pages = self.pages[start_index:]

        class _Iterator:
            def __init__(self, outer: FakePager, items: list[dict[str, Any]]) -> None:
                self._outer = outer
                self._items = items
                self._gen = self._iter()
                self.continuation_token: str | None = None

            def _iter(self):
                for page in self._items:
                    next_token = page.get("next")
                    self.continuation_token = next_token
                    self._outer.continuation_token = next_token
                    yield page.get("items", [])

            def __iter__(self):
                return self

            def __next__(self):
                return next(self._gen)

        return _Iterator(self, pages)


class FakeTableClient:
    def __init__(self, pages: list[dict[str, Any]]) -> None:
        self.pages = pages
        self.queries: list[tuple[str, int]] = []

    def query_entities(self, *, query_filter: str, results_per_page: int) -> FakePager:
        self.queries.append((query_filter, results_per_page))
        return FakePager(self.pages)


def _build_store(
    monkeypatch: pytest.MonkeyPatch,
    pages: list[dict[str, Any]],
) -> tuple[AzureTableJobStore[FakeRecord], FakeTableClient]:
    fake_client = FakeTableClient(pages)
    monkeypatch.setattr(job_store, "_table_client", lambda _config: fake_client)
    config = TableConfig(connection_string="UseDevelopmentStorage=true", table_name="test")
    store = AzureTableJobStore(
        record_type=FakeRecord,
        connection_string_var="CONN",
        table_name_var="TABLE",
        config=config,
    )
    return store, fake_client


def test_list_runs_uses_filtered_query_and_returns_continuation(monkeypatch: pytest.MonkeyPatch) -> None:
    pages = [
        {
            "token": None,
            "items": [{"PartitionKey": "batch-1", "RowKey": "a", "updated_at": "2024-01-02"}],
            "next": "ct1",
        },
    ]
    store, fake_client = _build_store(monkeypatch, pages)

    records, token = store.list_runs("batch-1", limit=1)

    assert fake_client.queries == [("PartitionKey eq 'batch-1'", 1)]
    assert token == "ct1"
    assert [record.job_id for record in records] == ["a"]


def test_list_runs_paginates_with_token(monkeypatch: pytest.MonkeyPatch) -> None:
    pages = [
        {
            "token": None,
            "items": [{"PartitionKey": "batch-1", "RowKey": "a", "updated_at": "2024-01-02"}],
            "next": "ct1",
        },
        {
            "token": "ct1",
            "items": [{"PartitionKey": "batch-1", "RowKey": "b", "updated_at": "2024-01-01"}],
            "next": None,
        },
    ]
    store, _ = _build_store(monkeypatch, pages)

    first_page, token = store.list_runs("batch-1", limit=1)
    assert token == "ct1"
    assert [record.job_id for record in first_page] == ["a"]

    second_page, token2 = store.list_runs("batch-1", limit=1, continuation_token=token)
    assert token2 is None
    assert [record.job_id for record in second_page] == ["b"]


def test_list_runs_missing_partition_is_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    store, fake_client = _build_store(monkeypatch, [])

    records, token = store.list_runs("missing", limit=1)

    assert fake_client.queries == [("PartitionKey eq 'missing'", 1)]
    assert records == []
    assert token is None


def test_list_runs_requires_query_entities(monkeypatch: pytest.MonkeyPatch) -> None:
    class MinimalClient:
        def list_entities(self, **_kwargs: object) -> None:
            return None

    monkeypatch.setattr(job_store, "_table_client", lambda _config: MinimalClient())
    config = TableConfig(connection_string="UseDevelopmentStorage=true", table_name="test")
    store = AzureTableJobStore(
        record_type=FakeRecord,
        connection_string_var="CONN",
        table_name_var="TABLE",
        config=config,
    )

    with pytest.raises(AzureTableError, match="query_entities is unavailable"):
        store.list_runs("batch-1", limit=1)
