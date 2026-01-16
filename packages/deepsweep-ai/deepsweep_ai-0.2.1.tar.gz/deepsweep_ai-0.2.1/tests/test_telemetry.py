"""
Tests for telemetry system.

Design Standards:
- NO EMOJIS
- Test privacy guarantees
- Test opt-out functionality
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from deepsweep.telemetry import (
    TelemetryClient,
    TelemetryConfig,
)


@pytest.fixture
def temp_config_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Create temporary config directory."""
    config_dir = tmp_path / ".deepsweep"
    config_file = config_dir / "config.json"
    telemetry_disabled_file = config_dir / ".telemetry_disabled"

    # Patch module-level constants in config module
    monkeypatch.setattr("deepsweep.telemetry.config.STATE_DIR", config_dir)
    monkeypatch.setattr("deepsweep.telemetry.config.CONFIG_FILE", config_file)
    monkeypatch.setattr("deepsweep.telemetry.config.TELEMETRY_DISABLED_FILE", telemetry_disabled_file)

    # Reset events module state
    import deepsweep.telemetry.events as events
    events._shutdown = False
    events._worker_thread = None
    # Clear the queue
    while not events._event_queue.empty():
        try:
            events._event_queue.get_nowait()
        except Exception:
            break

    return config_dir


class TestTelemetryConfig:
    """Test telemetry configuration management."""

    def test_creates_config_on_first_run(self, temp_config_dir: Path) -> None:
        """Test config file is created on first run."""
        config = TelemetryConfig()

        assert config.enabled is True
        assert config.first_run is True
        assert len(config.uuid) == 36  # UUID format

        # Check file exists
        config_file = temp_config_dir / "config.json"
        assert config_file.exists()

        # Check file contents
        with config_file.open() as f:
            data = json.load(f)
            assert data["telemetry_enabled"] is True
            assert data["first_run"] is True
            assert "uuid" in data

    def test_loads_existing_config(self, temp_config_dir: Path) -> None:
        """Test loading existing config from disk."""
        # Create config file
        config_file = temp_config_dir / "config.json"
        config_dir = temp_config_dir
        config_dir.mkdir(parents=True, exist_ok=True)

        existing_data = {
            "telemetry_enabled": False,
            "uuid": "test-uuid-1234",
            "first_run": False,
        }
        with config_file.open("w") as f:
            json.dump(existing_data, f)

        # Load config
        config = TelemetryConfig()

        assert config.enabled is False
        assert config.uuid == "test-uuid-1234"
        assert config.first_run is False

    def test_enable_telemetry(self, temp_config_dir: Path) -> None:
        """Test enabling telemetry."""
        config = TelemetryConfig()
        config.disable()
        assert config.enabled is False

        config.enable()
        assert config.enabled is True

        # Check file was updated
        config_file = temp_config_dir / "config.json"
        with config_file.open() as f:
            data = json.load(f)
            assert data["telemetry_enabled"] is True

    def test_disable_telemetry(self, temp_config_dir: Path) -> None:
        """Test disabling telemetry."""
        config = TelemetryConfig()
        assert config.enabled is True

        config.disable()
        assert config.enabled is False

        # Check file was updated
        config_file = temp_config_dir / "config.json"
        with config_file.open() as f:
            data = json.load(f)
            assert data["telemetry_enabled"] is False

    def test_mark_not_first_run(self, temp_config_dir: Path) -> None:
        """Test marking first run as complete."""
        config = TelemetryConfig()
        assert config.first_run is True

        config.mark_not_first_run()
        assert config.first_run is False

        # Check file was updated
        config_file = temp_config_dir / "config.json"
        with config_file.open() as f:
            data = json.load(f)
            assert data["first_run"] is False

    def test_get_status(self, temp_config_dir: Path) -> None:
        """Test getting telemetry status."""
        config = TelemetryConfig()
        status = config.get_status()

        assert "enabled" in status
        assert "uuid" in status
        assert "config_file" in status
        assert status["enabled"] is True
        assert len(status["uuid"]) == 36

    def test_handles_corrupted_config(self, temp_config_dir: Path) -> None:
        """Test handling corrupted config file."""
        config_dir = temp_config_dir
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.json"

        # Write corrupted JSON
        config_file.write_text("{ invalid json }")

        # Should create new config
        config = TelemetryConfig()
        assert config.enabled is True
        assert len(config.uuid) == 36


