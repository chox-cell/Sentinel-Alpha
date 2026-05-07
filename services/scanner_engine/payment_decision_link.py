import hashlib
import json
from datetime import datetime, timezone


FORBIDDEN_PAYMENT_KEYS = {
    "authorization",
    "headers",
    "cookies",
    "api_key",
    "private_key",
    "seed_phrase",
    "payment_signature",
    "wallet_private_key",
    "raw_payment_header",
    "raw_x402_payload",
    "bearer_token",
}


def _canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def get_payment_decision_link_status(config=None):
    _ = config if isinstance(config, dict) else {}
    return {
        "link_enabled": False,
        "link_mode": "disabled",
        "x402_settlement_required": False,
        "provider_required": False,
        "wallet_required": False,
        "private_key_required": False,
        "external_integration_status": "not_integrated",
        "notes": "Local boundary-only payment-decision linking status. No provider calls or settlement execution.",
    }


def sanitize_payment_context(payment_context):
    context = dict(payment_context or {}) if isinstance(payment_context, dict) else {}
    for key in FORBIDDEN_PAYMENT_KEYS:
        context.pop(key, None)

    if context.get("payer_id") and not context.get("payer_id_hash"):
        context["payer_id_hash"] = _sha256_hex(str(context.pop("payer_id")).strip())
    else:
        context.pop("payer_id", None)

    if context.get("facilitator_id") and not context.get("facilitator_id_hash"):
        context["facilitator_id_hash"] = _sha256_hex(str(context.pop("facilitator_id")).strip())
    else:
        context.pop("facilitator_id", None)

    allowed_protocols = {"x402", "lightning", "unknown"}
    allowed_status = {"required", "authorized", "settled", "failed", "unknown"}

    protocol = str(context.get("payment_protocol") or "unknown").strip().lower() or "unknown"
    status = str(context.get("payment_status") or "unknown").strip().lower() or "unknown"

    return {
        "payment_request_id": context.get("payment_request_id"),
        "payment_hash": context.get("payment_hash"),
        "payment_protocol": protocol if protocol in allowed_protocols else "unknown",
        "payment_status": status if status in allowed_status else "unknown",
        "amount": context.get("amount"),
        "currency": context.get("currency"),
        "payer_id_hash": context.get("payer_id_hash"),
        "facilitator_id_hash": context.get("facilitator_id_hash"),
        "created_at": context.get("created_at"),
    }


def build_payment_decision_link(decision_receipt, payment_context=None, config=None):
    safe_receipt = decision_receipt if isinstance(decision_receipt, dict) else {}
    safe_payment = sanitize_payment_context(payment_context)
    _ = config if isinstance(config, dict) else {}

    created_at = safe_payment.get("created_at") or safe_receipt.get("created_at") or datetime.now(timezone.utc).isoformat()
    payload = {
        "sentinel_decision_ref": safe_receipt.get("sentinel_decision_ref"),
        "action_ref": safe_receipt.get("action_ref"),
        "decision_id": safe_receipt.get("decision_id"),
        "payment_request_id": safe_payment.get("payment_request_id"),
        "payment_hash": safe_payment.get("payment_hash"),
        "payment_protocol": safe_payment.get("payment_protocol"),
        "payment_status": safe_payment.get("payment_status"),
        "chain": safe_receipt.get("chain"),
        "contract_address_hash": safe_receipt.get("contract_address_hash"),
        "decision_action": safe_receipt.get("decision_action"),
    }
    ref = _sha256_hex(_canonical_json(payload))
    return {
        "link_version": "v1",
        "payment_decision_link_ref": ref,
        "sentinel_decision_ref": safe_receipt.get("sentinel_decision_ref"),
        "action_ref": safe_receipt.get("action_ref"),
        "decision_id": safe_receipt.get("decision_id"),
        "payment_request_id": safe_payment.get("payment_request_id"),
        "payment_hash": safe_payment.get("payment_hash"),
        "payment_protocol": safe_payment.get("payment_protocol", "unknown"),
        "payment_status": safe_payment.get("payment_status", "unknown"),
        "chain": safe_receipt.get("chain"),
        "contract_address_hash": safe_receipt.get("contract_address_hash"),
        "decision_action": safe_receipt.get("decision_action"),
        "notSecurityGuarantee": True,
        "automatic_settlement_claimed": False,
        "external_integration_status": "not_integrated",
        "persistence_status": "not_persisted",
        "created_at": created_at,
        "notes": "Local deterministic payment-decision link boundary only; no automatic x402 settlement claim.",
    }
