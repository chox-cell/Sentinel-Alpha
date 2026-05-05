from __future__ import annotations

import hashlib
from datetime import datetime, timezone


_ALLOWED_FIELDS = {
    "verified_source_status",
    "abi_available",
    "abi_function_names",
    "abi_selector_count",
    "provider_name",
    "fetched_at",
    "ttl_seconds",
    "source_fetch_error_type",
}

_FORBIDDEN_MARKERS = {
    "api_key",
    "private_key",
    "seed_phrase",
    "authorization",
    "cookie",
    "payment_signature",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_abi_source_cache_status(config=None) -> dict:
    cfg = config if isinstance(config, dict) else {}
    enabled = cfg.get("enabled")
    if enabled in {True, 1, "1", "true", "True", "on", "ON"}:
        mode = "not_configured"
    elif enabled in {False, 0, "0", "false", "False", "off", "OFF"}:
        mode = "disabled"
    else:
        mode = "not_configured"

    return {
        "cache_enabled": False,
        "cache_mode": mode,
        "redis_required": False,
        "database_required": False,
        "read_attempted": False,
        "write_attempted": False,
        "notes": [
            "ABI/source cache boundary is disabled by default.",
            "REDIS_URL is not required by default.",
            "DATABASE_URL is not required by default.",
        ],
    }


def build_abi_source_cache_key(address, chain, provider_name) -> str:
    addr = str(address or "").strip().lower()
    net = str(chain or "").strip().lower()
    provider = str(provider_name or "none").strip().lower() or "none"
    digest = hashlib.sha256(f"{net}:{addr}:{provider}".encode("utf-8")).hexdigest()[:32]
    return f"abi_source:{net}:{provider}:{digest}"


def sanitize_abi_source_cache_payload(payload) -> dict:
    src = payload if isinstance(payload, dict) else {}
    out: dict = {}
    for key in _ALLOWED_FIELDS:
        if key not in src:
            continue
        key_l = key.lower()
        if any(marker in key_l for marker in _FORBIDDEN_MARKERS):
            continue
        out[key] = src[key]

    if "provider_name" in out:
        out["provider_name"] = str(out["provider_name"]).strip().lower() or "none"
    if "abi_function_names" in out and not isinstance(out["abi_function_names"], list):
        out["abi_function_names"] = []
    if "fetched_at" not in out:
        out["fetched_at"] = _now_iso()
    return out


def read_abi_source_cache(address, chain, provider_name, config=None, cache_backend=None) -> dict:
    status = get_abi_source_cache_status(config=config)
    if not isinstance(cache_backend, dict):
        return {
            **status,
            "cache_hit": False,
            "value": None,
            "read_attempted": False,
        }
    key = build_abi_source_cache_key(address, chain, provider_name)
    return {
        **status,
        "cache_hit": key in cache_backend,
        "value": cache_backend.get(key),
        "read_attempted": True,
    }


def write_abi_source_cache(address, chain, provider_name, payload, config=None, cache_backend=None) -> dict:
    status = get_abi_source_cache_status(config=config)
    clean_payload = sanitize_abi_source_cache_payload(payload)
    if not isinstance(cache_backend, dict):
        return {
            **status,
            "write_attempted": False,
            "write_status": "not_run",
            "cache_key": build_abi_source_cache_key(address, chain, provider_name),
            "cached_payload": clean_payload,
        }
    key = build_abi_source_cache_key(address, chain, provider_name)
    cache_backend[key] = clean_payload
    return {
        **status,
        "write_attempted": True,
        "write_status": "ok",
        "cache_key": key,
        "cached_payload": clean_payload,
    }
