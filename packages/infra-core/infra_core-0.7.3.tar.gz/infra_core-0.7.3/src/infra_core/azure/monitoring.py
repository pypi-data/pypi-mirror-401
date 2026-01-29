"""Shared run logging, heartbeat, and telemetry helpers for Azure services."""

from __future__ import annotations

import _thread
import json
import logging
import os
import threading
import time
import warnings
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Final

from ..fs_utils import ensure_parent
from . import storage as azure_storage

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TelemetryConfig:
    """Configuration for Application Insights telemetry.

    Attributes:
        connection_string: Application Insights connection string or instrumentation key.
        enabled: Whether telemetry is enabled (True if connection_string is set).
    """

    connection_string: str | None = None
    enabled: bool = True

    @classmethod
    def from_env(cls, *, env: Mapping[str, str] | None = None) -> TelemetryConfig:
        """Load telemetry config from standard environment variables.

        Reads APPLICATIONINSIGHTS_CONNECTION_STRING or APPINSIGHTS_INSTRUMENTATIONKEY.

        Args:
            env: Optional environment mapping (defaults to os.environ).

        Returns:
            TelemetryConfig with connection string and enabled status.
        """
        source = env if env is not None else os.environ
        conn_str = (
            source.get("APPLICATIONINSIGHTS_CONNECTION_STRING") or source.get("APPINSIGHTS_INSTRUMENTATIONKEY") or ""
        ).strip() or None
        return cls(connection_string=conn_str, enabled=bool(conn_str))

    @classmethod
    def from_env_with_prefix(cls, prefix: str, *, env: Mapping[str, str] | None = None) -> TelemetryConfig:
        """Load telemetry config from prefixed environment variables.

        Reads {PREFIX}_APPLICATIONINSIGHTS_CONNECTION_STRING, falling back to
        standard env vars if not found.

        Args:
            prefix: Environment variable prefix (e.g., "CRAWLER").
            env: Optional environment mapping (defaults to os.environ).

        Returns:
            TelemetryConfig with connection string and enabled status.

        Example:
            >>> config = TelemetryConfig.from_env_with_prefix("CRAWLER")
            # Reads CRAWLER_APPLICATIONINSIGHTS_CONNECTION_STRING
        """
        source = env if env is not None else os.environ
        prefixed_key = f"{prefix}_APPLICATIONINSIGHTS_CONNECTION_STRING"
        conn_str = source.get(prefixed_key, "").strip()
        if conn_str:
            return cls(connection_string=conn_str, enabled=True)
        # Fall back to standard env vars
        return cls.from_env(env=env)


UtcNowFunc = Callable[[], str]


class TelemetryEvent(str, Enum):
    """Canonical telemetry events emitted by shared services."""

    STARTED = "started"
    PROGRESS = "progress"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

    # Upload reliability metrics (Week 3)
    UPLOAD_ATTEMPT = "upload_attempt"
    UPLOAD_SUCCESS = "upload_success"
    UPLOAD_FAILURE = "upload_failure"
    UPLOAD_RETRY = "upload_retry"
    UPLOAD_PERMANENT_ERROR = "upload_permanent_error"
    UPLOAD_TRANSIENT_ERROR = "upload_transient_error"

    # Resume metrics
    RESUME_ASSET_REUSED = "resume_asset_reused"
    RESUME_ASSET_REDOWNLOAD = "resume_asset_redownload"

    # Critical upload metrics
    CRITICAL_UPLOAD_SUCCESS = "critical_upload_success"
    CRITICAL_UPLOAD_FAILURE = "critical_upload_failure"

    def __str__(self) -> str:
        return self.value


TELEMETRY_EVENTS: Final[frozenset[str]] = frozenset(event.value for event in TelemetryEvent)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RunLogWriter:
    """Append structured log entries for a run and mirror them to blob storage.

    Args:
        storage_root: Directory for local log files.
        azure_client: Azure storage client for uploading logs (required).
        utc_now: Optional clock override for testing.
    """

    def __init__(
        self,
        storage_root: Path,
        *,
        azure_client: azure_storage.AzureStorageClient,
        utc_now: UtcNowFunc | None = None,
    ):
        self._log_path = storage_root / "_logs" / "run.log"
        self._lock = threading.Lock()
        self._azure_client = azure_client
        self._utc_now = utc_now or _utc_now

    @property
    def path(self) -> Path:
        return self._log_path

    def write(self, event: str, **properties: Any) -> dict[str, Any]:
        record: dict[str, Any] = {"timestamp": self._utc_now(), "event": event}
        record.update(properties)
        line = json.dumps(record, ensure_ascii=False) + "\n"
        with self._lock:
            ensure_parent(self._log_path)
            with self._log_path.open("a", encoding="utf-8") as handle:
                handle.write(line)
        self._mirror()
        return record

    def _mirror(self) -> None:
        try:
            self._azure_client.upload_file(self._log_path)
        except Exception:  # pragma: no cover - defensive
            logger.warning("Failed to upload run log %s", self._log_path, exc_info=True)


