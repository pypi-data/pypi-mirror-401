"""Tests for HeartbeatMonitor critical upload behavior."""

from unittest.mock import Mock

import pytest
from azure.core.exceptions import ServiceRequestError

from infra_core.azure.monitoring import HeartbeatMonitor


class TestHeartbeatCriticalUpload:
    """Test that heartbeat upload failures propagate (critical)."""

    def test_heartbeat_upload_success(self, tmp_path):
        """Successful heartbeat upload should not raise."""
        storage_root = tmp_path / "storage"

        mock_client = Mock()
        mock_client.is_configured.return_value = True
        mock_client.write_json = None  # Force fallback to upload_file
        mock_client.upload_file.return_value = None  # Success

        monitor = HeartbeatMonitor(
            storage_root,
            interval_seconds=1.0,
            azure_client=mock_client,
        )

        # Set slug triggers persist which triggers _mirror
        monitor.set_slug("test-slug")

        # Verify upload was attempted
        assert mock_client.upload_file.call_count == 1
        called_path = mock_client.upload_file.call_args[0][0]
        assert "heartbeat.json" in str(called_path)

    def test_heartbeat_upload_failure_propagates(self, tmp_path):
        """Heartbeat upload failure should propagate (critical)."""
        storage_root = tmp_path / "storage"

        mock_client = Mock()
        mock_client.is_configured.return_value = True
        mock_client.write_json = None  # Force fallback to upload_file

        # Upload fails with Azure error
        exc = ServiceRequestError("Connection timeout")
        mock_client.upload_file.side_effect = exc

        monitor = HeartbeatMonitor(
            storage_root,
            interval_seconds=1.0,
            azure_client=mock_client,
        )

        # Upload failure should propagate
        with pytest.raises(ServiceRequestError, match="Connection timeout"):
            monitor.set_slug("test-slug")

    def test_heartbeat_write_json_failure_propagates(self, tmp_path):
        """Heartbeat write_json failure should propagate."""
        storage_root = tmp_path / "storage"

        mock_client = Mock()
        mock_client.is_configured.return_value = True

        # write_json exists but fails
        exc = ServiceRequestError("Write failed")
        mock_client.write_json.side_effect = exc

        monitor = HeartbeatMonitor(
            storage_root,
            interval_seconds=1.0,
            azure_client=mock_client,
        )

        # Upload failure should propagate
        with pytest.raises(ServiceRequestError, match="Write failed"):
            monitor.set_slug("test-slug")


def test_heartbeat_unconfigured_client_skips_upload(tmp_path):
    """Unconfigured client should skip upload without error."""
    storage_root = tmp_path / "storage"

    mock_client = Mock()
    mock_client.is_configured.return_value = False

    monitor = HeartbeatMonitor(
        storage_root,
        interval_seconds=1.0,
        azure_client=mock_client,
    )

    with pytest.raises(RuntimeError, match="not configured|mode"):
        monitor.set_slug("test-slug")

    # Upload should not be attempted
    assert mock_client.upload_file.call_count == 0

    def test_heartbeat_pulse_upload_failure_propagates(self, tmp_path):
        """pulse() triggering upload failure should propagate."""
        import time

        storage_root = tmp_path / "storage"

        mock_client = Mock()
        mock_client.is_configured.return_value = True
        mock_client.write_json = None  # Force fallback to upload_file

        # First call (set_slug) succeeds, second call (pulse) fails
        exc = ServiceRequestError("Upload failed")
        mock_client.upload_file.side_effect = [None, exc]

        monitor = HeartbeatMonitor(
            storage_root,
            interval_seconds=0.05,  # Very short interval
            azure_client=mock_client,
        )

        # set_slug succeeds
        monitor.set_slug("test-slug")

        # Wait for interval to pass
        time.sleep(0.06)

        # pulse() should trigger upload and fail
        with pytest.raises(ServiceRequestError, match="Upload failed"):
            monitor.pulse()

    def test_heartbeat_stop_upload_failure_propagates(self, tmp_path):
        """stop() triggering upload failure should propagate."""
        storage_root = tmp_path / "storage"

        mock_client = Mock()
        mock_client.is_configured.return_value = True
        mock_client.write_json = None  # Force fallback to upload_file

        # First call succeeds, stop() call fails
        exc = ServiceRequestError("Upload failed")
        mock_client.upload_file.side_effect = [None, exc]

        monitor = HeartbeatMonitor(
            storage_root,
            interval_seconds=1.0,
            azure_client=mock_client,
        )

        # set_slug succeeds
        monitor.set_slug("test-slug")

        # stop() should trigger upload and fail
        with pytest.raises(ServiceRequestError, match="Upload failed"):
            monitor.stop()


class TestHeartbeatBackwardCompatibility:
    """Test that heartbeat changes don't break existing functionality."""

    def test_heartbeat_with_log_writer(self, tmp_path):
        """HeartbeatMonitor with log_writer should log events."""
        storage_root = tmp_path / "storage"

        mock_client = Mock()
        mock_client.is_configured.return_value = True
        mock_client.upload_file.return_value = None

        mock_log_writer = Mock()

        monitor = HeartbeatMonitor(
            storage_root,
            interval_seconds=1.0,
            azure_client=mock_client,
            log_writer=mock_log_writer,
        )

        monitor.set_slug("test-slug")

        # Verify log was written
        assert mock_log_writer.write.call_count == 1
        call_args = mock_log_writer.write.call_args
        assert call_args[0][0] == "heartbeat"
        assert call_args[1]["slug"] == "test-slug"

    def test_background_failure_interrupts_main(self, tmp_path, monkeypatch):
        """Background thread failures should interrupt the main thread (fail-fast)."""
        storage_root = tmp_path / "storage"

        mock_client = Mock()
        mock_client.is_configured.return_value = True
        mock_client.write_json = None  # Force fallback to upload_file
        mock_client.upload_file.side_effect = ServiceRequestError("Upload failed")

        interrupted: list[bool] = []
        from infra_core.azure import monitoring

        monkeypatch.setattr(
            monitoring._thread,
            "interrupt_main",
            lambda: interrupted.append(True),
            raising=False,
        )

        monitor = HeartbeatMonitor(
            storage_root,
            interval_seconds=0.05,
            azure_client=mock_client,
            interrupt_main_on_error=True,
        )

        monitor.start()
        try:
            # Allow background thread to attempt upload and fail
            import time

            deadline = time.monotonic() + 1.0
            while mock_client.upload_file.call_count == 0 and time.monotonic() < deadline:
                time.sleep(0.01)

            assert mock_client.upload_file.call_count >= 1, "Background upload never started"

            # stop() should re-raise the stored exception
            with pytest.raises(ServiceRequestError, match="Upload failed"):
                monitor.stop()
        finally:
            # Ensure we don't leave a running thread in case of assertion failure
            monitor._stop.set()

        deadline = time.monotonic() + 0.5
        while not interrupted and time.monotonic() < deadline:
            time.sleep(0.01)

        assert interrupted, "Main thread should be interrupted on background failure"
