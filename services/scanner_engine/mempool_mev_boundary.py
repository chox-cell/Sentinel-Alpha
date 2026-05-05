from __future__ import annotations


def analyze_mempool_mev_risk(
    address=None,
    chain=None,
    asset_result=None,
    intent_result=None,
    simulation_result=None,
    mempool_context=None,
    config=None,
):
    """
    v5.9 mempool/MEV boundary.
    Default is not_configured with unknown/unavailable outputs.
    No external provider calls are made here.
    """
    asset_result = asset_result or {}
    intent_result = intent_result or {}
    simulation_result = simulation_result or {}
    mempool_context = mempool_context or {}
    config = config or {}

    chain_norm = (chain or "base").strip().lower() or "base"
    adapter = config.get("adapter")
    enabled = bool(config.get("enabled")) and isinstance(adapter, dict)

    out = {
        "mempool_signal_available": False,
        "mempool_mode": "disabled",
        "pending_activity_status": "unavailable",
        "mev_risk": "unknown",
        "front_run_observed": "unknown",
        "sandwich_risk": "unknown",
        "liquidity_attack_pressure": "unknown",
        "mempool_error_type": None,
        "confidence_impact": "none",
        "fallback_mode": True,
        "notes": [],
    }

    if not enabled:
        out["mempool_mode"] = "not_configured"
        out["mempool_error_type"] = "not_configured"
        out["confidence_impact"] = "review_due_to_missing_mempool_data"
        out["notes"].append("Mempool/MEV data is not configured/live in current runtime.")
        out["notes"].append("Boundary provides signals only; it does not claim blocking of MEV or front-running.")
        return {
            **out,
            "signal_flags": {
                "mempool_signal_unavailable": 1,
                "mev_risk_unknown": 1,
                "front_run_unknown": 1,
                "sandwich_risk_unknown": 1,
                "mempool_not_configured": 1,
            },
        }

    # Future adapter interface only (still no provider call here).
    available = bool(adapter.get("available"))
    if not available:
        out["mempool_mode"] = "adapter_ready"
        out["mempool_error_type"] = "provider_error"
        out["notes"].append("Mempool adapter declared but unavailable.")
        return {
            **out,
            "signal_flags": {
                "mempool_signal_unavailable": 1,
                "mev_risk_unknown": 1,
                "front_run_unknown": 1,
                "sandwich_risk_unknown": 1,
                "mempool_not_configured": 0,
            },
        }

    def _enum(value, allowed, default):
        if isinstance(value, str) and value.strip().lower() in allowed:
            return value.strip().lower()
        return default

    def _tri(value):
        if value in (True, False, "unknown"):
            return value
        if isinstance(value, str) and value.strip().lower() == "unknown":
            return "unknown"
        return "unknown"

    out["mempool_mode"] = "adapter_ready"
    out["mempool_signal_available"] = True
    out["fallback_mode"] = False
    out["pending_activity_status"] = _enum(
        adapter.get("pending_activity_status"),
        {"low", "elevated", "high", "unknown"},
        "unknown",
    )
    out["mev_risk"] = _enum(adapter.get("mev_risk"), {"low", "medium", "high", "unknown"}, "unknown")
    out["front_run_observed"] = _tri(adapter.get("front_run_observed"))
    out["sandwich_risk"] = _enum(adapter.get("sandwich_risk"), {"low", "medium", "high", "unknown"}, "unknown")
    out["liquidity_attack_pressure"] = _enum(
        adapter.get("liquidity_attack_pressure"),
        {"low", "medium", "high", "unknown"},
        "unknown",
    )
    out["confidence_impact"] = (
        "review_due_to_partial_mempool_data"
        if "unknown" in {
            out["pending_activity_status"],
            out["mev_risk"],
            out["sandwich_risk"],
            out["liquidity_attack_pressure"],
            out["front_run_observed"],
        }
        else "none"
    )
    out["notes"].append("Mempool/MEV boundary uses adapter outputs only; no prevention guarantee.")

    return {
        **out,
        "signal_flags": {
            "mempool_signal_unavailable": 0,
            "mev_risk_unknown": 1 if out["mev_risk"] == "unknown" else 0,
            "front_run_unknown": 1 if out["front_run_observed"] == "unknown" else 0,
            "sandwich_risk_unknown": 1 if out["sandwich_risk"] == "unknown" else 0,
            "mempool_not_configured": 0,
        },
    }

