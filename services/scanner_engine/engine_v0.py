from services.attestation_layer.attestation import build_attestation as _build_attestation
from services.mycelium_engine.engine import classify_threat, compute_confidence, compute_score, decide
from services.scanner_engine.adapters import get_viem_readiness, get_whatsabi_readiness
from services.scanner_engine.asset_classification import classify_asset_type
from services.scanner_engine.chain_support import get_chain_support
from services.scanner_engine.erc20_heuristics import analyze_erc20_risk
from services.scanner_engine.intent_alignment import analyze_intent_alignment
from services.scanner_engine.mempool_mev_boundary import analyze_mempool_mev_risk
from services.scanner_engine.nft_zora_heuristics import analyze_nft_zora_risk
from services.scanner_engine.risk_explanation import build_risk_explanation
from services.scanner_engine.simulation_boundary import analyze_simulation_risk
from services.scanner_engine.source_proxy_admin import analyze_source_proxy_admin
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
    abi_result = context.get("abi_result") if isinstance(context.get("abi_result"), dict) else {}
    simulation_request = context.get("simulation_request") if isinstance(context.get("simulation_request"), dict) else {}
    simulation_config = context.get("simulation_config") if isinstance(context.get("simulation_config"), dict) else {}
    intent_payload = context.get("intent") if isinstance(context.get("intent"), dict) else None
    requested_action = context.get("requested_action") if isinstance(context.get("requested_action"), str) else None
    mempool_context = context.get("mempool_context") if isinstance(context.get("mempool_context"), dict) else {}
    mempool_config = context.get("mempool_config") if isinstance(context.get("mempool_config"), dict) else {}

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

    asset = classify_asset_type(
        extracted["contract_address"],
        chain,
        chain_read_result=chain_read,
        abi_result=abi_result,
    )
    source_proxy_admin = analyze_source_proxy_admin(
        extracted["contract_address"],
        chain,
        asset_result=asset,
        chain_read_result=chain_read,
        abi_result=abi_result,
    )
    erc20 = analyze_erc20_risk(
        extracted["contract_address"],
        chain,
        asset_result=asset,
        source_proxy_admin_result=source_proxy_admin,
        abi_result=abi_result,
        chain_read_result=chain_read,
    )
    nft_zora = analyze_nft_zora_risk(
        extracted["contract_address"],
        chain,
        asset_result=asset,
        source_proxy_admin_result=source_proxy_admin,
        abi_result=abi_result,
        chain_read_result=chain_read,
    )
    simulation = analyze_simulation_risk(
        extracted["contract_address"],
        chain,
        asset_result=asset,
        erc20_result=erc20,
        nft_zora_result=nft_zora,
        source_proxy_admin_result=source_proxy_admin,
        simulation_request=simulation_request,
        config=simulation_config,
    )
    merged.update(source_proxy_admin.get("signal_flags", {}))
    merged.update(erc20.get("signal_flags", {}))
    merged.update(nft_zora.get("signal_flags", {}))
    merged.update(simulation.get("signal_flags", {}))
    chain_support = get_chain_support(chain)
    intent_alignment = analyze_intent_alignment(
        intent=intent_payload,
        requested_action=requested_action,
        address=extracted["contract_address"],
        chain=chain,
        asset_result=asset,
        source_proxy_admin_result=source_proxy_admin,
        erc20_result=erc20,
        nft_zora_result=nft_zora,
        simulation_result=simulation,
        chain_support_result=chain_support,
    )
    merged.update(intent_alignment.get("signal_flags", {}))
    mempool_mev = analyze_mempool_mev_risk(
        address=extracted["contract_address"],
        chain=chain,
        asset_result=asset,
        intent_result=intent_alignment,
        simulation_result=simulation,
        mempool_context=mempool_context,
        config=mempool_config,
    )
    merged.update(mempool_mev.get("signal_flags", {}))

    return {
        "contract_address": extracted["contract_address"],
        "chain": extracted["chain"],
        "signals": merged,
        "chain_support": chain_support,
        "asset": asset,
        "source_proxy_admin": source_proxy_admin,
        "erc20": erc20,
        "nft_zora": nft_zora,
        "simulation": simulation,
        "intent_alignment": intent_alignment,
        "mempool_mev": mempool_mev,
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


def buildRiskExplanation(
    decision=None,
    asset_result=None,
    source_proxy_admin_result=None,
    erc20_result=None,
    nft_zora_result=None,
    simulation_result=None,
    chain_read_result=None,
    signals=None,
) -> dict:
    return build_risk_explanation(
        decision=decision,
        asset_result=asset_result,
        source_proxy_admin_result=source_proxy_admin_result,
        erc20_result=erc20_result,
        nft_zora_result=nft_zora_result,
        simulation_result=simulation_result,
        chain_read_result=chain_read_result,
        signals=signals,
    )
