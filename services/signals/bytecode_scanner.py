from typing import Any, Dict

from services.signals.validators import normalize_address, normalize_chain


def scan_bytecode(contract_address: str, chain: str, context: dict | None = None) -> Dict[str, Any]:
    """
    Bytecode scanner stub for Real Signals v0.

    This intentionally returns conservative defaults until a real RPC-backed
    implementation is wired. Keys are internal and mapped back into existing
    signal fields by the extractor so the public API schema remains unchanged.
    """
    normalized_address = normalize_address(contract_address)
    normalized_chain = normalize_chain(chain)
    context = context or {}

    return {
        "scanner_version": "bytecode-stub-v0",
        "address": normalized_address,
        "chain": normalized_chain,
        "owner_privileges_detected": bool(context.get("owner_privileges_detected", False)),
        "simulation_revert_detected": bool(context.get("simulation_revert_detected", False)),
    }
