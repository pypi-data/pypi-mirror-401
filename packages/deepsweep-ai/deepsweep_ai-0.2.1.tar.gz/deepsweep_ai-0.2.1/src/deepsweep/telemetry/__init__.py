"""
DeepSweep Two-Tier Telemetry System

TIER 1 - Essential (Always On):
  Threat Intelligence - Powers the community security ecosystem
  - Pattern effectiveness data
  - Attack trend signals
  - Zero-day detection
  - Network effect reliability

TIER 2 - Optional (Can Disable):
  Product Analytics - PostHog for funnel optimization
  - Activation metrics
  - Retention tracking
  - Feature usage
  - Performance data

Privacy Guarantees:
- NO source code, file paths, or file contents
- NO repository names or user identities
- NO API keys, tokens, or secrets
- Anonymized machine ID only
"""

import contextlib
import time
from typing import Any

# Import public API from submodules
from .config import (
    TelemetryConfig,
    disable_telemetry,
    enable_telemetry,
    get_anonymous_id,
    get_telemetry_status,
    is_enabled,
    is_offline,
)
from .events import (
    flush,
    track,
    track_badge,
    track_error,
    track_patterns,
    track_validate,
)
from .threat import ThreatSignal, create_threat_signal, send_threat_signal

__all__ = [
    "TelemetryClient",
    "ThreatSignal",
    "create_threat_signal",
    "disable_telemetry",
    "enable_telemetry",
    "flush",
    "get_anonymous_id",
    "get_telemetry_client",
    "get_telemetry_status",
    "is_enabled",
    "is_offline",
    "send_threat_signal",
    "track",
    "track_badge",
    "track_error",
    "track_patterns",
    "track_validate",
]


# =============================================================================
# LEGACY TELEMETRY CLIENT (BACKWARD COMPATIBILITY)
# =============================================================================


class TelemetryClient:
    """
    Legacy telemetry client for backward compatibility.

    New code should use the module-level functions instead:
    - telemetry.track_validate()
    - telemetry.track_error()
    - telemetry.flush()
    """

    def __init__(self) -> None:
        self.config = TelemetryConfig()
        self._start_time: float = time.time()

    def track_command(
        self,
        command: str,
        exit_code: int = 0,
        findings_count: int | None = None,
        pattern_count: int | None = None,
        output_format: str | None = None,
        score: int | None = None,
        grade: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Track command execution (legacy API)."""
        duration_ms = int((time.time() - self._start_time) * 1000)

        # ESSENTIAL TIER: Send threat signal for validate commands
        if command == "validate" and not self.config.offline_mode:
            signal = create_threat_signal(
                findings_count=findings_count or 0,
                score=score or 0,
                grade=grade or "",
                duration_ms=duration_ms,
            )
            send_threat_signal(signal, offline_mode=self.config.offline_mode)

        # OPTIONAL TIER: PostHog analytics
        if command == "validate" and findings_count is not None and pattern_count is not None:
            track_validate(
                duration_ms=duration_ms,
                exit_code=exit_code,
                findings_count=findings_count,
                pattern_count=pattern_count,
                output_format=output_format or "text",
                first_run=self.config.first_run,
                mcp_included=kwargs.get("mcp_included", False),
            )
        elif command == "badge":
            track_badge(
                output_format=output_format or "svg",
                exit_code=exit_code,
            )
        elif command == "patterns" and pattern_count is not None:
            track_patterns(
                pattern_count=pattern_count,
            )
        else:
            # Generic tracking for other commands
            track(f"deepsweep_{command}", {
                "command": command,
                "exit_code": exit_code,
                "duration_ms": duration_ms,
                **kwargs,
            })

        # Mark first run complete
        if self.config.first_run:
            self.config.mark_not_first_run()

    def track_error(
        self,
        command: str,
        error_type: str,
        error_message: str | None = None,
    ) -> None:
        """Track error (legacy API)."""
        # Privacy guarantee: never transmit message contents
        _ = error_message
        track_error(command=command, error_type=error_type)

    def identify(self) -> None:
        """Identify user (legacy API - now a no-op)."""
        # PostHog identify is handled automatically by events module
        pass

    def shutdown(self) -> None:
        """Flush pending events (legacy API)."""
        with contextlib.suppress(Exception):
            flush()


_client: TelemetryClient | None = None


def get_telemetry_client() -> TelemetryClient:
    """Get singleton telemetry client (legacy API)."""
    global _client
    if _client is None:
        _client = TelemetryClient()
    return _client
