from __future__ import annotations

from services.signals.validators import normalize_address

_ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
_SIM_ALLOWED_STATUSES = {"passed", "failed", "unknown"}


def analyze_simulation_risk(
    address,
    chain,
    asset_result=None,
    erc20_result=None,
    nft_zora_result=None,
    source_proxy_admin_result=None,
    simulation_request=None,
    config=None,
):
    """
    v5.5 simulation adapter boundary.
    Default is disabled/not_configured with no external paid/provider calls.
    """
    addr = normalize_address(address or "")
    _chain = (chain or "base").strip().lower() or "base"
    asset_result = asset_result or {}
    _erc20 = erc20_result or {}
    _nft = nft_zora_result or {}
    _spa = source_proxy_admin_result or {}
    simulation_request = simulation_request or {}
    config = config or {}

    asset_type = str(asset_result.get("asset_type") or "unknown")
    adapter = config.get("adapter")
    adapter_enabled = bool(config.get("enabled")) and isinstance(adapter, dict)
    notes: list[str] = []

    out = {
        "simulation_available": False,
        "simulation_mode": "disabled",
        "buy_simulation_status": "not_run",
        "sell_simulation_status": "not_run",
        "call_simulation_status": "not_run",
        "honeypot_risk": "unknown",
        "simulation_error_type": None,
        "confidence_impact": "none",
        "fallback_mode": True,
        "notes": notes,
    }

    if addr == _ZERO_ADDRESS:
        out["simulation_mode"] = "not_configured"
        out["buy_simulation_status"] = "unavailable"
        out["sell_simulation_status"] = "unavailable"
        out["call_simulation_status"] = "unavailable"
        out["simulation_error_type"] = "invalid_request"
        notes.append("simulation boundary active but not configured; zero address not simulated")
        return {
            **out,
            "signal_flags": {
                "simulation_unavailable": 1,
                "honeypot_unknown": 1,
                "buy_simulation_not_run": 1,
                "sell_simulation_not_run": 1,
                "call_simulation_not_run": 1,
            },
        }

    if not adapter_enabled:
        out["simulation_mode"] = "not_configured"
        out["buy_simulation_status"] = "unavailable"
        out["sell_simulation_status"] = "unavailable"
        out["call_simulation_status"] = "unavailable"
        out["simulation_error_type"] = "not_configured"
        out["confidence_impact"] = "review_due_to_missing_simulation"
        notes.append("simulation adapter not configured/live; no buy/sell/call simulation executed")
        notes.append("honeypot confirmation is not available in this mode")
        return {
            **out,
            "signal_flags": {
                "simulation_unavailable": 1,
                "honeypot_unknown": 1,
                "buy_simulation_not_run": 1,
                "sell_simulation_not_run": 1,
                "call_simulation_not_run": 1,
            },
        }

    # Future-ready adapter shape (no network/provider execution here).
    available = bool(adapter.get("available"))
    if not available:
        out["simulation_mode"] = "adapter_ready"
        out["simulation_error_type"] = "provider_error"
        out["buy_simulation_status"] = "unavailable"
        out["sell_simulation_status"] = "unavailable"
        out["call_simulation_status"] = "unavailable"
        notes.append("simulation adapter declared but unavailable")
        return {
            **out,
            "signal_flags": {
                "simulation_unavailable": 1,
                "honeypot_unknown": 1,
                "buy_simulation_not_run": 1,
                "sell_simulation_not_run": 1,
                "call_simulation_not_run": 1,
            },
        }

    def _status(section):
        if not isinstance(section, dict):
            return "unknown"
        s = str(section.get("status") or "unknown").strip().lower()
        return s if s in _SIM_ALLOWED_STATUSES else "unknown"

    buy = _status(adapter.get("buy"))
    sell = _status(adapter.get("sell"))
    call = _status(adapter.get("call"))
    out["simulation_mode"] = "adapter_ready"
    out["simulation_available"] = True
    out["fallback_mode"] = False
    out["buy_simulation_status"] = buy
    out["sell_simulation_status"] = sell
    out["call_simulation_status"] = call
    out["honeypot_risk"] = "unknown"
    out["confidence_impact"] = "review_due_to_partial_simulation" if "unknown" in {buy, sell, call} else "none"
    notes.append("simulation adapter interface consumed; no honeypot confirmation claim")

    return {
        **out,
        "signal_flags": {
            "simulation_unavailable": 0,
            "honeypot_unknown": 1,
            "buy_simulation_not_run": 1 if buy in {"not_run", "unavailable"} else 0,
            "sell_simulation_not_run": 1 if sell in {"not_run", "unavailable"} else 0,
            "call_simulation_not_run": 1 if call in {"not_run", "unavailable"} else 0,
        },
    }

