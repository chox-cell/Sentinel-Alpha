from services.attestation_layer.attestation import build_attestation as _build_attestation
from services.mycelium_engine.engine import classify_threat, compute_confidence, compute_score, decide
from services.scanner_engine.adapters import get_viem_readiness, get_whatsabi_readiness
from services.scanner_engine.chain_read_adapter import classify_account_type, get_chain_readiness
from services.signals.extractor import extract_signals
from services.signals.validators import normalize_address


def normalizeContractAddress(address: str) -> str:
    return normalize_address(address)


def _merge_chain_read_signals(signals: dict, contract_address: str, chain: str) -> tuple[dict, dict]:
    """Augment signals with chain-read heuristics; return (signals, chain_read meta block)."""
    readiness = get_chain_readiness(chain)
    classified = classify_account_type(contract_address, chain)
    fetch_status = classified["code_fetch_status"]
    account_type = str(classified.get("account_type") or "unknown")

    out = dict(signals)
    out["contract_code_available"] = 1 if fetch_status == "ok" and account_type == "contract" else 0
    out["chain_read_provider_unavailable"] = (
        1
        if fetch_status in {"not_configured", "unsupported_chain", "provider_error", "reads_disabled"}
        else 0
    )
    out["eoa_account"] = 1 if fetch_status == "ok" and account_type == "eoa" else 0
    # Only downgrade confidence when RPC failed after an attempt—not when RPC is intentionally absent.
    out["unknown_account_kind"] = 1 if fetch_status == "provider_error" else 0

    chain_read = {
        "chain_read_status": fetch_status,
        "account_type": account_type,
        "adapter_mode": readiness["adapter_mode"],
        "contract_code_available": bool(out["contract_code_available"]),
    }
    return out, chain_read


def analyzeContractRisk(input_data: dict) -> dict:
    """
    v0 analysis boundary:
    - extracts deterministic signals
    - optional JSON-RPC chain read (BASE_RPC_URL, Base only) — Viem-equivalent path can live in SDK later
    """
    contract_address = normalizeContractAddress(input_data.get("contract_address", ""))
    chain = (input_data.get("chain") or "base").strip().lower() or "base"
    context = input_data.get("context") if isinstance(input_data.get("context"), dict) else {}

    extracted = extract_signals(contract_address, chain, context)
    signals = extracted["signals"]

    if signals.get("zero_address"):
        readiness = get_chain_readiness(chain)
        merged = dict(signals)
        merged["contract_code_available"] = 0
        merged["eoa_account"] = 0
        merged["unknown_account_kind"] = 0
        merged["chain_read_provider_unavailable"] = 0
        chain_read = {
            "chain_read_status": "unavailable",
            "account_type": "unknown",
            "adapter_mode": readiness["adapter_mode"],
            "contract_code_available": False,
        }
    else:
        merged, chain_read = _merge_chain_read_signals(signals, extracted["contract_address"], chain)

    return {
        "contract_address": extracted["contract_address"],
        "chain": extracted["chain"],
        "signals": merged,
        "viem_adapter": get_viem_readiness(),
        "whatsabi_adapter": get_whatsabi_readiness(),
        "chain_read": chain_read,
    }


def buildRiskDecision(signals: dict) -> dict:
    score = compute_score(signals)
    confidence = compute_confidence(signals)

    if signals.get("eoa_account"):
        confidence = min(confidence, 0.48)
    if signals.get("unknown_account_kind") and not signals.get("zero_address"):
        confidence = min(confidence, 0.42)

    action = decide(score, confidence, signals)
    threat_class = classify_threat(signals)
    return {
        "score": score,
        "confidence": confidence,
        "action": action,
        "threat_class": threat_class,
        "emergency_signal": "EXIT_NOW" if action == "EXIT_NOW" else "NONE",
    }


def buildAttestation(decision: dict, contract_address: str, chain: str, trace_id: str) -> dict:
    return _build_attestation(
        contract_address=contract_address,
        chain=chain,
        score=decision["score"],
        action=decision["action"],
        trace_id=trace_id,
    )
