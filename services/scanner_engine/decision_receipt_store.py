from datetime import datetime, timezone
import hashlib


SAFE_RECEIPT_FIELDS = {
    "receipt_version",
    "decision_id",
    "sentinel_decision_ref",
    "action_ref",
    "chain",
    "contract_address_hash",
    "requested_action",
    "intent_hash",
    "decision_action",
    "confidence",
    "risk_score",
    "signals_summary",
    "explanation_hash",
    "policy_version",
    "created_at",
    "notSecurityGuarantee",
}

FORBIDDEN_KEYS = {
    "contract_address",
    "private_key",
    "seed_phrase",
    "authorization",
    "api_key",
    "headers",
    "cookies",
    "payment_signature",
    "wallet_private_key",
    "raw_prompt",
    "prompt",
    "raw_intent_text",
    "intent_text",
}


def get_decision_receipt_store_status(config=None):
    _ = config if isinstance(config, dict) else {}
    return {
        "store_enabled": False,
        "store_mode": "disabled",
        "database_required": False,
        "redis_required": False,
        "filesystem_required": False,
        "write_attempted": False,
        "write_status": "not_run",
        "persistence_status": "not_persisted",
    }


def sanitize_decision_receipt_for_storage(receipt):
    source = receipt if isinstance(receipt, dict) else {}
    sanitized = {k: source.get(k) for k in SAFE_RECEIPT_FIELDS if k in source}
    for key in FORBIDDEN_KEYS:
        sanitized.pop(key, None)
    return sanitized


def _hash_client_id(client_id_value) -> str | None:
    if not client_id_value:
        return None
    raw = str(client_id_value).strip()
    if not raw:
        return None
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_decision_receipt_store_record(receipt, request_meta=None):
    sanitized = sanitize_decision_receipt_for_storage(receipt)
    safe_meta = request_meta if isinstance(request_meta, dict) else {}
    record_request_meta = {}
    if safe_meta.get("request_id"):
        record_request_meta["request_id"] = str(safe_meta["request_id"])
    client_id_hash = _hash_client_id(safe_meta.get("client_id"))
    if client_id_hash:
        record_request_meta["client_id_hash"] = client_id_hash
    if safe_meta.get("source"):
        record_request_meta["source"] = str(safe_meta["source"])

    return {
        "record_version": "v1",
        "record_type": "sentinel_decision_receipt",
        "receipt": sanitized,
        "request_meta": record_request_meta,
        "storage_privacy_notes": (
            "Sanitized storage boundary only. No raw contract addresses, headers, "
            "cookies, secrets, payment signatures, or wallet private keys."
        ),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def persist_decision_receipt(record, config=None, store_backend=None):
    _ = config if isinstance(config, dict) else {}
    safe_record = build_decision_receipt_store_record(
        receipt=(record.get("receipt") if isinstance(record, dict) and isinstance(record.get("receipt"), dict) else record),
        request_meta=(record.get("request_meta") if isinstance(record, dict) and isinstance(record.get("request_meta"), dict) else None),
    )
    if store_backend is None:
        return {
            "write_attempted": False,
            "write_status": "not_run",
            "persistence_status": "not_persisted",
            "error_type": None,
        }

    if isinstance(store_backend, list):
        store_backend.append(safe_record)
    elif isinstance(store_backend, dict):
        key = safe_record["receipt"].get("sentinel_decision_ref") or safe_record["receipt"].get("decision_id") or "record"
        store_backend[key] = safe_record
    else:
        return {
            "write_attempted": False,
            "write_status": "not_run",
            "persistence_status": "not_persisted",
            "error_type": "unsupported_test_backend",
        }

    return {
        "write_attempted": True,
        "write_status": "written_to_test_backend",
        "persistence_status": "stored_in_test_backend",
        "test_only": True,
        "error_type": None,
    }
