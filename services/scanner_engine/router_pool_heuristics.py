from __future__ import annotations


def _as_lower_set(values: object) -> set[str]:
    if not isinstance(values, list):
        return set()
    out: set[str] = set()
    for item in values:
        if isinstance(item, str) and item.strip():
            out.add(item.strip().lower())
    return out


def analyze_router_pool_risk(
    address=None,
    chain=None,
    asset_result=None,
    abi_result=None,
    bytecode_result=None,
    source_proxy_admin_result=None,
):
    """
    v6.6.1 router/pool candidate heuristics (local-only, conservative).
    Candidate tags only; no full DEX coverage or malicious certainty claims.
    """
    _ = chain  # reserved for future chain-specific heuristics
    _ = address
    asset_result = asset_result or {}
    abi_result = abi_result or {}
    bytecode_result = bytecode_result or {}
    source_proxy_admin_result = source_proxy_admin_result or {}

    notes: list[str] = []
    asset_type = str(asset_result.get("asset_type") or "unknown")
    fallback_mode = bool(asset_result.get("fallback_mode"))
    abi_available = (
        abi_result.get("available") is True
        or source_proxy_admin_result.get("abi_available") is True
        or bool(_as_lower_set(abi_result.get("functions")))
    )
    functions = _as_lower_set(abi_result.get("functions"))

    base = {
        "router_pool_analysis_status": "unknown",
        "router_candidate": "unknown",
        "pool_candidate": "unknown",
        "lp_token_candidate": "unknown",
        "swap_function_possible": "unknown",
        "liquidity_function_possible": "unknown",
        "reserve_function_possible": "unknown",
        "factory_pattern_possible": "unknown",
        "pair_pattern_possible": "unknown",
        "confidence_impact": "none",
        "fallback_mode": fallback_mode,
        "notes": notes,
    }

    if asset_type == "eoa":
        notes.append("EOA input: router/pool contract heuristics are not applicable.")
        return {
            **base,
            "router_pool_analysis_status": "not_applicable",
            "router_candidate": False,
            "pool_candidate": False,
            "lp_token_candidate": False,
            "swap_function_possible": False,
            "liquidity_function_possible": False,
            "reserve_function_possible": False,
            "factory_pattern_possible": False,
            "pair_pattern_possible": False,
            "signal_flags": {
                "router_pool_not_applicable": 1,
                "router_candidate": 0,
                "pool_candidate": 0,
                "lp_token_candidate": 0,
                "router_pool_data_unknown": 0,
            },
        }

    if not abi_available:
        notes.append("ABI/source hints unavailable: router/pool status remains conservative unknown.")
        notes.append("Does not claim complete DEX, router, or pool coverage.")
        return {
            **base,
            "router_pool_analysis_status": "unknown",
            "confidence_impact": "review_due_to_unknown_router_pool_heuristics",
            "signal_flags": {
                "router_pool_not_applicable": 0,
                "router_candidate": 0,
                "pool_candidate": 0,
                "lp_token_candidate": 0,
                "router_pool_data_unknown": 1,
            },
        }

    base["router_pool_analysis_status"] = "analyzed"
    router_markers = {
        "swapexacttokensfortokens",
        "swapexactethfortokens",
        "swapexacttokensforeth",
        "getamountsout",
        "getamountsin",
        "addliquidity",
        "addliquidityeth",
        "removeliquidity",
        "removeliquidityeth",
    }
    pool_markers = {
        "getreserves",
        "token0",
        "token1",
        "sync",
        "mint",
        "burn",
        "swap",
        "skim",
    }

    has_router_marker = any(fn in functions for fn in router_markers)
    has_pool_marker = any(fn in functions for fn in pool_markers)
    has_liquidity_marker = any("liquidity" in fn for fn in functions)
    has_factory_marker = any("factory" in fn for fn in functions)
    has_pair_marker = any("pair" in fn for fn in functions)
    has_swap_marker = any("swap" in fn for fn in functions)
    has_reserve_marker = any("reserve" in fn for fn in functions)

    base["router_candidate"] = True if (has_router_marker or abi_result.get("is_router") is True) else "unknown"
    base["pool_candidate"] = True if (has_pool_marker or abi_result.get("is_pool") is True) else "unknown"
    base["lp_token_candidate"] = True if (has_liquidity_marker and has_pair_marker) else "unknown"
    base["swap_function_possible"] = True if has_swap_marker else "unknown"
    base["liquidity_function_possible"] = True if has_liquidity_marker else "unknown"
    base["reserve_function_possible"] = True if has_reserve_marker else "unknown"
    base["factory_pattern_possible"] = True if has_factory_marker else "unknown"
    base["pair_pattern_possible"] = True if has_pair_marker else "unknown"
    base["fallback_mode"] = bool(asset_result.get("fallback_mode")) or bool(bytecode_result.get("fallback_mode"))

    if any(v == "unknown" for k, v in base.items() if k.endswith("_possible") or k.endswith("_candidate")):
        base["confidence_impact"] = "review_due_to_partial_router_pool_heuristics"

    notes.append("Router/pool outputs are candidate heuristics only.")
    notes.append("Does not claim complete DEX support or malicious behavior certainty.")
    notes.append("Does not claim honeypot detection.")

    return {
        **base,
        "signal_flags": {
            "router_pool_not_applicable": 0,
            "router_candidate": 1 if base["router_candidate"] is True else 0,
            "pool_candidate": 1 if base["pool_candidate"] is True else 0,
            "lp_token_candidate": 1 if base["lp_token_candidate"] is True else 0,
            "router_pool_data_unknown": 1 if (base["router_candidate"] == "unknown" and base["pool_candidate"] == "unknown") else 0,
        },
    }
