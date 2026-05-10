from __future__ import annotations

from services.signals.validators import normalize_address
from services.scanner_engine.abi_source_dry_run_provider import (
    dry_run_abi_source_lookup,
    hash_contract_address_for_plan,
    should_use_dry_run_skeleton,
)
from services.scanner_engine.abi_source_provider_config import (
    get_abi_source_provider_config,
    get_abi_source_provider_runtime_status,
)

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


def _fake_backend_result(scenario: str) -> dict:
    scenario = str(scenario or "").strip().lower()
    if scenario == "success_verified_source":
        names = ["transfer", "approve", "balanceOf"]
        return {
            "source_provider_status": "adapter_ready",
            "verified_source_status": "verified",
            "abi_available": True,
            "abi_function_names": names,
            "abi_selector_count": len(names),
            "source_fetch_error_type": None,
            "provider_name": "fake_backend",
            "confidence_impact": "none",
            "fallback_mode": False,
            "notes": [
                "Fake backend contract test scenario: success_verified_source.",
                "No external provider call was performed.",
                "No full ABI coverage is claimed.",
            ],
        }

    if scenario == "success_abi_only":
        names = ["transfer", "totalSupply"]
        return {
            "source_provider_status": "adapter_ready",
            "verified_source_status": "unverified",
            "abi_available": True,
            "abi_function_names": names,
            "abi_selector_count": len(names),
            "source_fetch_error_type": None,
            "provider_name": "fake_backend",
            "confidence_impact": "neutral",
            "fallback_mode": False,
            "notes": [
                "Fake backend contract test scenario: success_abi_only.",
                "No external provider call was performed.",
                "No full verified-source coverage is claimed.",
            ],
        }

    error_map = {
        "timeout": "timeout",
        "rate_limited": "rate_limited",
        "invalid_response": "invalid_response",
        "provider_down": "provider_down",
        "unsupported_chain": "unsupported_chain",
    }
    if scenario in error_map:
        return {
            "source_provider_status": "not_configured",
            "verified_source_status": "unknown",
            "abi_available": "unknown",
            "abi_function_names": [],
            "abi_selector_count": 0,
            "source_fetch_error_type": error_map[scenario],
            "provider_name": "fake_backend",
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "fallback_mode": True,
            "notes": [
                f"Fake backend contract test scenario: {scenario}.",
                "No external provider call was performed.",
                "Fallback mode is expected for unavailable provider context.",
            ],
        }

    return {
        "source_provider_status": "not_configured",
        "verified_source_status": "unknown",
        "abi_available": "unknown",
        "abi_function_names": [],
        "abi_selector_count": 0,
        "source_fetch_error_type": "invalid_response",
        "provider_name": "fake_backend",
        "confidence_impact": "low_confidence_due_to_unavailable_source",
        "fallback_mode": True,
        "notes": [
            "Fake backend scenario was not recognized.",
            "No external provider call was performed.",
        ],
    }


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
    provider_config = get_abi_source_provider_config(env=None, overrides=config)
    provider_runtime_status = get_abi_source_provider_runtime_status(provider_config)

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
            "provider_runtime_status": provider_runtime_status,
            "notes": [
                "ABI/source provider is disabled by configuration.",
                "No live verified-source lookup is performed by default.",
                "No full ABI coverage is claimed.",
            ],
        }

    provider_name = str(provider_context.get("provider_name") or "none").strip().lower() or "none"
    fake_backend_enabled = bool(provider_context.get("fake_backend")) or provider_name == "fake_backend"
    fake_backend_scenario = provider_context.get("scenario") or config.get("fake_backend_scenario")
    if fake_backend_enabled:
        out = _fake_backend_result(str(fake_backend_scenario or "invalid_response"))
        out["provider_runtime_status"] = provider_runtime_status
        return out

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
            "provider_runtime_status": provider_runtime_status,
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
            "provider_runtime_status": provider_runtime_status,
            "notes": [
                f"Unsupported chain for current ABI/source adapter boundary: {_chain}.",
                "ABI/source provider is not configured by default.",
            ],
        }

    provider_mode = str(provider_runtime_status.get("provider_mode") or "disabled")
    if provider_mode in {"disabled", "not_configured", "unsupported_provider"}:
        fetch_error = "unsupported_provider" if provider_mode == "unsupported_provider" else "not_configured"
        mode_note = (
            "ABI/source provider wiring skeleton is disabled by default."
            if provider_mode == "disabled"
            else "ABI/source provider wiring skeleton is enabled but provider name is missing."
            if provider_mode == "not_configured"
            else "ABI/source provider wiring skeleton has unsupported provider name."
        )
        return {
            "source_provider_status": provider_mode,
            "verified_source_status": "unknown",
            "abi_available": "unknown",
            "abi_function_names": [],
            "abi_selector_count": 0,
            "source_fetch_error_type": fetch_error,
            "provider_name": provider_runtime_status.get("provider_name") or "none",
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "fallback_mode": True,
            "provider_runtime_status": provider_runtime_status,
            "notes": [
                mode_note,
                "ABI/source provider is not configured by default.",
                "No live provider call is performed in skeleton mode.",
                "No API key is required by default.",
                "No full ABI coverage is claimed.",
            ],
        }

    if provider_mode == "adapter_ready":
        if should_use_dry_run_skeleton(provider_config):
            addr_hash = hash_contract_address_for_plan(_address)
            dry = dry_run_abi_source_lookup(
                provider_runtime_status.get("provider_name"),
                _chain,
                contract_address_hash=addr_hash,
                config=provider_config,
            )
            dry_notes = list(dry.get("notes") or [])
            return {
                "source_provider_status": "adapter_ready",
                "verified_source_status": dry.get("verified_source_status"),
                "abi_available": dry.get("abi_available"),
                "abi_function_names": list(dry.get("abi_function_names_sample") or []),
                "abi_selector_count": int(dry.get("abi_function_count") or 0),
                "source_fetch_error_type": dry.get("source_fetch_error_type"),
                "provider_name": provider_runtime_status.get("provider_name"),
                "confidence_impact": dry.get("confidence_impact"),
                "fallback_mode": bool(dry.get("fallback_mode", True)),
                "provider_runtime_status": provider_runtime_status,
                "dry_run_lookup": dry,
                "notes": [
                    "ABI/source provider dry-run skeleton (Sourcify or Blockscout) is active.",
                    "Endpoint templates are documentation only and are not called.",
                    "No trial evidence is produced by dry-run rows alone.",
                    *dry_notes,
                ],
            }

        return {
            "source_provider_status": "adapter_ready",
            "verified_source_status": "unknown",
            "abi_available": "unknown",
            "abi_function_names": [],
            "abi_selector_count": 0,
            "source_fetch_error_type": "not_activated",
            "provider_name": provider_runtime_status.get("provider_name"),
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "fallback_mode": True,
            "provider_runtime_status": provider_runtime_status,
            "notes": [
                "ABI/source provider wiring skeleton is ready but live lookup is not activated.",
                "No network call is performed in skeleton mode.",
                "No API key is required by default.",
                "No guaranteed source verification is claimed.",
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
        "provider_runtime_status": provider_runtime_status,
        "notes": [
            "ABI/source provider is not configured by default.",
            "No live verified-source lookup is performed unless explicitly configured.",
            "No full ABI coverage is claimed.",
        ],
    }
