from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_identifier(value: str) -> str:
    raw = (value or "").strip().lower().encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def get_risk_history_status(config=None) -> dict:
    cfg = config if isinstance(config, dict) else {}
    enabled = cfg.get("enabled")
    if enabled in {True, 1, "1", "true", "True", "on", "ON"}:
        mode = "not_configured"
    elif enabled in {False, 0, "0", "false", "False", "off", "OFF"}:
        mode = "disabled"
    else:
        mode = "not_configured"

    return {
        "persistence_enabled": False,
        "persistence_mode": mode,
        "database_url_required": False,
        "write_attempted": False,
        "write_status": "not_run",
        "error_type": None,
        "notes": [
            "Risk history runtime persistence is disabled by default.",
            "No DATABASE_URL is required at this stage.",
            "Local DB boundary is planning-only until future rollout.",
        ],
    }


def build_scan_record(response, request_meta=None) -> dict:
    body = response if isinstance(response, dict) else {}
    req = request_meta if isinstance(request_meta, dict) else {}

    trace_id = str(body.get("meta", {}).get("trace_id") or "")
    chain = str(req.get("chain") or body.get("meta", {}).get("chain_read", {}).get("chain") or "unknown").lower()
    contract_address = str(req.get("contract_address") or "")
    contract_address_hash = _hash_identifier(f"{chain}:{contract_address}") if contract_address else "unknown"

    attestation = body.get("attestation", {}) if isinstance(body.get("attestation"), dict) else {}
    attestation_id = str(attestation.get("attestation_id") or "")
    attestation_hash = _hash_identifier(attestation_id) if attestation_id else None

    return {
        "request_id": str(req.get("request_id") or trace_id or uuid.uuid4()),
        "trace_id": trace_id or None,
        "chain": chain,
        "contract_address_hash": contract_address_hash,
        "score": body.get("risk_metrics", {}).get("score"),
        "action": body.get("decision", {}).get("action"),
        "confidence": body.get("decision", {}).get("confidence"),
        "risk_metrics_snapshot": body.get("risk_metrics", {}),
        "security_signals_snapshot": body.get("meta", {}).get("security_signals", {}),
        "attestation_hash": attestation_hash,
        "created_at": _utc_now_iso(),
        "privacy_notes": [
            "No private keys.",
            "No seed phrases.",
            "No raw secrets.",
            "No raw payment headers.",
        ],
    }


def persist_scan_result(record, config=None) -> dict:
    _ = record if isinstance(record, dict) else {}
    status = get_risk_history_status(config=config)
    return {
        **status,
        "record_id": None,
    }
