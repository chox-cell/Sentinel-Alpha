import os


DEFAULT_MAX_CANDIDATES_PER_WEBHOOK = 50
DEFAULT_MAX_EVALUATIONS_PER_WEBHOOK = 10
DEFAULT_MAX_PAYLOAD_BYTES_WARN = 500000
DEFAULT_MAX_PAYLOAD_BYTES_HARD = 3000000


def _get_env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return default
    return value if value > 0 else default


def get_ingestion_limits() -> dict:
    return {
        "max_candidates_per_webhook": _get_env_int(
            "SENTINEL_MAX_CANDIDATES_PER_WEBHOOK",
            DEFAULT_MAX_CANDIDATES_PER_WEBHOOK,
        ),
        "max_evaluations_per_webhook": _get_env_int(
            "SENTINEL_MAX_EVALUATIONS_PER_WEBHOOK",
            DEFAULT_MAX_EVALUATIONS_PER_WEBHOOK,
        ),
        "max_payload_bytes_warn": _get_env_int(
            "SENTINEL_MAX_PAYLOAD_BYTES_WARN",
            DEFAULT_MAX_PAYLOAD_BYTES_WARN,
        ),
        "max_payload_bytes_hard": _get_env_int(
            "SENTINEL_MAX_PAYLOAD_BYTES_HARD",
            DEFAULT_MAX_PAYLOAD_BYTES_HARD,
        ),
    }
