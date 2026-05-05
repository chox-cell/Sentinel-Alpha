from __future__ import annotations

from datetime import datetime, timezone


_ALLOWED_FIELDS = {
    "chain",
    "address",
    "action",
    "token_in",
    "token_out",
    "amount",
    "calldata",
    "sender",
    "created_at",
}

_FORBIDDEN_FIELDS = {
    "private_key",
    "seed_phrase",
    "authorization",
    "api_key",
    "headers",
    "cookies",
    "payment_signature",
    "wallet_private_key",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_simulation_provider_status(config=None) -> dict:
    cfg = config if isinstance(config, dict) else {}
    enabled = cfg.get("enabled")
    if enabled in {True, 1, "1", "true", "True", "on", "ON"}:
        mode = "not_configured"
    elif enabled in {False, 0, "0", "false", "False", "off", "OFF"}:
        mode = "disabled"
    else:
        mode = "not_configured"
    return {
        "provider_enabled": False,
        "provider_mode": mode,
        "provider_required": False,
        "live_simulation_available": False,
        "wallet_required": False,
        "private_key_required": False,
        "write_attempted": False,
        "execution_attempted": False,
        "simulation_status": "not_run",
        "error_type": None,
        "notes": [
            "Live simulation provider is not configured by default.",
            "No wallet execution or transaction signing occurs in this boundary.",
            "No provider key is required by default.",
        ],
    }


def build_simulation_request(
    address=None,
    chain=None,
    action=None,
    token_in=None,
    token_out=None,
    amount=None,
    calldata=None,
    sender=None,
):
    return {
        "chain": (str(chain or "base").strip().lower() or "base"),
        "address": str(address or "").strip().lower(),
        "action": str(action or "").strip().lower(),
        "token_in": str(token_in or "").strip().lower() or None,
        "token_out": str(token_out or "").strip().lower() or None,
        "amount": amount,
        "calldata": str(calldata or "").strip().lower() or None,
        "sender": str(sender or "").strip().lower() or None,
        "created_at": _now_iso(),
    }


def sanitize_simulation_request(request):
    req = request if isinstance(request, dict) else {}
    out = {}
    for key in _ALLOWED_FIELDS:
        if key in req:
            out[key] = req[key]
    for blocked in _FORBIDDEN_FIELDS:
        out.pop(blocked, None)
    if "created_at" not in out:
        out["created_at"] = _now_iso()
    return out


def run_simulation_provider(request, config=None, provider_backend=None) -> dict:
    status = get_simulation_provider_status(config=config)
    sanitized = sanitize_simulation_request(request)
    default_result = {
        "simulation_provider_status": status["provider_mode"],
        "simulation_status": "not_run",
        "buy_simulation_status": "not_run",
        "sell_simulation_status": "not_run",
        "call_simulation_status": "not_run",
        "live_simulation_available": False,
        "honeypot_risk": "unknown",
        "provider_name": "none",
        "error_type": "not_configured",
        "confidence_impact": "low_confidence_due_to_simulation_unavailable",
        "fallback_mode": True,
        "notes": [
            "Simulation provider adapter boundary is disabled by default.",
            "No live simulation is executed in this mode.",
            "No honeypot detection claim is made.",
        ],
        "sanitized_request": sanitized,
        "write_attempted": False,
        "execution_attempted": False,
    }

    if provider_backend is None:
        return default_result

    if isinstance(provider_backend, dict):
        simulated = provider_backend.get("result")
    elif callable(provider_backend):
        simulated = provider_backend(sanitized)
    else:
        simulated = None

    if not isinstance(simulated, dict):
        return {
            **default_result,
            "simulation_provider_status": "not_configured",
            "error_type": "invalid_response",
            "notes": default_result["notes"] + ["Explicit test backend returned invalid response shape."],
        }

    # Explicit backend path is deterministic test mode only (still non-live).
    buy = str(simulated.get("buy_simulation_status") or "not_run")
    sell = str(simulated.get("sell_simulation_status") or "not_run")
    call = str(simulated.get("call_simulation_status") or "not_run")
    return {
        **default_result,
        "simulation_provider_status": str(simulated.get("simulation_provider_status") or "test_backend"),
        "simulation_status": str(simulated.get("simulation_status") or "simulated_test_only"),
        "buy_simulation_status": buy,
        "sell_simulation_status": sell,
        "call_simulation_status": call,
        "provider_name": str(simulated.get("provider_name") or "test_backend"),
        "error_type": simulated.get("error_type"),
        "notes": default_result["notes"] + ["Deterministic test backend used; this is not live simulation."],
    }
