from __future__ import annotations

from services.signals.validators import normalize_address

SUPPORTED_CHAINS = {"base", "ethereum", "arbitrum", "optimism", "polygon", "zora"}


def _safe_function_names(abi_value: object) -> list[str]:
    if not isinstance(abi_value, list):
        return []
    names: list[str] = []
    for entry in abi_value:
        if not isinstance(entry, dict):
            continue
        if str(entry.get("type") or "").strip().lower() != "function":
            continue
        name = str(entry.get("name") or "").strip()
        if name and name not in names:
            names.append(name)
    return names


def analyze_abi_source_status(
    address=None,
    chain=None,
    provider_context=None,
    config=None,
) -> dict:
    """
    v6.2 ABI/source provider boundary.
    Safe-by-default path is non-configured and fallback mode.
    """
    _address = normalize_address(str(address or ""))
    _chain = (str(chain or "base").strip().lower() or "base")
    provider_context = provider_context if isinstance(provider_context, dict) else {}
    config = config if isinstance(config, dict) else {}

    notes: list[str] = []
    source_fetch_error_type = None

    enabled = config.get("enabled")
    if enabled in {False, 0, "0", "false", "False", "off", "OFF"}:
        return {
            "source_provider_status": "disabled",
            "verified_source_status": "unknown",
            "abi_available": "unknown",
            "abi_function_names": [],
            "abi_selector_count": 0,
            "source_fetch_error_type": "not_configured",
            "provider_name": "none",
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "fallback_mode": True,
            "notes": [
                "ABI/source provider is disabled by configuration.",
                "No live verified-source lookup is performed by default.",
                "No full ABI coverage is claimed.",
            ],
        }

    provider_name = str(provider_context.get("provider_name") or "none").strip().lower() or "none"
    if provider_name == "local_fixture":
        verified_status = str(provider_context.get("verified_source_status") or "unknown").strip().lower()
        if verified_status not in {"verified", "unverified", "unavailable", "unknown"}:
            verified_status = "unknown"
        abi_list = provider_context.get("abi")
        function_names = _safe_function_names(abi_list)
        abi_available = True if isinstance(abi_list, list) and len(abi_list) > 0 else False
        notes.append("Local fixture provider context used for deterministic/offline tests.")
        notes.append("No external source provider call was required.")
        notes.append("No full ABI coverage is claimed.")
        return {
            "source_provider_status": "available",
            "verified_source_status": verified_status,
            "abi_available": abi_available,
            "abi_function_names": function_names,
            "abi_selector_count": len(function_names),
            "source_fetch_error_type": source_fetch_error_type,
            "provider_name": "local_fixture",
            "confidence_impact": "none" if abi_available else "low_confidence_due_to_unavailable_source",
            "fallback_mode": not abi_available,
            "notes": notes,
        }

    if _chain not in SUPPORTED_CHAINS:
        source_fetch_error_type = "unsupported_chain"
        return {
            "source_provider_status": "not_configured",
            "verified_source_status": "unavailable",
            "abi_available": "unknown",
            "abi_function_names": [],
            "abi_selector_count": 0,
            "source_fetch_error_type": source_fetch_error_type,
            "provider_name": "none",
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "fallback_mode": True,
            "notes": [
                f"Unsupported chain for current ABI/source adapter boundary: {_chain}.",
                "ABI/source provider is not configured by default.",
            ],
        }

    return {
        "source_provider_status": "not_configured",
        "verified_source_status": "unknown",
        "abi_available": "unknown",
        "abi_function_names": [],
        "abi_selector_count": 0,
        "source_fetch_error_type": "not_configured",
        "provider_name": "none",
        "confidence_impact": "low_confidence_due_to_unavailable_source",
        "fallback_mode": True,
        "notes": [
            "ABI/source provider is not configured by default.",
            "No live verified-source lookup is performed unless explicitly configured.",
            "No full ABI coverage is claimed.",
        ],
    }
