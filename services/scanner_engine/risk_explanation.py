from __future__ import annotations


def build_risk_explanation(
    decision=None,
    asset_result=None,
    source_proxy_admin_result=None,
    erc20_result=None,
    nft_zora_result=None,
    simulation_result=None,
    chain_read_result=None,
    signals=None,
):
    decision = decision or {}
    asset_result = asset_result or {}
    source_proxy_admin_result = source_proxy_admin_result or {}
    erc20_result = erc20_result or {}
    nft_zora_result = nft_zora_result or {}
    simulation_result = simulation_result or {}
    chain_read_result = chain_read_result or {}
    signals = signals or {}

    explanation: list[str] = []
    uncertainty_notes: list[str] = []
    top_risk_factors: list[str] = []

    action = str(decision.get("action") or "UNKNOWN").upper()
    confidence = decision.get("confidence")

    if signals.get("zero_address"):
        explanation.append("Zero address detected; high-risk path preserved.")
        top_risk_factors.append("zero_address")

    read_status = str(chain_read_result.get("chain_read_status") or "unknown")
    fallback_reason = None
    if read_status in {"not_configured", "unsupported_chain", "provider_error", "reads_disabled", "unavailable"}:
        fallback_reason = f"Provider unavailable ({read_status}); confidence reduced."
        explanation.append("Provider unavailable; confidence reduced.")
        uncertainty_notes.append("Chain-read context is unavailable; contract classification depth is limited.")

    asset_type = str(asset_result.get("asset_type") or "unknown")
    if asset_type == "eoa":
        explanation.append("Target is an EOA; contract analysis is not applicable.")
    elif asset_type == "generic_contract":
        spa_source = source_proxy_admin_result.get("verified_source_status")
        spa_abi = source_proxy_admin_result.get("abi_available")
        if spa_source in {"unavailable", "unknown"} or spa_abi == "unknown":
            explanation.append("Contract bytecode is available, but ABI/source context is unavailable.")
            uncertainty_notes.append("Generic-contract path has limited semantic context.")

    if source_proxy_admin_result.get("proxy_detected") == "unknown":
        explanation.append("Proxy status is unknown; review may be appropriate.")
        uncertainty_notes.append("Proxy/implementation certainty is unavailable.")

    if source_proxy_admin_result.get("owner_admin_permissions") == "unknown":
        uncertainty_notes.append("Owner/admin permission visibility is limited.")

    if erc20_result.get("erc20_analysis_status") in {"unknown", "unavailable"}:
        explanation.append("ERC20 risk signals are unknown without ABI/source context.")
    if nft_zora_result.get("nft_zora_analysis_status") in {"unknown", "unavailable"}:
        explanation.append("NFT/Zora-specific signals are unknown without ABI/source context.")

    if simulation_result.get("simulation_mode") in {"disabled", "not_configured"}:
        explanation.append("Simulation is not configured; honeypot status remains unknown.")
        uncertainty_notes.append("Buy/sell/call simulation evidence is unavailable.")
    if simulation_result.get("honeypot_risk") == "unknown":
        uncertainty_notes.append("Honeypot risk remains unknown without live simulation evidence.")

    for key in (
        "oracle_dislocation",
        "liquidity_unlocked",
        "simulation_revert",
        "owner_privileges",
        "bad_cluster",
        "shadow_link",
        "invalid_address",
    ):
        if signals.get(key):
            top_risk_factors.append(key)

    if not top_risk_factors:
        top_risk_factors.append("insufficient_data_or_low_signal_density")

    if confidence is not None and isinstance(confidence, (int, float)):
        confidence_reason = f"Confidence={confidence:.2f}; adjusted by available signal coverage and uncertainty."
    else:
        confidence_reason = "Confidence is driven by available signal coverage and uncertainty."

    step_map = {
        "ALLOW": "allow",
        "REVIEW": "review",
        "BLOCK": "block",
        "EXIT_NOW": "block",
        "REDUCE": "review",
    }
    recommended_next_step = step_map.get(action, "unknown")

    if not explanation:
        explanation.append("Risk decision generated from deterministic available signals.")

    return {
        "explanation": explanation,
        "top_risk_factors": top_risk_factors,
        "confidence_reason": confidence_reason,
        "fallback_reason": fallback_reason,
        "uncertainty_notes": uncertainty_notes,
        "recommended_next_step": recommended_next_step,
    }

