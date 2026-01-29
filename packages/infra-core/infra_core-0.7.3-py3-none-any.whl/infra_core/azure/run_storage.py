"""Shared filesystem/blob storage helpers for Azure-hosted run services.

This module centralises the logic for building run storage paths, enumerating
local artifacts, and mirroring them with Azure Blob Storage. Services can reuse
these helpers to keep manifest generation consistent across crawler and
screenshot workloads.

Example:
    >>> from infra_core.azure.run_storage import build_run_storage_path
    >>> path = build_run_storage_path("CRAWL_STORAGE_BASE", "runs", "batch", "job")
    >>> path.parts[-3:]
    ('runs', 'batch', 'job')
"""

from __future__ import annotations

import logging
import mimetypes
import os
import tempfile
from collections.abc import Iterable, Mapping
from pathlib import Path

from .storage import AzureStorageClient, ConfigurationError

_DEFAULT_FALLBACK_ENVS: tuple[str, ...] = ("TMP", "TEMP", "TMPDIR")


logger = logging.getLogger(__name__)


def resolve_base_path(env_var: str, *, fallback_envs: Iterable[str] | None = None) -> Path:
    """Resolve the root directory for run storage.

    Prefers the explicit ``env_var`` override, then checks common temporary
    directory variables before falling back to ``tempfile.gettempdir``.

    Args:
        env_var: Name of the environment variable that points to the desired
            base directory.
        fallback_envs: Optional iterable of environment variables to probe
            when ``env_var`` is unset or empty. Defaults to ``TMPDIR``, ``TMP``,
            and ``TEMP``.

    Returns:
        Path to the directory that should contain run artifacts.
    """

    override = (os.getenv(env_var) or "").strip()
    if override:
        return Path(override)

    for candidate in fallback_envs or _DEFAULT_FALLBACK_ENVS:
        value = (os.getenv(candidate) or "").strip()
        if value:
            return Path(value)

    return Path(tempfile.gettempdir())


def build_run_storage_path(env_var: str, *segments: str, fallback_envs: Iterable[str] | None = None) -> Path:
    """Build a run storage path below the resolved base directory.

    Args:
        env_var: Environment variable that controls the storage base.
        *segments: Additional path components appended under the base.
        fallback_envs: Optional override for the fallback variable probe order.

    Returns:
        Full path to the run storage directory.
    """

    base = resolve_base_path(env_var, fallback_envs=fallback_envs)
    path = base
    for segment in segments:
        if segment:
            path /= segment
    return path


def collect_local_files(storage_path: Path) -> list[dict[str, int | str]]:
    """Return file metadata for on-disk artifacts within ``storage_path``.

    Args:
        storage_path: Directory containing run artifacts.

    Returns:
        List of ``{"path": <relative>, "size": <bytes>}`` dictionaries sorted
        lexicographically by path. Returns an empty list when the directory does
        not exist.
    """

    if not storage_path.exists() or not storage_path.is_dir():
        return []

    items: list[dict[str, int | str]] = []
    for path in storage_path.rglob("*"):
        if path.is_file():
            items.append(
                {
                    "path": str(path.relative_to(storage_path)),
                    "size": path.stat().st_size,
                }
            )
    items.sort(key=lambda item: item["path"])
    return items


def collect_blob_files(client: AzureStorageClient, storage_path: Path) -> list[dict[str, int | str]]:
    """Enumerate blob-backed artifacts for ``storage_path`` via ``client``.

    Args:
        client: Azure storage client used to list blob contents.
        storage_path: Local directory whose relative structure is mirrored in
            Azure Blob Storage.

    Returns:
        List of ``{"path": <relative>, "size": <bytes>}`` dictionaries sorted
        lexicographically by path.
    """

    if not client.is_configured():
        raise ConfigurationError("Azure storage is not configured for blob collection")

    try:
        entries = client.list_tree(storage_path)
    except Exception as exc:  # pragma: no cover - defensive guard around SDK failures
        logger.warning(
            "Failed to enumerate Azure storage for run manifest",
            extra={"storage_path": str(storage_path), "error": type(exc).__name__},
            exc_info=True,
        )
        raise

    items: list[dict[str, int | str]] = [{"path": relative_path, "size": size} for relative_path, size in entries]
    items.sort(key=lambda item: item["path"])
    return items


def _infer_file_type(path: str) -> str:
    """Infer generic file type category from path extension.

    Categorizes files into broad types (image, document, data, other)
    based on file extension for manifest organization.

    Args:
        path: File path with extension (e.g., "photo.jpg", "data.json").

    Returns:
        Category string: "image", "document", "data", or "other".

    Example:
        >>> _infer_file_type("logo.png")
        'image'
        >>> _infer_file_type("config.yaml")
        'data'
        >>> _infer_file_type("unknown.xyz")
        'other'
    """
    path_lower = path.lower()
    if path_lower.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg", ".ico")):
        return "image"
    if path_lower.endswith((".html", ".htm", ".xml", ".txt", ".md", ".csv")):
        return "document"
    if path_lower.endswith((".json", ".yaml", ".yml", ".toml", ".ini", ".conf")):
        return "data"
    return "other"


