import time
import uuid

from services.cache.redis_client import get_cache, set_cache
from services.signals.extractor import extract_signals
from services.mycelium_engine.engine import (
    compute_score,
    compute_confidence,
    decide,
    classify_threat,
)
from services.attestation_layer.attestation import build_attestation

def evaluate_contract(contract_address: str, chain: str, context: dict | None = None) -> dict:
    start = time.time()
    trace_id = str(uuid.uuid4())

    cache_key = f"{chain}:{contract_address}:{hash(str(context))}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    extracted = extract_signals(contract_address, chain, context)
    signals = extracted["signals"]

    score = compute_score(signals)
    confidence = compute_confidence(signals)
    action = decide(score, confidence, signals)
    threat_class = classify_threat(signals)

    attestation = build_attestation(
        contract_address=extracted["contract_address"],
        chain=extracted["chain"],
        score=score,
        action=action,
        trace_id=trace_id,
    )

    response = {
        "api_version": "2026.8.0",
        "decision": {
            "action": action,
            "emergency_signal": "EXIT_NOW" if action == "EXIT_NOW" else "NONE",
            "confidence": confidence,
        },
        "risk_metrics": {
            "score": score,
            "threat_class": threat_class,
        },
        "signals": signals,
        "attestation": attestation,
        "latency": {
            "lane": "standard",
            "latency_ms": int((time.time() - start) * 1000),
        },
        "meta": {
            "ttl_seconds": 300,
            "trace_id": trace_id,
        },
        "billing": {
            "amount": "0.02",
            "method": "x402",
            "status": "demo",
        },
    }

    set_cache(cache_key, response, ttl=300)
    return response
