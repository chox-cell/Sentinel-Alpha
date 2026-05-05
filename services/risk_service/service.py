import time
import uuid

from services.cache.redis_client import get_cache, set_cache
from services.cache.metrics import record_cache_hit, record_cache_miss
from services.scanner_engine import (
    analyzeContractRisk,
    buildAttestation,
    buildRiskDecision,
    buildRiskExplanation,
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
    explanation = buildRiskExplanation(
        decision=decision,
        asset_result=analysis["asset"],
        source_proxy_admin_result=analysis["source_proxy_admin"],
        erc20_result=analysis["erc20"],
        nft_zora_result=analysis["nft_zora"],
        simulation_result=analysis["simulation"],
        chain_read_result=analysis["chain_read"],
        signals=signals,
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
            "asset": {
                "asset_type": analysis["asset"]["asset_type"],
                "asset_confidence": analysis["asset"]["asset_confidence"],
                "classification_basis": analysis["asset"]["classification_basis"],
                "fallback_mode": analysis["asset"]["fallback_mode"],
                "unsupported_asset_type": analysis["asset"]["unsupported_asset_type"],
                "notes": analysis["asset"]["notes"],
                "signals": analysis["asset"]["signals"],
            },
            "security_signals": {
                "source_proxy_admin": {
                    "verified_source_status": analysis["source_proxy_admin"]["verified_source_status"],
                    "abi_available": analysis["source_proxy_admin"]["abi_available"],
                    "proxy_detected": analysis["source_proxy_admin"]["proxy_detected"],
                    "implementation_address": analysis["source_proxy_admin"]["implementation_address"],
                    "owner_admin_permissions": analysis["source_proxy_admin"]["owner_admin_permissions"],
                    "privileged_controls": analysis["source_proxy_admin"]["privileged_controls"],
                    "confidence_impact": analysis["source_proxy_admin"]["confidence_impact"],
                    "fallback_mode": analysis["source_proxy_admin"]["fallback_mode"],
                    "classification_basis": analysis["source_proxy_admin"]["classification_basis"],
                    "notes": analysis["source_proxy_admin"]["notes"],
                },
                "erc20": {
                    "erc20_analysis_status": analysis["erc20"]["erc20_analysis_status"],
                    "erc20_candidate": analysis["erc20"]["erc20_candidate"],
                    "transfer_tax_possible": analysis["erc20"]["transfer_tax_possible"],
                    "blacklist_possible": analysis["erc20"]["blacklist_possible"],
                    "pause_possible": analysis["erc20"]["pause_possible"],
                    "max_tx_possible": analysis["erc20"]["max_tx_possible"],
                    "max_wallet_possible": analysis["erc20"]["max_wallet_possible"],
                    "mint_possible": analysis["erc20"]["mint_possible"],
                    "owner_can_change_fees": analysis["erc20"]["owner_can_change_fees"],
                    "sell_restriction_possible": analysis["erc20"]["sell_restriction_possible"],
                    "honeypot_simulation_available": analysis["erc20"]["honeypot_simulation_available"],
                    "confidence_impact": analysis["erc20"]["confidence_impact"],
                    "fallback_mode": analysis["erc20"]["fallback_mode"],
                    "notes": analysis["erc20"]["notes"],
                },
                "nft_zora": {
                    "nft_zora_analysis_status": analysis["nft_zora"]["nft_zora_analysis_status"],
                    "erc721_candidate": analysis["nft_zora"]["erc721_candidate"],
                    "erc1155_candidate": analysis["nft_zora"]["erc1155_candidate"],
                    "zora_creator_coin_candidate": analysis["nft_zora"]["zora_creator_coin_candidate"],
                    "creator_asset_context": analysis["nft_zora"]["creator_asset_context"],
                    "transfer_restriction_possible": analysis["nft_zora"]["transfer_restriction_possible"],
                    "operator_approval_risk": analysis["nft_zora"]["operator_approval_risk"],
                    "mint_control_possible": analysis["nft_zora"]["mint_control_possible"],
                    "metadata_mutability_possible": analysis["nft_zora"]["metadata_mutability_possible"],
                    "royalty_admin_possible": analysis["nft_zora"]["royalty_admin_possible"],
                    "collection_age_unknown": analysis["nft_zora"]["collection_age_unknown"],
                    "zora_context_detected": analysis["nft_zora"]["zora_context_detected"],
                    "confidence_impact": analysis["nft_zora"]["confidence_impact"],
                    "fallback_mode": analysis["nft_zora"]["fallback_mode"],
                    "notes": analysis["nft_zora"]["notes"],
                },
                "simulation": {
                    "simulation_available": analysis["simulation"]["simulation_available"],
                    "simulation_mode": analysis["simulation"]["simulation_mode"],
                    "buy_simulation_status": analysis["simulation"]["buy_simulation_status"],
                    "sell_simulation_status": analysis["simulation"]["sell_simulation_status"],
                    "call_simulation_status": analysis["simulation"]["call_simulation_status"],
                    "honeypot_risk": analysis["simulation"]["honeypot_risk"],
                    "simulation_error_type": analysis["simulation"]["simulation_error_type"],
                    "confidence_impact": analysis["simulation"]["confidence_impact"],
                    "fallback_mode": analysis["simulation"]["fallback_mode"],
                    "notes": analysis["simulation"]["notes"],
                },
            },
            "security_explanation": explanation,
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