class HeartbeatMonitor:
    """Persist heartbeat metadata and trigger callbacks when slugs stall.

    Args:
        storage_root: Directory for local heartbeat files.
        interval_seconds: How often to persist heartbeat (default: 30s).
        slug_timeout_seconds: Max time for a slug before timeout callback (default: 300s).
        log_writer: Optional run log writer for heartbeat events.
        on_timeout: Callback when a slug times out.
        force_first_slug_timeout: If True, trigger timeout on first slug for testing.
        force_first_slug_delay: Delay before forced timeout.
        azure_client: Azure storage client for uploading heartbeats (required).
        utc_now: Optional clock override for testing.
        on_error: Callback for background thread errors.
        interrupt_main_on_error: If True, interrupt main thread on critical errors.
    """

    def __init__(
        self,
        storage_root: Path,
        *,
        interval_seconds: float = 30.0,
        slug_timeout_seconds: float | None = 300.0,
        log_writer: RunLogWriter | None = None,
        on_timeout: Callable[[str, float], None] | None = None,
        force_first_slug_timeout: bool = False,
        force_first_slug_delay: float = 0.0,
        azure_client: azure_storage.AzureStorageClient,
        utc_now: UtcNowFunc | None = None,
        on_error: Callable[[Exception], None] | None = None,
        interrupt_main_on_error: bool = False,
    ):
        self._heartbeat_path = storage_root / "_state" / "heartbeat.json"
        self._interval = max(0.05, float(interval_seconds))
        self._slug_timeout = float(slug_timeout_seconds) if slug_timeout_seconds else None
        self._log_writer = log_writer
        self._on_timeout = on_timeout
        self._azure_client = azure_client
        self._utc_now = utc_now or _utc_now
        self._on_error = on_error
        self._interrupt_main_on_error = interrupt_main_on_error

        self._lock = threading.Lock()
        self._current_slug: str | None = None
        self._slug_started_at: float | None = None
        self._last_persist: float = 0.0
        self._timed_out_slug: str | None = None

        self._force_first_slug_timeout = force_first_slug_timeout
        self._force_first_slug_delay = max(0.0, float(force_first_slug_delay))
        self._force_timeout_fired = False
        self._timers: list[threading.Timer] = []

        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._thread_exception: Exception | None = None  # Store background thread failures

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="heartbeat-monitor", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        with self._lock:
            for timer in self._timers:
                timer.cancel()
            self._timers.clear()
        if self._thread:
            self._thread.join(timeout=self._interval)

        # Check if background thread failed before final persist
        # This ensures upload failures during the thread's lifetime are surfaced
        self._raise_if_thread_failed()

        self._persist(force=True)

    def set_slug(self, slug: str | None) -> None:
        # Check if background thread failed - re-raise critical upload errors
        self._raise_if_thread_failed()

        with self._lock:
            self._current_slug = slug
            self._slug_started_at = time.monotonic() if slug else None
            self._timed_out_slug = None
            force_timeout = self._force_first_slug_timeout and not self._force_timeout_fired and slug is not None
            if force_timeout:
                self._force_timeout_fired = True
                timer = threading.Timer(
                    self._force_first_slug_delay,
                    self._trigger_timeout,
                    args=(slug, self._force_first_slug_delay),
                )
                timer.daemon = True
                self._timers.append(timer)
                timer.start()
        self._persist(force=True)

    def pulse(self) -> None:
        # Check if background thread failed - re-raise critical upload errors
        self._raise_if_thread_failed()
        self._persist()

    # Internal -----------------------------------------------------------------

    def _run(self) -> None:
        """Background thread loop that persists heartbeat and checks timeouts.

        Catches exceptions from _persist() (which may raise from _mirror())
        and stores them for re-raising in the main thread.
        """
        try:
            while not self._stop.wait(self._interval):
                self._persist()
                self._check_timeout()
        except Exception as exc:
            # Store exception for re-raising in main thread
            logger.error("Background heartbeat thread failed: %s", exc, exc_info=True)
            self._thread_exception = exc
            # Stop the thread - critical upload failure
            self._stop.set()
            # Notify main thread (fail-fast) or delegate to user callback
            self._notify_error(exc)

    def _raise_if_thread_failed(self) -> None:
        """Check if background thread encountered a critical failure and re-raise.

        This ensures that exceptions from the background thread (e.g., heartbeat
        upload failures) are propagated to the main thread on the next synchronous
        call (set_slug, pulse, stop).
        """
        if self._thread_exception is not None:
            exc = self._thread_exception
            self._thread_exception = None  # Clear to avoid double-raise
            raise exc

    def _notify_error(self, exc: Exception) -> None:
        """Notify caller about background failures immediately.

        If an explicit error callback was provided, invoke it. Optionally interrupt
        the main thread to fail-fast when configured, ensuring the job notices
        the critical error even when no further HeartbeatMonitor methods are
        called.
        """
        if self._on_error:
            try:
                self._on_error(exc)
            except Exception:  # pragma: no cover - defensive
                logger.warning("Heartbeat on_error callback failed", exc_info=True)
            return

        if self._interrupt_main_on_error:
            # Optional fail-fast: interrupt the main thread to raise a KeyboardInterrupt
            # on the next tick. This prevents silent background failures.
            try:
                _thread.interrupt_main()
            except Exception:  # pragma: no cover - defensive
                logger.warning("Failed to interrupt main thread after heartbeat error", exc_info=True)

    def _persist(self, force: bool = False) -> None:
        now_monotonic = time.monotonic()
        with self._lock:
            if not force and (now_monotonic - self._last_persist) < self._interval:
                return
            heartbeat = {"timestamp": self._utc_now(), "slug": self._current_slug}
            self._last_persist = now_monotonic
        ensure_parent(self._heartbeat_path)
        self._heartbeat_path.write_text(json.dumps(heartbeat, ensure_ascii=False) + "\n", encoding="utf-8")
        self._mirror(heartbeat)
        if self._log_writer:
            self._log_writer.write("heartbeat", **heartbeat)

    def _mirror(self, heartbeat: dict[str, Any]) -> None:
        """Upload heartbeat to Azure Blob Storage.

        Heartbeat files are CRITICAL for timeout monitoring. The timeout
        coordination system depends on heartbeat uploads to detect stuck jobs.
        Upload failures will propagate and fail the job.

        Args:
            heartbeat: Heartbeat metadata to upload.

        Raises:
            ConfigurationError: If Azure storage is not configured.
            Exception: If Azure upload fails (critical - no retry).
            RuntimeError: If client has no upload method available.
        """
        # CRITICAL: Heartbeat must upload or job fails
        # No try/catch - let errors propagate
        if not self._azure_client.is_configured():
            raise RuntimeError(
                f"Azure storage is not configured (mode={getattr(self._azure_client, '_mode', 'unknown')}). "
                f"Heartbeat uploads are CRITICAL - configure Azure storage or use strict mode."
            )
        logger.debug("Uploading critical heartbeat: %s", self._heartbeat_path)
        writer = getattr(self._azure_client, "write_json", None)
        if callable(writer):
            try:
                writer(self._heartbeat_path, heartbeat, raise_on_error=True)
            except TypeError:
                # Backward compatibility for clients without raise_on_error
                writer(self._heartbeat_path, heartbeat)
            logger.debug("Heartbeat uploaded successfully (write_json): %s", self._heartbeat_path)
            return

        uploader = getattr(self._azure_client, "upload_file", None)
        if callable(uploader):
            try:
                uploader(self._heartbeat_path, raise_on_error=True)
            except TypeError:
                uploader(self._heartbeat_path)
            logger.debug("Heartbeat uploaded successfully (upload_file): %s", self._heartbeat_path)
            return

        # No upload method available - this is a critical error
        raise RuntimeError(
            f"Azure client has neither write_json nor upload_file method. "
            f"Cannot upload critical heartbeat: {self._heartbeat_path}"
        )

    def _check_timeout(self) -> None:
        if self._slug_timeout is None:
            return
        with self._lock:
            slug = self._current_slug
            started_at = self._slug_started_at
            timed_out_slug = self._timed_out_slug
        if not slug or started_at is None:
            return
        elapsed = time.monotonic() - started_at
        if elapsed >= self._slug_timeout and slug != timed_out_slug:
            self._trigger_timeout(slug, elapsed)

    def _trigger_timeout(self, slug: str, elapsed: float) -> None:
        with self._lock:
            if self._timed_out_slug == slug:
                return
            self._timed_out_slug = slug
        if self._log_writer:
            self._log_writer.write("heartbeat_timeout", slug=slug, elapsed_seconds=round(elapsed, 2))
        if self._on_timeout:
            try:
                self._on_timeout(slug, elapsed)
            except Exception:  # pragma: no cover - defensive
                logger.warning("Heartbeat timeout callback failed for %s", slug, exc_info=True)


