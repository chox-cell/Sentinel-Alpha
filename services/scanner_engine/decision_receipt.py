import hashlib
import json
from datetime import datetime, timezone


def _sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sanitize_context(request_context: dict) -> dict:
    context = dict(request_context or {})
    contract_address = str(context.get("contract_address") or "").strip().lower()
    requested_action = str(context.get("requested_action") or "").strip().lower() or "unknown"
    chain = str(context.get("chain") or "base").strip().lower() or "base"
    intent = context.get("intent")
    policy_version = str(context.get("policy_version") or "sentinel-policy-v0")
    created_at = context.get("created_at")
    trace_or_receipt = context.get("trace_id") or context.get("receipt_id")
    return {
        "contract_address": contract_address,
        "requested_action": requested_action,
        "chain": chain,
        "intent": intent,
        "policy_version": policy_version,
        "created_at": created_at,
        "trace_or_receipt": trace_or_receipt,
    }


def _extract_signals_summary(response: dict) -> dict:
    signals = response.get("signals")
    if not isinstance(signals, dict):
        return {"total": 0, "active_count": 0, "active_signals": []}
    active = sorted([key for key, value in signals.items() if bool(value)])
    return {
        "total": len(signals),
        "active_count": len(active),
        "active_signals": active[:25],
    }


def build_decision_receipt(response, request_context=None, config=None):
    """Build a deterministic, local-only decision receipt for trust-loop references."""
    safe_response = response if isinstance(response, dict) else {}
    safe_context = _sanitize_context(request_context if isinstance(request_context, dict) else {})
    safe_config = config if isinstance(config, dict) else {}

    chain = safe_context["chain"] or str(safe_response.get("meta", {}).get("chain_read", {}).get("chain") or "base").lower()
    contract_address_hash = _sha256_hex(safe_context["contract_address"]) if safe_context["contract_address"] else "missing"
    requested_action = safe_context["requested_action"]

    intent = safe_context["intent"]
    if isinstance(intent, dict):
        intent_hash = _sha256_hex(_canonical_json(intent))
    elif isinstance(intent, str) and intent.strip():
        intent_hash = _sha256_hex(intent.strip())
    else:
        intent_hash = "missing"

    explanation = safe_response.get("meta", {}).get("security_explanation")
    explanation_hash = _sha256_hex(_canonical_json(explanation if explanation is not None else {}))

    decision_block = safe_response.get("decision", {}) if isinstance(safe_response.get("decision"), dict) else {}
    risk_metrics = safe_response.get("risk_metrics", {}) if isinstance(safe_response.get("risk_metrics"), dict) else {}

    action_ref_payload = {
        "chain": chain,
        "contract_address_hash": contract_address_hash,
        "requested_action": requested_action,
        "intent_hash": intent_hash,
    }
    action_ref = _sha256_hex(_canonical_json(action_ref_payload))

    canonical_payload = {
        "action_ref": action_ref,
        "chain": chain,
        "contract_address_hash": contract_address_hash,
        "decision_action": decision_block.get("action"),
        "explanation_hash": explanation_hash,
        "intent_hash": intent_hash,
        "policy_version": safe_context["policy_version"] or str(safe_config.get("policy_version") or "sentinel-policy-v0"),
        "requested_action": requested_action,
        "risk_score": risk_metrics.get("score"),
        "signals_summary": _extract_signals_summary(safe_response),
    }
    sentinel_decision_ref = _sha256_hex(_canonical_json(canonical_payload))

    created_at = safe_context["created_at"] or safe_response.get("attestation", {}).get("signed_at")
    if not created_at:
        created_at = datetime.now(timezone.utc).isoformat()

    receipt = {
        "receipt_version": "v1",
        "decision_id": sentinel_decision_ref[:24],
        "sentinel_decision_ref": sentinel_decision_ref,
        "action_ref": action_ref,
        "chain": chain,
        "contract_address_hash": contract_address_hash,
        "requested_action": requested_action,
        "intent_hash": intent_hash,
        "decision_action": decision_block.get("action"),
        "confidence": decision_block.get("confidence"),
        "risk_score": risk_metrics.get("score"),
        "signals_summary": canonical_payload["signals_summary"],
        "explanation_hash": explanation_hash,
        "policy_version": canonical_payload["policy_version"],
        "created_at": created_at,
        "notSecurityGuarantee": True,
        "persistence_status": "not_persisted",
        "external_integration_status": "not_integrated",
        "notes": "Local deterministic decision receipt boundary for reference and audit-linking context only.",
    }

    trace_or_receipt = safe_context.get("trace_or_receipt")
    if trace_or_receipt:
        receipt["trace_id_or_receipt_id"] = str(trace_or_receipt)
    return receipt
