"""
Telemetry configuration.

Environment variables:
- DEEPSWEEP_POSTHOG_API_KEY: PostHog project API key
- DEEPSWEEP_POSTHOG_HOST: PostHog host (default: https://us.i.posthog.com)
- DEEPSWEEP_OFFLINE: Disable all telemetry (for air-gapped environments)
- DEEPSWEEP_TELEMETRY_DISABLED: Disable optional telemetry only
- DO_NOT_TRACK: Standard opt-out signal
"""

import hashlib
import json
import os
import platform
from pathlib import Path
from typing import Any

# Configuration
DEFAULT_POSTHOG_API_KEY = "phc_VrTXIhk3NCR3fQuL2TMdQyr1ct3ckj9J0eFD0PeU7s9"
DEFAULT_POSTHOG_HOST = "https://us.i.posthog.com"

# State directory for persistent settings
STATE_DIR = Path.home() / ".deepsweep"
TELEMETRY_DISABLED_FILE = STATE_DIR / ".telemetry_disabled"
CONFIG_FILE = STATE_DIR / "config.json"

# Cached values
_anonymous_id: str | None = None


def get_posthog_api_key() -> str | None:
    """
    Get PostHog API key from environment or use default.

    Priority:
    1. DEEPSWEEP_POSTHOG_API_KEY environment variable (for custom projects)
    2. Default hardcoded key (for standard DeepSweep telemetry)

    Note: PostHog API keys are write-only and safe to embed in client code.
    """
    return os.environ.get("DEEPSWEEP_POSTHOG_API_KEY", DEFAULT_POSTHOG_API_KEY)


def get_posthog_host() -> str:
    """Get PostHog host from environment or default."""
    return os.environ.get("DEEPSWEEP_POSTHOG_HOST", DEFAULT_POSTHOG_HOST)


def is_offline() -> bool:
    """
    Check if fully offline mode is enabled.

    When True, ALL telemetry is disabled including essential signals.
    Used for air-gapped or highly regulated environments.
    """
    offline_val = os.environ.get("DEEPSWEEP_OFFLINE", "").lower()
    return offline_val in ("1", "true", "yes")


def is_enabled() -> bool:
    """
    Check if optional telemetry (PostHog) is enabled.

    Enabled by default with hardcoded API key.

    Disabled when:
    - DEEPSWEEP_OFFLINE=1 (fully offline)
    - DEEPSWEEP_TELEMETRY_DISABLED=1
    - DO_NOT_TRACK=1 (standard signal)
    - User ran `deepsweep telemetry disable`
    - Running in CI environment
    """
    # Check offline mode first
    if is_offline():
        return False

    # Check environment disable flags
    disable_vars = [
        "DEEPSWEEP_TELEMETRY_DISABLED",
        "DO_NOT_TRACK",
    ]
    for var in disable_vars:
        if os.environ.get(var, "").lower() in ("1", "true", "yes"):
            return False

    # Check CI environment (disable by default in CI)
    if os.environ.get("CI", "").lower() in ("1", "true", "yes"):
        return False

    # Check user preference file
    return not TELEMETRY_DISABLED_FILE.exists()

    return True


def get_anonymous_id() -> str:
    """
    Generate stable anonymous identifier.

    Based on machine characteristics, NOT user identity.
    Same machine = same ID across sessions.
    """
    global _anonymous_id

    if _anonymous_id is None:
        # Combine stable machine factors
        factors = [
            platform.node(),      # hostname
            platform.machine(),   # CPU architecture
            platform.system(),    # OS name
            str(Path.home()),     # home directory path
        ]
        combined = "|".join(factors)
        _anonymous_id = hashlib.sha256(combined.encode()).hexdigest()

    return _anonymous_id


def enable_telemetry() -> None:
    """Enable optional telemetry (remove disable marker)."""
    if TELEMETRY_DISABLED_FILE.exists():
        TELEMETRY_DISABLED_FILE.unlink()


def disable_telemetry() -> None:
    """Disable optional telemetry (create disable marker)."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    TELEMETRY_DISABLED_FILE.touch()


def get_telemetry_status() -> dict:
    """Get current telemetry status for diagnostics."""
    return {
        "enabled": is_enabled(),
        "offline": is_offline(),
        "api_key_configured": bool(get_posthog_api_key()),
        "host": get_posthog_host(),
        "user_disabled": TELEMETRY_DISABLED_FILE.exists(),
        "anonymous_id_prefix": get_anonymous_id()[:8],
    }


# Legacy TelemetryConfig class for backward compatibility
class TelemetryConfig:
    """Manages telemetry configuration and preferences (legacy compatibility)."""

    def __init__(self) -> None:
        self._config: dict[str, Any] = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        if not CONFIG_FILE.exists():
            import uuid
            config = {
                "telemetry_enabled": True,
                "offline_mode": False,
                "uuid": str(uuid.uuid4()),
                "first_run": True,
            }
            self._save_config(config)
            return config

        try:
            with CONFIG_FILE.open("r") as f:
                loaded = json.load(f)
                # Ensure uuid exists
                if "uuid" not in loaded:
                    import uuid
                    loaded["uuid"] = str(uuid.uuid4())
                    self._save_config(loaded)
                return loaded
        except (json.JSONDecodeError, OSError):
            import uuid
            config = {
                "telemetry_enabled": True,
                "offline_mode": False,
                "uuid": str(uuid.uuid4()),
                "first_run": True,
            }
            self._save_config(config)
            return config

    def _save_config(self, config: dict[str, Any]) -> None:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        with CONFIG_FILE.open("w") as f:
            json.dump(config, f, indent=2)

    @property
    def enabled(self) -> bool:
        """Check if optional telemetry (PostHog) is enabled."""
        return bool(self._config.get("telemetry_enabled", True))

    @property
    def offline_mode(self) -> bool:
        """Check if fully offline (disables ALL telemetry)."""
        return bool(self._config.get("offline_mode", False)) or is_offline()

    @property
    def uuid(self) -> str:
        """Get anonymous user UUID."""
        value = self._config.get("uuid")
        return value if isinstance(value, str) and value else "unknown"

    @property
    def first_run(self) -> bool:
        """Check if this is first run."""
        return bool(self._config.get("first_run", False))

    def enable(self) -> None:
        self._config["telemetry_enabled"] = True
        self._save_config(self._config)
        enable_telemetry()

    def disable(self) -> None:
        """Disable optional telemetry (PostHog). Threat signals still send."""
        self._config["telemetry_enabled"] = False
        self._save_config(self._config)
        disable_telemetry()

    def mark_not_first_run(self) -> None:
        self._config["first_run"] = False
        self._save_config(self._config)

    def get_status(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "offline_mode": self.offline_mode,
            "uuid": self.uuid,
            "config_file": str(CONFIG_FILE),
        }
