"""Tests for the infra_core package export surface."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest


def test_package_exports_public_symbols() -> None:
    import infra_core

    required = [
        "TaskRuntime",
        "RuntimeConfig",
        "download_asset",
        "fetch_async",
        "AzureStorageClient",
        "AzureStorageSettings",
        "get_client",
    ]
    for name in required:
        assert hasattr(infra_core, name), f"{name} missing from infra_core"
        assert name in infra_core.__all__


def test_package_handles_missing_azure_dependencies(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    module_name = "infra_core"
    sys.modules.pop(module_name, None)
    sys.modules.pop(f"{module_name}.azure_storage", None)
    sys.modules.pop(f"{module_name}.azure", None)
    sys.modules.pop(f"{module_name}.azure.storage", None)
    monkeypatch.setitem(sys.modules, "azure.identity", None)
    monkeypatch.setitem(sys.modules, "azure.identity.aio", None)

    module = importlib.import_module(module_name)

    # get_client now requires arguments, so just calling it should fail
    # when Azure dependencies are missing
    with pytest.raises(ModuleNotFoundError):
        module.get_client(None, None)

    sys.modules.pop(module_name, None)
