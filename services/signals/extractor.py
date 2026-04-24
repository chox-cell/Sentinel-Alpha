from services.signals.validators import (
    normalize_address,
    normalize_chain,
    is_valid_evm_address,
    is_probably_evm_like,
)
from services.signals.bytecode_scanner import scan_bytecode

def extract_signals(contract_address: str, chain: str, context: dict | None = None) -> dict:
    """
    Real Signals v0.

    This is not mock_signals.
    It extracts deterministic risk signals from:
    - address validity
    - chain
    - optional event/context payload
    - launch-time metadata

    Later this file will connect to:
    - QuickNode RPC
    - bytecode scan
    - liquidity scan
    - deployer profile
    - simulation
    """

    context = context or {}

    address = normalize_address(contract_address)
    chain = normalize_chain(chain)

    valid_evm = is_valid_evm_address(address)
    evm_like = is_probably_evm_like(address)

    signals = {
        "invalid_address": 0,
        "unverified_address_shape": 0,
        "new_deploy": 0,
        "first_liquidity": 0,
        "owner_privileges": 0,
        "liquidity_unlocked": 0,
        "oracle_dislocation": 0,
        "simulation_revert": 0,
        "bad_cluster": 0,
        "shadow_link": 0,
        "bad_bot_activity": 0,
        "insufficient_data": 0,
    }

    # Address-level truth
    if chain in {"base", "ethereum", "arbitrum", "optimism", "polygon", "monad"}:
        if not valid_evm:
            signals["invalid_address"] = 1
            if evm_like:
                signals["unverified_address_shape"] = 1

    # Event/context-level truth
    if context.get("event_type") in {"contract_created", "new_deploy"}:
        signals["new_deploy"] = 1

    if context.get("event_type") in {"liquidity_added", "first_liquidity"}:
        signals["first_liquidity"] = 1

    # Bytecode scanner stub (mapped into existing signal keys).
    bytecode_findings = scan_bytecode(address, chain, context)
    if bytecode_findings.get("owner_privileges_detected"):
        signals["owner_privileges"] = 1
    if bytecode_findings.get("simulation_revert_detected"):
        signals["simulation_revert"] = 1

    # Optional upstream flags
    for key in [
        "owner_privileges",
        "liquidity_unlocked",
        "oracle_dislocation",
        "simulation_revert",
        "bad_cluster",
        "shadow_link",
        "bad_bot_activity",
    ]:
        if context.get(key) is True or context.get(key) == 1:
            signals[key] = 1

    # If no real upstream evidence exists yet, lower confidence via insufficient_data.
    evidence_keys = [
        "new_deploy",
        "first_liquidity",
        "owner_privileges",
        "liquidity_unlocked",
        "oracle_dislocation",
        "simulation_revert",
        "bad_cluster",
        "shadow_link",
        "bad_bot_activity",
    ]

    if sum(signals[k] for k in evidence_keys) == 0:
        signals["insufficient_data"] = 1

    return {
        "chain": chain,
        "contract_address": address,
        "signals": signals,
    }
