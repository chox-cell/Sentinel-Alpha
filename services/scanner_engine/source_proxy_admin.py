from __future__ import annotations

from services.signals.validators import normalize_address

_ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def _flag(value: object) -> bool:
    return value is True or value == 1


def analyze_source_proxy_admin(
    address: str,
    chain: str,
    asset_result: dict | None = None,
    chain_read_result: dict | None = None,
    abi_result: dict | None = None,
) -> dict:
    """
    Conservative v5.2 source/proxy/admin boundary.
    Unknown/unavailable is preferred over false certainty.
    """
    addr = normalize_address(address or "")
    _chain = (chain or "base").strip().lower() or "base"
    asset_result = asset_result or {}
    chain_read_result = chain_read_result or {}
    abi_result = abi_result or {}

    notes: list[str] = []
    basis: list[str] = []

    read_status = str(chain_read_result.get("chain_read_status") or "unknown")
    fallback_mode = read_status != "ok"
    asset_type = str(asset_result.get("asset_type") or "unknown")

    if addr == _ZERO_ADDRESS:
        return {
            "verified_source_status": "unavailable",
            "abi_available": "unknown",
            "proxy_detected": "unknown",
            "implementation_address": None,
            "owner_admin_permissions": "unknown",
            "privileged_controls": {
                "pause_possible": "unknown",
                "blacklist_possible": "unknown",
                "mint_possible": "unknown",
                "upgrade_possible": "unknown",
                "fee_change_possible": "unknown",
                "admin_transfer_possible": "unknown",
            },
            "confidence_impact": "none",
            "fallback_mode": fallback_mode,
            "classification_basis": ["zero_address"],
            "notes": ["zero address path: source/proxy/admin analysis unavailable"],
            "signal_flags": {
                "source_unavailable": 1,
                "abi_unavailable": 1,
                "proxy_unknown": 1,
                "admin_permissions_unknown": 1,
                "privileged_controls_unknown": 1,
            },
        }

    if asset_type == "eoa":
        return {
            "verified_source_status": "unknown",
            "abi_available": "unknown",
            "proxy_detected": "unknown",
            "implementation_address": None,
            "owner_admin_permissions": "unknown",
            "privileged_controls": {
                "pause_possible": "unknown",
                "blacklist_possible": "unknown",
                "mint_possible": "unknown",
                "upgrade_possible": "unknown",
                "fee_change_possible": "unknown",
                "admin_transfer_possible": "unknown",
            },
            "confidence_impact": "none",
            "fallback_mode": fallback_mode,
            "classification_basis": ["asset_type:eoa"],
            "notes": ["EOA input: source/proxy/admin contract analysis not applicable"],
            "signal_flags": {
                "source_unavailable": 0,
                "abi_unavailable": 0,
                "proxy_unknown": 1,
                "admin_permissions_unknown": 1,
                "privileged_controls_unknown": 1,
            },
        }

    if read_status in {"not_configured", "unsupported_chain", "provider_error", "reads_disabled", "unavailable"}:
        return {
            "verified_source_status": "unavailable",
            "abi_available": "unknown",
            "proxy_detected": "unknown",
            "implementation_address": None,
            "owner_admin_permissions": "unknown",
            "privileged_controls": {
                "pause_possible": "unknown",
                "blacklist_possible": "unknown",
                "mint_possible": "unknown",
                "upgrade_possible": "unknown",
                "fee_change_possible": "unknown",
                "admin_transfer_possible": "unknown",
            },
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "fallback_mode": True,
            "classification_basis": [f"chain_read:{read_status}"],
            "notes": ["provider unavailable/disabled: source-proxy-admin analysis in fallback mode"],
            "signal_flags": {
                "source_unavailable": 1,
                "abi_unavailable": 1,
                "proxy_unknown": 1,
                "admin_permissions_unknown": 1,
                "privileged_controls_unknown": 1,
            },
        }

    has_abi = _flag(abi_result.get("abi_available"))
    has_source = _flag(abi_result.get("verified_source"))
    source_status = "verified" if has_source else "unverified" if has_abi else "unavailable"
    abi_available = True if has_abi else "unknown"

    if has_abi:
        basis.append("abi_available")
    else:
        notes.append("ABI/source data unavailable: conservative unknown statuses used")

    proxy_hint = abi_result.get("is_proxy")
    if proxy_hint is True or proxy_hint == 1:
        proxy_detected: bool | str = True
        basis.append("proxy_hint:true")
    elif proxy_hint is False:
        proxy_detected = False
        basis.append("proxy_hint:false")
    else:
        proxy_detected = "unknown"
        notes.append("proxy status unknown without ABI/source certainty")

    impl = abi_result.get("implementation_address")
    impl_norm = normalize_address(str(impl)) if isinstance(impl, str) and impl.strip() else None
    if not impl_norm:
        impl_norm = None

    owner_hint = abi_result.get("owner_admin_permissions")
    if owner_hint in {"present", "absent", "unknown"}:
        owner_admin_permissions = owner_hint
    elif owner_hint is True or owner_hint == 1:
        owner_admin_permissions = "present"
    elif owner_hint is False:
        owner_admin_permissions = "absent"
    else:
        owner_admin_permissions = "unknown"

    controls = {
        "pause_possible": abi_result.get("pause_possible", "unknown"),
        "blacklist_possible": abi_result.get("blacklist_possible", "unknown"),
        "mint_possible": abi_result.get("mint_possible", "unknown"),
        "upgrade_possible": abi_result.get("upgrade_possible", "unknown"),
        "fee_change_possible": abi_result.get("fee_change_possible", "unknown"),
        "admin_transfer_possible": abi_result.get("admin_transfer_possible", "unknown"),
    }

    # Normalize any non-bool values to "unknown" to avoid false certainty.
    for key, value in list(controls.items()):
        if not isinstance(value, bool):
            controls[key] = "unknown"

    if owner_admin_permissions == "unknown":
        notes.append("owner/admin permission status unknown without strong ABI/source support")

    any_control_unknown = any(v == "unknown" for v in controls.values())

    return {
        "verified_source_status": source_status,
        "abi_available": abi_available,
        "proxy_detected": proxy_detected,
        "implementation_address": impl_norm,
        "owner_admin_permissions": owner_admin_permissions,
        "privileged_controls": controls,
        "confidence_impact": (
            "low_confidence_due_to_unavailable_source"
            if source_status == "unavailable"
            else "review_due_to_unknown_admin_or_proxy"
            if (proxy_detected == "unknown" or owner_admin_permissions == "unknown")
            else "none"
        ),
        "fallback_mode": fallback_mode,
        "classification_basis": basis,
        "notes": notes,
        "signal_flags": {
            "source_unavailable": 1 if source_status == "unavailable" else 0,
            "abi_unavailable": 1 if abi_available != True else 0,
            "proxy_unknown": 1 if proxy_detected == "unknown" else 0,
            "admin_permissions_unknown": 1 if owner_admin_permissions == "unknown" else 0,
            "privileged_controls_unknown": 1 if any_control_unknown else 0,
        },
    }