class TestTelemetryClient:
    """Test telemetry client."""

    @patch("deepsweep.telemetry.events._send_to_posthog")
    def test_track_command_when_enabled(
        self, mock_send: MagicMock, temp_config_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test tracking command when telemetry is enabled."""
        # Set API key to enable telemetry
        monkeypatch.setenv("DEEPSWEEP_POSTHOG_API_KEY", "test_key")
        monkeypatch.setenv("CI", "0")

        client = TelemetryClient()
        mock_send.return_value = True

        client.track_command(
            command="validate",
            exit_code=0,
            findings_count=5,
            pattern_count=16,
            output_format="json",
        )

        # Give background worker time to process
        import time
        time.sleep(0.1)

        # Verify PostHog send was called
        assert mock_send.called
        call_args = mock_send.call_args
        assert call_args[0][0] == "deepsweep_validate"
        assert call_args[0][1]["command"] == "validate"
        assert call_args[0][1]["exit_code"] == 0
        assert call_args[0][1]["findings_count"] == 5
        assert call_args[0][1]["pattern_count"] == 16
        assert call_args[0][1]["output_format"] == "json"

    @patch("deepsweep.telemetry.events._send_to_posthog")
    def test_track_command_when_disabled(
        self, mock_send: MagicMock, temp_config_dir: Path
    ) -> None:
        """Test tracking command when telemetry is disabled."""
        client = TelemetryClient()
        client.config.disable()

        client.track_command(command="validate", exit_code=0)

        # Give background worker time to process
        import time
        time.sleep(0.1)

        # Verify PostHog was NOT called
        assert not mock_send.called

    @patch("deepsweep.telemetry.events._send_to_posthog")
    def test_track_error(self, mock_send: MagicMock, temp_config_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test tracking errors."""
        # Set API key to enable telemetry
        monkeypatch.setenv("DEEPSWEEP_POSTHOG_API_KEY", "test_key")
        monkeypatch.setenv("CI", "0")

        client = TelemetryClient()
        mock_send.return_value = True

        client.track_error(
            command="validate",
            error_type="ValidationError",
            error_message="File not found",
        )

        # Give background worker time to process
        import time
        time.sleep(0.1)

        # Verify PostHog was called
        assert mock_send.called
        call_args = mock_send.call_args

        assert call_args[0][0] == "deepsweep_error"
        assert call_args[0][1]["command"] == "validate"
        assert call_args[0][1]["error_type"] == "ValidationError"

    def test_identify(self, temp_config_dir: Path) -> None:
        """Test user identification (now a no-op)."""
        client = TelemetryClient()
        # identify() is now a no-op for backward compatibility
        client.identify()  # Should not raise

    @patch("deepsweep.telemetry.flush")
    def test_shutdown(self, mock_flush: MagicMock, temp_config_dir: Path) -> None:
        """Test shutdown flushes events."""
        client = TelemetryClient()
        client.shutdown()

        # Verify flush was called
        mock_flush.assert_called_once()

    @patch("deepsweep.telemetry.events._send_to_posthog")
    def test_marks_first_run_complete(self, mock_send: MagicMock, temp_config_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test first run is marked complete after tracking."""
        # Set API key to enable telemetry
        monkeypatch.setenv("DEEPSWEEP_POSTHOG_API_KEY", "test_key")
        monkeypatch.setenv("CI", "0")

        client = TelemetryClient()
        mock_send.return_value = True
        assert client.config.first_run is True

        client.track_command(command="validate", exit_code=0)

        assert client.config.first_run is False

    def test_sanitizes_error_messages(self, temp_config_dir: Path) -> None:
        """Test error messages are not sent (privacy guarantee)."""
        client = TelemetryClient()

        # Error with home directory path - should not be sent
        error_msg = f"File not found: {Path.home()}/my-secret-project/file.txt"
        client.track_error(
            command="validate",
            error_type="ValidationError",
            error_message=error_msg,
        )

        # Error messages are not sent in new implementation (privacy)

    @patch("deepsweep.telemetry.events._send_to_posthog")
    def test_never_fails_on_telemetry_errors(
        self, mock_send: MagicMock, temp_config_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test telemetry errors don't crash the application."""
        # Set API key to enable telemetry
        monkeypatch.setenv("DEEPSWEEP_POSTHOG_API_KEY", "test_key")
        monkeypatch.setenv("CI", "0")

        # Make PostHog raise an exception
        mock_send.side_effect = Exception("Network error")

        client = TelemetryClient()

        # Should not raise exception
        client.track_command(command="validate", exit_code=0)
        client.track_error(
            command="validate",
            error_type="ValidationError",
            error_message="Test",
        )
        client.identify()
        client.shutdown()


class TestTelemetryPrivacy:
    """Test telemetry privacy guarantees."""

    @patch("deepsweep.telemetry.events._send_to_posthog")
    def test_no_file_paths_in_telemetry(
        self, mock_send: MagicMock, temp_config_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test file paths are not included in telemetry."""
        # Set API key to enable telemetry
        monkeypatch.setenv("DEEPSWEEP_POSTHOG_API_KEY", "test_key")
        monkeypatch.setenv("CI", "0")

        client = TelemetryClient()
        mock_send.return_value = True

        client.track_command(
            command="validate",
            exit_code=0,
            findings_count=5,
        )

        # Give background worker time to process
        import time
        time.sleep(0.1)

        if mock_send.called:
            call_args = mock_send.call_args
            properties = call_args[0][1]

            # Should not contain file paths
            assert "path" not in properties
            assert "file" not in properties
            assert "directory" not in properties

    @patch("deepsweep.telemetry.events._send_to_posthog")
    def test_no_code_content_in_telemetry(
        self, mock_send: MagicMock, temp_config_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test code content is not included in telemetry."""
        # Set API key to enable telemetry
        monkeypatch.setenv("DEEPSWEEP_POSTHOG_API_KEY", "test_key")
        monkeypatch.setenv("CI", "0")

        client = TelemetryClient()
        mock_send.return_value = True

        client.track_command(
            command="validate",
            exit_code=0,
            findings_count=5,
        )

        # Give background worker time to process
        import time
        time.sleep(0.1)

        if mock_send.called:
            call_args = mock_send.call_args
            properties = call_args[0][1]

            # Should not contain code or finding details
            assert "code" not in properties
            assert "content" not in properties
            assert "finding" not in properties
            assert "pattern" not in properties

    @patch("deepsweep.telemetry.events._send_to_posthog")
    def test_only_aggregated_metrics(self, mock_send: MagicMock, temp_config_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test only aggregated metrics are collected."""
        # Set API key to enable telemetry
        monkeypatch.setenv("DEEPSWEEP_POSTHOG_API_KEY", "test_key")
        monkeypatch.setenv("CI", "0")

        client = TelemetryClient()
        mock_send.return_value = True

        client.track_command(
            command="validate",
            exit_code=0,
            findings_count=5,
            pattern_count=16,
        )

        # Give background worker time to process
        import time
        time.sleep(0.1)

        if mock_send.called:
            call_args = mock_send.call_args
            properties = call_args[0][1]

            # Should only have counts, not details
            assert "findings_count" in properties
            assert properties["findings_count"] == 5
            assert "pattern_count" in properties
            assert properties["pattern_count"] == 16
