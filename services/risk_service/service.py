import time
import uuid

from services.cache.redis_client import get_cache, set_cache
from services.cache.metrics import record_cache_hit, record_cache_miss
from services.scanner_engine import (
    analyzeContractRisk,
    buildAttestation,
    buildRiskDecision,
    normalizeContractAddress,
)

def evaluate_contract(contract_address: str, chain: str, context: dict | None = None) -> dict:
    result = evaluate_contract_with_meta(contract_address, chain, context)
    return result["response"]


def evaluate_contract_with_meta(contract_address: str, chain: str, context: dict | None = None) -> dict:
    start = time.time()
    trace_id = str(uuid.uuid4())

    normalized_addr = normalizeContractAddress(contract_address)
    normalized_chain = (chain or "base").strip().lower() or "base"
    cache_key = f"{normalized_chain}:{normalized_addr}:{hash(str(context))}"
    cached = get_cache(cache_key)
    if cached:
        record_cache_hit(cache_key)
        return {
            "response": cached,
            "cache_hit": True,
            "outcome_record": None,
        }
    record_cache_miss(cache_key)

    analysis = analyzeContractRisk(
        {
            "contract_address": normalized_addr,
            "chain": normalized_chain,
            "context": context,
        }
    )
    signals = analysis["signals"]
    decision = buildRiskDecision(signals)
    score = decision["score"]
    confidence = decision["confidence"]
    action = decision["action"]
    threat_class = decision["threat_class"]
    attestation = buildAttestation(
        decision=decision,
        contract_address=analysis["contract_address"],
        chain=analysis["chain"],
        trace_id=trace_id,
    )

    response = {
        "api_version": "2026.8.0",
        "decision": {
            "action": action,
            "emergency_signal": decision["emergency_signal"],
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
            "scanner_engine_version": "sentinel-scanner-v0",
            "chain_read": analysis["chain_read"],
            "fallback_mode": (
                not (analysis["viem_adapter"]["configured"] and analysis["whatsabi_adapter"]["configured"])
                or analysis["chain_read"]["chain_read_status"] != "ok"
            ),
        },
        "billing": {
            "amount": "0.02",
            "method": "x402",
            "status": "demo",
        },
    }

    set_cache(cache_key, response, ttl=300)
    return {
        "response": response,
        "cache_hit": False,
        "outcome_record": {
            "trace_id": trace_id,
            "contract_address": analysis["contract_address"],
            "chain": analysis["chain"],
            "score": score,
            "confidence": confidence,
            "action": action,
            "threat_class": threat_class,
            "signals": signals,
            "attestation": attestation,
            "created_at": response["attestation"]["signed_at"],
        },
    }
