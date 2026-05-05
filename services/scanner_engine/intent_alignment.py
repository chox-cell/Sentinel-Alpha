from __future__ import annotations


def _normalize_intent_category(intent=None, requested_action=None) -> str:
    candidates = []
    if isinstance(intent, dict):
        candidates.extend(
            [
                intent.get("category"),
                intent.get("intent"),
                intent.get("action"),
                intent.get("type"),
            ]
        )
    candidates.append(requested_action)

    known = {"swap", "transfer", "mint", "approve", "bridge", "execute"}
    for item in candidates:
        if isinstance(item, str):
            token = item.strip().lower()
            if token in known:
                return token
    return "unknown"


def analyze_intent_alignment(
    intent=None,
    requested_action=None,
    address=None,
    chain=None,
    asset_result=None,
    source_proxy_admin_result=None,
    erc20_result=None,
    nft_zora_result=None,
    simulation_result=None,
    chain_support_result=None,
):
    asset_result = asset_result or {}
    source_proxy_admin_result = source_proxy_admin_result or {}
    erc20_result = erc20_result or {}
    nft_zora_result = nft_zora_result or {}
    simulation_result = simulation_result or {}
    chain_support_result = chain_support_result or {}

    category = _normalize_intent_category(intent, requested_action)
    asset_type = str(asset_result.get("asset_type") or "unknown")
    chain_support = str(chain_support_result.get("support_status") or "unknown")

    out = {
        "intent_alignment_status": "unknown",
        "intent_category": category,
        "requested_action": requested_action if isinstance(requested_action, str) else None,
        "unexpected_capability_detected": "unknown",
        "suspicious_reason": None,
        "policy_recommendation": "unknown",
        "confidence_impact": "none",
        "fallback_mode": True,
        "notes": [],
    }

    if category == "unknown":
        out["intent_alignment_status"] = "not_provided"
        out["policy_recommendation"] = "unknown"
        out["notes"].append("No intent/action context provided; intent alignment remains unknown.")
        return {
            **out,
            "signal_flags": {
                "intent_not_provided": 1,
                "intent_alignment_unknown": 1,
                "intent_review_recommended": 0,
                "unexpected_capability_unknown": 1,
            },
        }

    out["fallback_mode"] = False
    out["intent_alignment_status"] = "aligned"
    out["policy_recommendation"] = "allow"
    out["unexpected_capability_detected"] = False

    if chain_support in {"unsupported", "unknown"}:
        out["intent_alignment_status"] = "unknown"
        out["policy_recommendation"] = "review"
        out["unexpected_capability_detected"] = "unknown"
        out["suspicious_reason"] = "unsupported_or_unknown_chain"
        out["confidence_impact"] = "review_due_to_chain_support_limits"
        out["notes"].append("Chain support is unsupported/unknown; intent alignment is conservative.")

    if category == "swap" and asset_type in {"erc721_candidate", "erc1155_candidate", "unknown", "generic_contract"}:
        out["intent_alignment_status"] = "suspicious"
        out["policy_recommendation"] = "review"
        out["unexpected_capability_detected"] = "unknown"
        out["suspicious_reason"] = "swap_intent_with_non_clear_swap_context"
        out["confidence_impact"] = "review_due_to_intent_capability_mismatch"
        out["notes"].append("Swap intent is not clearly aligned with current target context.")

    if category == "transfer" and source_proxy_admin_result.get("owner_admin_permissions") == "unknown":
        out["intent_alignment_status"] = "suspicious"
        out["policy_recommendation"] = "review"
        out["unexpected_capability_detected"] = "unknown"
        out["suspicious_reason"] = "transfer_with_unknown_admin_controls"
        out["confidence_impact"] = "review_due_to_unknown_admin_context"
        out["notes"].append("Transfer intent with unknown admin controls should be reviewed.")

    if category == "approve" and asset_type in {"unknown", "generic_contract"}:
        out["intent_alignment_status"] = "suspicious"
        out["policy_recommendation"] = "review"
        out["unexpected_capability_detected"] = "unknown"
        out["suspicious_reason"] = "approve_with_unknown_contract_context"
        out["confidence_impact"] = "review_due_to_unknown_contract_context"
        out["notes"].append("Approve intent with unknown contract context should be reviewed.")

    if category == "mint" and nft_zora_result.get("nft_zora_analysis_status") in {"unknown", "unavailable"}:
        out["intent_alignment_status"] = "suspicious"
        out["policy_recommendation"] = "review"
        out["unexpected_capability_detected"] = "unknown"
        out["suspicious_reason"] = "mint_with_unknown_nft_zora_context"
        out["confidence_impact"] = "review_due_to_unknown_nft_context"
        out["notes"].append("Mint intent without clear NFT/Zora context should be reviewed.")

    out["notes"].append("Intent alignment is policy assistance only, not full intent verification.")

    return {
        **out,
        "signal_flags": {
            "intent_not_provided": 0,
            "intent_alignment_unknown": 1 if out["intent_alignment_status"] in {"unknown", "not_provided"} else 0,
            "intent_review_recommended": 1 if out["policy_recommendation"] == "review" else 0,
            "unexpected_capability_unknown": 1 if out["unexpected_capability_detected"] == "unknown" else 0,
        },
    }

