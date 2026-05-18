"""In-process usage counters for public /public/metrics (no PII, no env leak)."""

from __future__ import annotations

import threading
from datetime import datetime, timezone

_LOCK = threading.Lock()
_UNPAID_DISCOVERY_402 = 0
_PAID_REQUESTS = 0
_LAST_UPDATED: str | None = None


def _touch() -> None:
    global _LAST_UPDATED
    _LAST_UPDATED = datetime.now(timezone.utc).isoformat()


def record_unpaid_discovery_402() -> None:
    global _UNPAID_DISCOVERY_402
    with _LOCK:
        _UNPAID_DISCOVERY_402 += 1
        _touch()


def record_paid_request() -> None:
    global _PAID_REQUESTS
    with _LOCK:
        _PAID_REQUESTS += 1
        _touch()


def reset_public_usage_metrics() -> None:
    """Test isolation only."""
    global _UNPAID_DISCOVERY_402, _PAID_REQUESTS, _LAST_UPDATED
    with _LOCK:
        _UNPAID_DISCOVERY_402 = 0
        _PAID_REQUESTS = 0
        _LAST_UPDATED = None


def get_public_usage_metrics() -> dict:
    with _LOCK:
        return {
            "unpaid_discovery_402_count": _UNPAID_DISCOVERY_402,
            "paid_request_count": _PAID_REQUESTS,
            "last_updated": _LAST_UPDATED,
            "scope": "process_lifetime",
            "note": (
                "Counters since this API process started. "
                "Not authoritative billing or revenue data."
            ),
        }
