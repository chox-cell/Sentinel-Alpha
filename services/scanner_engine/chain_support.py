from __future__ import annotations

from services.scanner_engine.chain_read_adapter import get_chain_readiness


def get_chain_support(chain: str) -> dict:
    normalized = (chain or "base").strip().lower() or "base"
    readiness = get_chain_readiness(normalized)
    read_status = str(readiness.get("status") or "unknown")

    # Conservative truth posture: Base is primary, others are partial/roadmap/unsupported.
    if normalized == "base":
        support_status = "primary"
        risk_engine_support = "full_v5_primary"
        notes = [
            "Base is the primary production chain for Sentinel risk decisions.",
            "Chain reads are config-gated and can be disabled by default.",
        ]
        confidence_impact = "none"
    elif normalized in {"ethereum"}:
        support_status = "partial"
        risk_engine_support = "partial_signals"
        notes = [
            "Ethereum support is partial/roadmap-facing, not full primary coverage.",
            "Use conservative interpretation for non-Base risk confidence.",
        ]
        confidence_impact = "review_due_to_partial_chain_support"
    elif normalized in {"zora"}:
        support_status = "roadmap"
        risk_engine_support = "docs_only"
        notes = [
            "Zora chain context is roadmap/partial candidate support only.",
            "No full Zora chain support claim in current runtime.",
        ]
        confidence_impact = "review_due_to_partial_chain_support"
    elif normalized in {"arbitrum", "optimism", "polygon", "monad"}:
        support_status = "roadmap"
        risk_engine_support = "partial_signals"
        notes = [
            "Chain is recognized as EVM but not primary support in current runtime.",
        ]
        confidence_impact = "review_due_to_partial_chain_support"
    else:
        support_status = "unsupported"
        risk_engine_support = "unsupported"
        notes = ["Unsupported or unknown chain; fallback-safe behavior applies."]
        confidence_impact = "low_confidence_due_to_unsupported_chain"

    chain_read_default = "enabled" if read_status == "available" else "disabled"
    if read_status in {"not_configured", "reads_disabled", "unsupported_chain", "unknown"}:
        chain_read_default = "not_configured"

    return {
        "chain": normalized,
        "support_status": support_status,
        "network_family": "evm" if support_status != "unsupported" else "unknown",
        "risk_engine_support": risk_engine_support,
        "chain_read_default": chain_read_default,
        "paid_rpc_required": False,
        "confidence_impact": confidence_impact,
        "notes": notes,
    }

