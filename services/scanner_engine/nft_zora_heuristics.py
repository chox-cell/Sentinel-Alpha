from __future__ import annotations

from services.signals.validators import normalize_address

_ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def _as_lower_set(values: object) -> set[str]:
    if not isinstance(values, list):
        return set()
    out: set[str] = set()
    for item in values:
        if isinstance(item, str) and item.strip():
            out.add(item.strip().lower())
    return out


def analyze_nft_zora_risk(
    address: str,
    chain: str,
    asset_result: dict | None = None,
    source_proxy_admin_result: dict | None = None,
    abi_result: dict | None = None,
    chain_read_result: dict | None = None,
) -> dict:
    """
    Conservative v5.4 NFT/Zora heuristic boundary.
    Uses possible/unknown/candidate language only.
    """
    addr = normalize_address(address or "")
    _chain = (chain or "base").strip().lower() or "base"
    asset_result = asset_result or {}
    source_proxy_admin_result = source_proxy_admin_result or {}
    abi_result = abi_result or {}
    chain_read_result = chain_read_result or {}

    asset_type = str(asset_result.get("asset_type") or "unknown")
    read_status = str(chain_read_result.get("chain_read_status") or "unknown")
    fallback_mode = read_status != "ok"
    notes: list[str] = []

    base = {
        "nft_zora_analysis_status": "unknown",
        "erc721_candidate": "unknown",
        "erc1155_candidate": "unknown",
        "zora_creator_coin_candidate": "unknown",
        "creator_asset_context": "unknown",
        "transfer_restriction_possible": "unknown",
        "operator_approval_risk": "unknown",
        "mint_control_possible": "unknown",
        "metadata_mutability_possible": "unknown",
        "royalty_admin_possible": "unknown",
        "collection_age_unknown": True,
        "zora_context_detected": "unknown",
        "confidence_impact": "none",
        "fallback_mode": fallback_mode,
        "notes": notes,
    }

    if addr == _ZERO_ADDRESS:
        base["nft_zora_analysis_status"] = "unavailable"
        notes.append("zero address path: NFT/Zora heuristics unavailable")
        return {
            **base,
            "signal_flags": {
                "nft_zora_analysis_unavailable": 1,
                "erc721_candidate": 0,
                "erc1155_candidate": 0,
                "zora_context_possible": 0,
                "operator_approval_risk_unknown": 1,
                "transfer_restriction_unknown": 1,
                "mint_control_possible": 0,
                "metadata_mutability_unknown": 1,
            },
        }

    if asset_type == "eoa":
        base["nft_zora_analysis_status"] = "not_applicable"
        base["erc721_candidate"] = False
        base["erc1155_candidate"] = False
        base["zora_creator_coin_candidate"] = False
        notes.append("EOA input: NFT/Zora contract heuristics not applicable")
        return {
            **base,
            "signal_flags": {
                "nft_zora_analysis_unavailable": 0,
                "erc721_candidate": 0,
                "erc1155_candidate": 0,
                "zora_context_possible": 0,
                "operator_approval_risk_unknown": 0,
                "transfer_restriction_unknown": 0,
                "mint_control_possible": 0,
                "metadata_mutability_unknown": 0,
            },
        }

    if read_status in {"not_configured", "unsupported_chain", "provider_error", "reads_disabled", "unavailable"}:
        base["nft_zora_analysis_status"] = "unavailable"
        base["confidence_impact"] = "low_confidence_due_to_unavailable_nft_zora_data"
        notes.append("provider unavailable/disabled: NFT/Zora heuristics in fallback mode")
        return {
            **base,
            "signal_flags": {
                "nft_zora_analysis_unavailable": 1,
                "erc721_candidate": 0,
                "erc1155_candidate": 0,
                "zora_context_possible": 0,
                "operator_approval_risk_unknown": 1,
                "transfer_restriction_unknown": 1,
                "mint_control_possible": 0,
                "metadata_mutability_unknown": 1,
            },
        }

    functions = _as_lower_set(abi_result.get("functions"))
    selectors = _as_lower_set(abi_result.get("selectors"))
    abi_available = (
        abi_result.get("available") is True
        or source_proxy_admin_result.get("abi_available") is True
        or bool(functions)
    )

    if not abi_available:
        base["nft_zora_analysis_status"] = "unknown"
        base["confidence_impact"] = "review_due_to_unknown_nft_zora_heuristics"
        notes.append("no ABI/source hints: NFT/Zora heuristics remain unknown and conservative")
        notes.append("does not claim full Zora support or complete NFT risk coverage")
        return {
            **base,
            "signal_flags": {
                "nft_zora_analysis_unavailable": 0,
                "erc721_candidate": 0,
                "erc1155_candidate": 0,
                "zora_context_possible": 0,
                "operator_approval_risk_unknown": 1,
                "transfer_restriction_unknown": 1,
                "mint_control_possible": 0,
                "metadata_mutability_unknown": 1,
            },
        }

    base["nft_zora_analysis_status"] = "analyzed"

    erc721_funcs = {"ownerof", "tokenuri", "setapprovalforall"}
    erc1155_funcs = {"ur i".replace(" ", ""), "balanceofbatch", "safeBatchTransferFrom".lower(), "setapprovalforall"}
    zora_funcs = {"zora", "creator", "saleconfig", "royaltyinfo", "setroyalty", "createedition", "mintwithrewards"}

    has_erc721 = any(fn in functions for fn in erc721_funcs)
    has_erc1155 = any(fn in functions for fn in erc1155_funcs)
    has_zora = any(h in fn for fn in functions for h in zora_funcs) or any("zora" in s for s in selectors)

    base["erc721_candidate"] = True if has_erc721 or asset_type == "erc721_candidate" else "unknown"
    base["erc1155_candidate"] = True if has_erc1155 or asset_type == "erc1155_candidate" else "unknown"
    base["zora_creator_coin_candidate"] = True if has_zora else "unknown"
    base["zora_context_detected"] = True if has_zora else "unknown"

    if has_zora:
        base["creator_asset_context"] = "zora"
    elif has_erc721 or has_erc1155:
        base["creator_asset_context"] = "nft"
    else:
        base["creator_asset_context"] = "unknown"

    def _possible(names: set[str]) -> bool | str:
        return True if any(name in functions for name in names) else "unknown"

    base["transfer_restriction_possible"] = _possible({"settransfervalidator", "settransferrestriction", "settradingenabled"})
    base["operator_approval_risk"] = True if "setapprovalforall" in functions else "unknown"
    base["mint_control_possible"] = _possible({"mint", "mintto", "_mint", "createedition"})
    base["metadata_mutability_possible"] = _possible({"setbaseuri", "settokenuri", "setcontracturi"})
    base["royalty_admin_possible"] = _possible({"setroyalty", "royaltyinfo", "setdefaultroyalty"})
    base["collection_age_unknown"] = True

    notes.append("does not claim full Zora support")
    notes.append("does not claim all NFT transfer/metadata risks are covered")
    if selectors:
        notes.append("selector hints supplied; interpreted conservatively as possible capabilities")

    unknowns = [
        base["transfer_restriction_possible"],
        base["operator_approval_risk"],
        base["mint_control_possible"],
        base["metadata_mutability_possible"],
        base["royalty_admin_possible"],
    ]
    base["confidence_impact"] = "review_due_to_partial_nft_zora_heuristics" if any(v == "unknown" for v in unknowns) else "none"

    return {
        **base,
        "signal_flags": {
            "nft_zora_analysis_unavailable": 0,
            "erc721_candidate": 1 if base["erc721_candidate"] is True else 0,
            "erc1155_candidate": 1 if base["erc1155_candidate"] is True else 0,
            "zora_context_possible": 1 if base["zora_context_detected"] is True else 0,
            "operator_approval_risk_unknown": 1 if base["operator_approval_risk"] == "unknown" else 0,
            "transfer_restriction_unknown": 1 if base["transfer_restriction_possible"] == "unknown" else 0,
            "mint_control_possible": 1 if base["mint_control_possible"] is True else 0,
            "metadata_mutability_unknown": 1 if base["metadata_mutability_possible"] == "unknown" else 0,
        },
    }