def _infer_content_type(path: str) -> str:
    """Infer MIME content type from path extension.

    Uses Python's mimetypes library with fallback to application/octet-stream.

    Args:
        path: File path with extension (e.g., "photo.jpg", "data.json").

    Returns:
        MIME content type string (e.g., "image/png", "application/json").

    Example:
        >>> _infer_content_type("logo.png")
        'image/png'
        >>> _infer_content_type("unknown.xyz")
        'application/octet-stream'
    """
    content_type, _ = mimetypes.guess_type(path)
    return content_type or "application/octet-stream"


def _build_file_entries(
    raw_files: list[dict[str, int | str]],
    root: Path,
    client: AzureStorageClient,
) -> list[dict[str, object]]:
    """Build enriched file entries with URLs and metadata.

    Transforms raw file records (path + size) into enriched entries with
    inferred file types, MIME content types, and full blob URLs when Azure
    storage is configured.

    Args:
        raw_files: List of file records with 'path' and 'size' keys.
        root: Base storage path used to construct blob names.
        client: Azure storage client for URL generation.

    Returns:
        List of enriched file dictionaries with path, type, content_type,
        size_bytes, and optional url fields.
    """
    enriched_files = []

    for file_entry in raw_files:
        path = str(file_entry["path"])
        size = int(file_entry["size"])

        entry: dict[str, object] = {
            "path": path,
            "type": _infer_file_type(path),
            "content_type": _infer_content_type(path),
            "size_bytes": size,
        }

        # Add URL if Azure storage is configured
        if client.is_configured():
            blob_name = client.blob_name_for_path(root / path)
            url = client.blob_url_for_name(blob_name)
            if url:
                entry["url"] = url

        enriched_files.append(entry)

    return enriched_files


def _build_storage_section(root: Path, client: AzureStorageClient) -> dict[str, object] | None:
    """Build storage metadata section with provider and blob location.

    Constructs storage metadata including provider type (azure_blob),
    blob prefix path, and container name for files in the manifest.

    Args:
        root: Base storage path used to construct blob prefix.
        client: Azure storage client for settings and path resolution.

    Returns:
        Storage metadata dictionary with provider, prefix, and container
        fields, or None if Azure storage is not configured.
    """
    if not client.is_configured():
        return None

    settings = client.settings
    if not settings:
        return None

    blob_prefix = client.blob_name_for_path(root)

    storage: dict[str, object] = {
        "provider": "azure_blob",
        "prefix": blob_prefix,
    }

    if settings.container:
        storage["container"] = settings.container

    return storage


def _get_file_size(file_entry: dict[str, object]) -> int:
    """Extract size_bytes from file entry with type safety.

    Args:
        file_entry: File dictionary containing size_bytes field.

    Returns:
        File size in bytes, or 0 if missing or invalid.
    """
    size = file_entry.get("size_bytes", 0)
    return int(size) if isinstance(size, int) else 0


def _build_summary(files: list[dict[str, object]]) -> dict[str, object]:
    """Build summary statistics section with file counts and sizes.

    Aggregates file metadata to provide total counts, total size in bytes,
    and breakdown of file types for the manifest.

    Args:
        files: List of enriched file dictionaries with type and size_bytes.

    Returns:
        Summary dictionary with total_files, total_size_bytes, and
        file_types breakdown (e.g., {"image": 3, "data": 2}).
    """
    total_size = sum(_get_file_size(f) for f in files)

    # Count by type
    type_counts: dict[str, int] = {}
    for file_entry in files:
        file_type = str(file_entry.get("type", "other"))
        type_counts[file_type] = type_counts.get(file_type, 0) + 1

    return {
        "total_files": len(files),
        "total_size_bytes": total_size,
        "file_types": type_counts,
    }


def build_manifest(
    storage_path: str | Path,
    *,
    client: AzureStorageClient,
) -> Mapping[str, object]:
    """Assemble a manifest describing files for the given run storage path.

    Args:
        storage_path: Directory on disk that may contain run artifacts.
        client: Azure storage client (required).

    Returns:
        Mapping with storage metadata, enriched file listings with URLs,
        and summary statistics. Structure follows 2025 REST API best practices.
    """

    root = Path(storage_path) if storage_path else None
    if root is None or not str(root).strip():
        return {"files": []}

    raw_files = collect_local_files(root)
    if not raw_files:
        raw_files = collect_blob_files(client, root)

    # Build enriched file entries with URLs and metadata
    files = _build_file_entries(raw_files, root, client)

    # Build storage metadata section
    storage_section = _build_storage_section(root, client)

    # Build summary statistics
    summary = _build_summary(files)

    manifest: dict[str, object] = {
        "files": files,
    }

    if storage_section:
        manifest["storage"] = storage_section

    if summary:
        manifest["summary"] = summary

    return manifest


__all__ = [
    "resolve_base_path",
    "build_run_storage_path",
    "collect_local_files",
    "collect_blob_files",
    "build_manifest",
]
