"""
PostHog event tracking.

Event schemas match official DeepSweep telemetry specification.
All events are non-blocking and fail silently.
"""

import atexit
import platform
import queue
import threading
from datetime import datetime, timezone
from typing import Any

from . import config

# Event queue for async processing
_event_queue: queue.Queue = queue.Queue(maxsize=100)
_worker_thread: threading.Thread | None = None
_shutdown = False


def _get_base_properties() -> dict[str, Any]:
    """Get base properties included in all events."""
    from deepsweep import __version__

    return {
        "version": __version__,
        "os": platform.system(),
        "python_version": platform.python_version(),
    }


def _send_to_posthog(event_name: str, properties: dict[str, Any]) -> bool:
    """
    Send event to PostHog. Blocking call.

    Returns True on success, False on failure.
    """
    import requests

    api_key = config.get_posthog_api_key()
    host = config.get_posthog_host()

    if not api_key:
        return False

    try:
        payload = {
            "api_key": api_key,
            "event": event_name,
            "distinct_id": config.get_anonymous_id(),
            "properties": {
                **_get_base_properties(),
                **properties,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        response = requests.post(
            f"{host}/capture/",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=3,
        )

        return response.status_code == 200

    except Exception:
        return False


def _worker():
    """Background worker that processes event queue."""
    global _shutdown

    while not _shutdown:
        try:
            event_name, properties = _event_queue.get(timeout=1)
            _send_to_posthog(event_name, properties)
            _event_queue.task_done()
        except queue.Empty:
            continue
        except Exception:
            continue


def _ensure_worker():
    """Start background worker if not running."""
    global _worker_thread

    if _worker_thread is None or not _worker_thread.is_alive():
        _worker_thread = threading.Thread(target=_worker, daemon=True)
        _worker_thread.start()


def track(event_name: str, properties: dict[str, Any] | None = None) -> None:
    """
    Track an event asynchronously.

    This function returns immediately. Events are sent in background.
    Failures are silent - never impacts user experience.

    Args:
        event_name: Event name (e.g., 'deepsweep_validate')
        properties: Additional properties (no PII allowed)
    """
    if not config.is_enabled():
        return

    props = properties or {}

    try:
        _ensure_worker()
        _event_queue.put_nowait((event_name, props))
    except queue.Full:
        pass  # Drop event if queue full - never block


def track_validate(
    duration_ms: int,
    exit_code: int,
    findings_count: int,
    pattern_count: int,
    output_format: str = "text",
    first_run: bool = False,
    mcp_included: bool = False,
) -> None:
    """
    Track validation event with standard schema.

    Event: deepsweep_validate
    """
    track("deepsweep_validate", {
        "command": "validate",
        "duration_ms": duration_ms,
        "exit_code": exit_code,
        "findings_count": findings_count,
        "pattern_count": pattern_count,
        "output_format": output_format,
        "first_run": first_run,
        "mcp_included": mcp_included,
    })


def track_error(
    command: str,
    error_type: str,
) -> None:
    """
    Track error event with standard schema.

    Event: deepsweep_error
    """
    track("deepsweep_error", {
        "command": command,
        "error_type": error_type,
    })


def track_badge(
    output_format: str,
    exit_code: int,
) -> None:
    """
    Track badge generation event.

    Event: deepsweep_badge
    """
    track("deepsweep_badge", {
        "command": "badge",
        "output_format": output_format,
        "exit_code": exit_code,
    })


def track_patterns(
    pattern_count: int,
) -> None:
    """
    Track patterns list event.

    Event: deepsweep_patterns
    """
    track("deepsweep_patterns", {
        "command": "patterns",
        "pattern_count": pattern_count,
    })


def flush(timeout: float = 2.0) -> None:
    """
    Wait for pending events to send.

    Call before exit to ensure events are delivered.
    """
    global _shutdown

    _shutdown = True  # Signal worker to stop

    try:
        # Wait for queue to empty with timeout
        import time
        start = time.time()
        while not _event_queue.empty() and (time.time() - start) < timeout:
            time.sleep(0.1)
    except Exception:
        pass


# Register flush on exit
atexit.register(flush)