class TelemetryClient:
    """Structured telemetry logger backed by Application Insights instrumentation.

    Args:
        config: Telemetry configuration (required for explicit configuration).
        service_name: Service name for telemetry events (default: "infra_core").
        logger_name: Custom logger name (default: "{service_name}.azure.telemetry").

    Example:
        >>> config = TelemetryConfig.from_env_with_prefix("CRAWLER")
        >>> client = TelemetryClient(config=config, service_name="crawler")
        >>> client.track_event(TelemetryEvent.STARTED, batch_id="batch-1")
    """

    def __init__(
        self,
        *,
        config: TelemetryConfig | None = None,
        service_name: str = "infra_core",
        logger_name: str | None = None,
    ):
        if config is None:
            warnings.warn(
                "TelemetryClient() without explicit config is deprecated. "
                "Use TelemetryConfig.from_env() or TelemetryConfig.from_env_with_prefix() "
                "to create a config and pass it explicitly.",
                DeprecationWarning,
                stacklevel=2,
            )
            config = TelemetryConfig.from_env()

        self._config = config
        self._service_name = service_name
        self._logger = logging.getLogger(logger_name or f"{service_name}.azure.telemetry")
        self._enabled = config.enabled
        if self._enabled:
            self.track_event(
                TelemetryEvent.STARTED,
                metadata={"stage": "telemetry_initialized"},
            )

    def validate_event(self, name: TelemetryEvent | str) -> TelemetryEvent:
        """Return a normalized telemetry event or raise ``ValueError`` if invalid."""

        return _normalize_telemetry_event(name)

    def track_event(self, name: TelemetryEvent | str, **properties: Any) -> None:
        event = self.validate_event(name)
        payload = self._build_payload(event, dict(properties))
        if not self._enabled:
            return
        self._logger.info("telemetry_event %s", json.dumps(payload, ensure_ascii=False, default=str))

    def track_error(self, name: TelemetryEvent | str, **properties: Any) -> None:
        event = self.validate_event(name)
        payload = self._build_payload(event, dict(properties))
        if not self._enabled:
            return
        self._logger.error("telemetry_error %s", json.dumps(payload, ensure_ascii=False, default=str))

    def _build_payload(self, event: TelemetryEvent, properties: dict[str, Any]) -> dict[str, Any]:
        metadata: dict[str, Any] = dict(properties)
        service = _coerce_required_str(metadata.pop("service", self._service_name), field="service")
        batch_id = _coerce_optional_str(metadata.pop("batch_id", None), field="batch_id")
        job_id = _coerce_optional_str(metadata.pop("job_id", None), field="job_id")
        slug = _coerce_optional_str(metadata.pop("slug", None), field="slug")

        explicit_metadata = metadata.pop("metadata", None)
        metadata_payload: dict[str, Any] = {}
        if explicit_metadata is not None:
            if not isinstance(explicit_metadata, Mapping):
                raise ValueError("metadata must be a mapping when provided")
            metadata_payload = dict(explicit_metadata)
        if metadata:
            metadata_payload.update(metadata)

        for key in metadata_payload:
            if not isinstance(key, str):
                raise ValueError("metadata keys must be strings")

        payload: dict[str, Any] = {
            "service": service,
            "event": event.value,
            "batch_id": batch_id,
            "job_id": job_id,
            "slug": slug,
        }
        if metadata_payload:
            payload["metadata"] = metadata_payload
        return payload


def _normalize_telemetry_event(name: TelemetryEvent | str) -> TelemetryEvent:
    if isinstance(name, TelemetryEvent):
        return name
    event = str(name or "").strip().lower()
    if not event:
        raise ValueError("telemetry event name is required")
    for candidate in TelemetryEvent:
        if candidate.value == event:
            return candidate
    raise ValueError(
        f"telemetry event '{name}' is not one of: {', '.join(sorted(event.value for event in TelemetryEvent))}"
    )


def _coerce_optional_str(value: Any, *, field: str) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    raise ValueError(f"{field} must be a string when provided")


def _coerce_required_str(value: Any, *, field: str) -> str:
    result = _coerce_optional_str(value, field=field)
    if result is None:
        raise ValueError(f"{field} must be a non-empty string")
    return result


__all__ = [
    "RunLogWriter",
    "HeartbeatMonitor",
    "TelemetryClient",
    "TelemetryConfig",
    "TelemetryEvent",
    "TELEMETRY_EVENTS",
]
