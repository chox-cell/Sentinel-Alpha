from services.attestation_layer.attestation import build_attestation as _build_attestation
from services.mycelium_engine.engine import classify_threat, compute_confidence, compute_score, decide
from services.scanner_engine.adapters import get_viem_readiness, get_whatsabi_readiness
from services.signals.extractor import extract_signals
from services.signals.validators import normalize_address


def normalizeContractAddress(address: str) -> str:
    return normalize_address(address)


def analyzeContractRisk(input_data: dict) -> dict:
    """
    v0 analysis boundary:
    - extracts deterministic signals
    - returns adapter readiness (no chain-read hard dependency yet)
    """
    contract_address = normalizeContractAddress(input_data.get("contract_address", ""))
    chain = (input_data.get("chain") or "base").strip().lower() or "base"
    context = input_data.get("context") if isinstance(input_data.get("context"), dict) else {}

    extracted = extract_signals(contract_address, chain, context)
    return {
        "contract_address": extracted["contract_address"],
        "chain": extracted["chain"],
        "signals": extracted["signals"],
        "viem_adapter": get_viem_readiness(),
        "whatsabi_adapter": get_whatsabi_readiness(),
    }


def buildRiskDecision(signals: dict) -> dict:
    score = compute_score(signals)
    confidence = compute_confidence(signals)
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

