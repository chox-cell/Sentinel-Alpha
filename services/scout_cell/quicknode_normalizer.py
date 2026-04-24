from typing import Any


def normalize_quicknode_payload(payload: dict) -> dict:
    """
    QuickNode Payload Normalizer v0.1

    Supports multiple incoming shapes and nested wrappers such as {"data": {...}}
    or {"event": {...}} while preserving unknown fields in context for incremental
    Real Signals integration.
    """
    payload = payload or {}

    normalized = _unwrap_payload(payload)

    contract_address = normalized.get("contract_address") or normalized.get("address")
    chain = str(normalized.get("chain") or "base").strip().lower()
    event_type = str(normalized.get("event_type") or "new_deploy").strip().lower()

    context = dict(normalized)
    context["event_type"] = event_type

    return {
        "contract_address": contract_address,
        "chain": chain,
        "event_type": event_type,
        "context": context,
    }


def _unwrap_payload(payload: dict) -> dict[str, Any]:
    current = payload
    visited: set[int] = set()

    while isinstance(current, dict):
        marker = id(current)
        if marker in visited:
            break
        visited.add(marker)

        if _has_primary_keys(current):
            return current

        nested = None
        for key in ("data", "event"):
            candidate = current.get(key)
            if isinstance(candidate, dict):
                nested = candidate
                break

        if nested is None:
            return current
        current = nested

    return payload


def _has_primary_keys(payload: dict) -> bool:
    return any(
        key in payload
        for key in ("contract_address", "address", "event_type", "chain")
    )
