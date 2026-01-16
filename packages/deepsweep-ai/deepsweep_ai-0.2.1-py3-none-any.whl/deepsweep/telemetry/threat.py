"""
DeepSweep Threat Intelligence (Essential Tier).

This module handles the essential tier of telemetry - threat intelligence signals
that power the community security ecosystem. This tier is always active unless
offline mode is enabled.

Privacy Guarantees:
- NO source code, file paths, or file contents
- NO repository names or user identities
- NO API keys, tokens, or secrets
- Anonymized machine ID only (SHA256 hash)
"""

import contextlib
import hashlib
import json
import os
import platform
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Final
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from deepsweep.constants import VERSION

# Threat Intelligence endpoint (Essential tier)
THREAT_INTEL_ENDPOINT: Final[str] = os.environ.get(
    "DEEPSWEEP_INTEL_ENDPOINT", "https://api.deepsweep.ai/v1/signal"
)

# Request timeout (never block CLI)
REQUEST_TIMEOUT: Final[float] = 2.0

# Install ID cache
_install_id_cache: str | None = None


def _get_install_id() -> str:
    """
    Get anonymized install ID (SHA-256 hash of machine identifiers).

    Used only for:
    - Deduplication in analytics
    - Cohort analysis (not individual tracking)

    Cannot be reversed to identify user or machine.
    """
    global _install_id_cache

    if _install_id_cache is not None:
        return _install_id_cache

    components = [
        platform.node(),
        platform.machine(),
        platform.processor(),
        str(uuid.getnode()),
    ]

    raw = "|".join(components).encode()
    _install_id_cache = hashlib.sha256(raw).hexdigest()[:32]
    return _install_id_cache


@dataclass
class ThreatSignal:
    """
    Anonymized threat intelligence signal.

    NEVER includes: file paths, code, repo names, user identity
    """

    # Pattern intelligence (THE reliability)
    pattern_ids: list[str] = field(default_factory=list)
    cve_matches: list[str] = field(default_factory=list)
    severity_counts: dict[str, int] = field(default_factory=dict)

    # Tool context (aggregate risk profiles)
    tool_context: list[str] = field(default_factory=list)
    file_types: list[str] = field(default_factory=list)

    # Validation metadata
    score: int = 0
    grade: str = ""
    finding_count: int = 0
    file_count: int = 0
    duration_ms: int = 0

    # Environment
    cli_version: str = ""
    python_version: str = ""
    os_type: str = ""
    is_ci: bool = False
    ci_provider: str | None = None

    # Temporal
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # Anonymized identity (for deduplication only)
    install_id: str = field(default_factory=_get_install_id)
    session_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])


def _detect_ci() -> tuple[bool, str | None]:
    """Detect if running in CI environment."""
    ci_indicators = {
        "GITHUB_ACTIONS": "github",
        "GITLAB_CI": "gitlab",
        "CIRCLECI": "circleci",
        "JENKINS_URL": "jenkins",
        "TRAVIS": "travis",
        "BUILDKITE": "buildkite",
        "AZURE_PIPELINES": "azure",
        "BITBUCKET_PIPELINES": "bitbucket",
        "CI": None,
    }

    for env_var, provider in ci_indicators.items():
        if os.environ.get(env_var):
            return True, provider

    return False, None


def _send_async(url: str, data: dict[str, Any], timeout: float = REQUEST_TIMEOUT) -> None:
    """Send data asynchronously (fire and forget)."""

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return  # silently drop invalid schemes

    def _do_send() -> None:
        with contextlib.suppress(Exception):
            request = Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": f"deepsweep-cli/{VERSION}",
                },
                method="POST",
            )
            with urlopen(request, timeout=timeout):  # nosec
                pass

    threading.Thread(target=_do_send, daemon=True).start()


def send_threat_signal(signal: ThreatSignal, offline_mode: bool = False) -> None:
    """
    ESSENTIAL TIER - Always sent unless fully offline.

    This sends anonymized threat intelligence to help the community.
    """
    if offline_mode:
        return

    _send_async(
        THREAT_INTEL_ENDPOINT,
        {
            "event": "threat_signal",
            "version": "1",
            **asdict(signal),
        },
    )


def create_threat_signal(
    findings_count: int = 0,
    score: int = 0,
    grade: str = "",
    duration_ms: int = 0,
    pattern_ids: list[str] | None = None,
    cve_matches: list[str] | None = None,
    severity_counts: dict[str, int] | None = None,
) -> ThreatSignal:
    """Create a threat signal from validation results."""
    is_ci, ci_provider = _detect_ci()

    return ThreatSignal(
        pattern_ids=pattern_ids or [],
        cve_matches=cve_matches or [],
        severity_counts=severity_counts or {},
        tool_context=[],
        file_types=[],
        score=score,
        grade=grade,
        finding_count=findings_count,
        file_count=0,
        duration_ms=duration_ms,
        cli_version=VERSION,
        python_version=platform.python_version(),
        os_type=platform.system().lower(),
        is_ci=is_ci,
        ci_provider=ci_provider,
    )
