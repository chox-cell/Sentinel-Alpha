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


def analyze_erc20_risk(
    address: str,
    chain: str,
    asset_result: dict | None = None,
    source_proxy_admin_result: dict | None = None,
    abi_result: dict | None = None,
    chain_read_result: dict | None = None,
) -> dict:
    """
    Conservative v5.3 ERC20 heuristic boundary.
    Never claims honeypot detection or deep bytecode certainty.
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
        "erc20_analysis_status": "unknown",
        "erc20_candidate": "unknown",
        "transfer_tax_possible": "unknown",
        "blacklist_possible": "unknown",
        "pause_possible": "unknown",
        "max_tx_possible": "unknown",
        "max_wallet_possible": "unknown",
        "mint_possible": "unknown",
        "owner_can_change_fees": "unknown",
        "sell_restriction_possible": "unknown",
        "honeypot_simulation_available": False,
        "confidence_impact": "none",
        "fallback_mode": fallback_mode,
        "notes": notes,
    }

    if addr == _ZERO_ADDRESS:
        base["erc20_analysis_status"] = "unavailable"
        base["confidence_impact"] = "none"
        notes.append("zero address path: ERC20 heuristics unavailable")
        return {
            **base,
            "signal_flags": {
                "erc20_analysis_unavailable": 1,
                "transfer_tax_unknown": 1,
                "blacklist_possible": 0,
                "pause_possible": 0,
                "mint_possible": 0,
                "sell_restriction_unknown": 1,
                "honeypot_simulation_unavailable": 1,
            },
        }

    if asset_type == "eoa":
        base["erc20_analysis_status"] = "not_applicable"
        base["erc20_candidate"] = False
        notes.append("EOA input: ERC20 contract heuristics not applicable")
        return {
            **base,
            "signal_flags": {
                "erc20_analysis_unavailable": 0,
                "transfer_tax_unknown": 0,
                "blacklist_possible": 0,
                "pause_possible": 0,
                "mint_possible": 0,
                "sell_restriction_unknown": 0,
                "honeypot_simulation_unavailable": 1,
            },
        }

    if read_status in {"not_configured", "unsupported_chain", "provider_error", "reads_disabled", "unavailable"}:
        base["erc20_analysis_status"] = "unavailable"
        base["confidence_impact"] = "low_confidence_due_to_unavailable_erc20_data"
        notes.append("provider unavailable/disabled: ERC20 heuristics in fallback mode")
        return {
            **base,
            "signal_flags": {
                "erc20_analysis_unavailable": 1,
                "transfer_tax_unknown": 1,
                "blacklist_possible": 0,
                "pause_possible": 0,
                "mint_possible": 0,
                "sell_restriction_unknown": 1,
                "honeypot_simulation_unavailable": 1,
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
        base["erc20_analysis_status"] = "unknown"
        if asset_type in {"generic_contract", "unknown", "proxy_candidate"}:
            notes.append("no ABI/source hints: ERC20 heuristics remain unknown and conservative")
        base["confidence_impact"] = "review_due_to_unknown_erc20_heuristics"
        return {
            **base,
            "signal_flags": {
                "erc20_analysis_unavailable": 0,
                "transfer_tax_unknown": 1,
                "blacklist_possible": 0,
                "pause_possible": 0,
                "mint_possible": 0,
                "sell_restriction_unknown": 1,
                "honeypot_simulation_unavailable": 1,
            },
        }

    # ABI hints present: expose "possible" style flags only.
    base["erc20_analysis_status"] = "analyzed"
    token_hint = any(
        name in functions
        for name in {
            "totalSupply".lower(),
            "balanceOf".lower(),
            "transfer".lower(),
            "transferFrom".lower(),
            "approve".lower(),
            "allowance".lower(),
            "decimals".lower(),
        }
    )
    base["erc20_candidate"] = True if token_hint or asset_type == "erc20_candidate" else "unknown"

    def _possible(names: set[str]) -> bool | str:
        return True if any(name in functions for name in names) else "unknown"

    base["transfer_tax_possible"] = _possible({"settaxfee", "settax", "setfees", "setbuytax", "setselltax", "_taxfee"})
    base["blacklist_possible"] = _possible({"blacklist", "setblacklist", "addblacklist", "isblacklisted"})
    base["pause_possible"] = _possible({"pause", "unpause", "paused"})
    base["max_tx_possible"] = _possible({"setmaxtx", "setmaxtransactionamount", "maxtransactionamount", "_maxtxamount"})
    base["max_wallet_possible"] = _possible({"setmaxwallet", "maxwallet", "_maxwalletsize"})
    base["mint_possible"] = _possible({"mint", "_mint", "mintto"})
    base["owner_can_change_fees"] = _possible({"settaxfee", "setfees", "setbuytax", "setselltax", "setmarketingfee"})
    base["sell_restriction_possible"] = _possible({"settradingenabled", "setswapenabled", "setlimitsintrade", "_isblacklisted"})

    if selectors:
        notes.append("selector hints supplied; interpreted conservatively as possible capabilities")
    notes.append("honeypot simulation is not available in v5.3")

    unknowns = [
        base["transfer_tax_possible"],
        base["blacklist_possible"],
        base["pause_possible"],
        base["max_tx_possible"],
        base["max_wallet_possible"],
        base["mint_possible"],
        base["owner_can_change_fees"],
        base["sell_restriction_possible"],
    ]
    base["confidence_impact"] = "review_due_to_partial_erc20_heuristics" if any(v == "unknown" for v in unknowns) else "none"

    return {
        **base,
        "signal_flags": {
            "erc20_analysis_unavailable": 0,
            "transfer_tax_unknown": 1 if base["transfer_tax_possible"] == "unknown" else 0,
            "blacklist_possible": 1 if base["blacklist_possible"] is True else 0,
            "pause_possible": 1 if base["pause_possible"] is True else 0,
            "mint_possible": 1 if base["mint_possible"] is True else 0,
            "sell_restriction_unknown": 1 if base["sell_restriction_possible"] == "unknown" else 0,
            "honeypot_simulation_unavailable": 1,
        },
    }

