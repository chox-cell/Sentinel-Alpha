from __future__ import annotations


SUPPORTED_PROVIDERS = ["basescan", "etherscan", "blockscout", "sourcify"]


def _to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def get_abi_source_provider_config(env=None, overrides=None):
    """Return sanitized ABI/source provider config for boundary wiring skeleton."""
    env_map = env if isinstance(env, dict) else {}
    override_map = overrides if isinstance(overrides, dict) else {}

    enabled_raw = override_map.get(
        "SENTINEL_ABI_SOURCE_PROVIDER_ENABLED",
        env_map.get("SENTINEL_ABI_SOURCE_PROVIDER_ENABLED"),
    )
    provider_enabled = _to_bool(enabled_raw)
    provider_name_raw = override_map.get(
        "SENTINEL_ABI_SOURCE_PROVIDER_NAME",
        env_map.get("SENTINEL_ABI_SOURCE_PROVIDER_NAME"),
    )
    provider_name = str(provider_name_raw or "").strip().lower() or None

    dry_run_raw = override_map.get(
        "SENTINEL_ABI_SOURCE_DRY_RUN_ONLY",
        env_map.get("SENTINEL_ABI_SOURCE_DRY_RUN_ONLY"),
    )
    dry_run_only = _to_bool(dry_run_raw)

    blockscout_raw = override_map.get(
        "BLOCKSCOUT_BASE_URL",
        env_map.get("BLOCKSCOUT_BASE_URL"),
    )
    blockscout_base_url = str(blockscout_raw or "").strip()

    timeout_raw = override_map.get(
        "SENTINEL_ABI_SOURCE_PROVIDER_TIMEOUT_MS",
        env_map.get("SENTINEL_ABI_SOURCE_PROVIDER_TIMEOUT_MS", 3000),
    )
    try:
        timeout_ms = int(timeout_raw)
    except (TypeError, ValueError):
        timeout_ms = 3000
    timeout_ms = max(500, timeout_ms)

    if not provider_enabled:
        provider_mode = "disabled"
    elif provider_name is None:
        provider_mode = "not_configured"
    elif provider_name not in SUPPORTED_PROVIDERS:
        provider_mode = "unsupported_provider"
    else:
        provider_mode = "adapter_ready"

    return {
        "provider_enabled": provider_enabled,
        "provider_name": provider_name,
        "provider_mode": provider_mode,
        "dry_run_only": dry_run_only,
        "blockscout_base_url": blockscout_base_url,
        "api_key_required": False,
        "network_calls_enabled": False,
        "timeout_ms": timeout_ms,
        "supported_providers": list(SUPPORTED_PROVIDERS),
        "external_integration_status": "not_integrated",
    }


def get_abi_source_provider_runtime_status(config=None):
    cfg = config if isinstance(config, dict) else get_abi_source_provider_config()
    return {
        "provider_enabled": bool(cfg.get("provider_enabled")),
        "provider_name": cfg.get("provider_name"),
        "provider_mode": cfg.get("provider_mode", "disabled"),
        "dry_run_only": bool(cfg.get("dry_run_only", False)),
        "network_calls_enabled": bool(cfg.get("network_calls_enabled", False)),
        "api_key_required": bool(cfg.get("api_key_required", False)),
        "timeout_ms": int(cfg.get("timeout_ms", 3000)),
        "supported_providers": list(cfg.get("supported_providers") or SUPPORTED_PROVIDERS),
        "external_integration_status": cfg.get("external_integration_status", "not_integrated"),
    }
