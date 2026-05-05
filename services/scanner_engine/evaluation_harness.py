from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from services.scanner_engine.abi_source_adapter import analyze_abi_source_status
from services.scanner_engine.asset_classification import classify_asset_type
from services.scanner_engine.erc20_heuristics import analyze_erc20_risk
from services.scanner_engine.local_bytecode_analyzer import analyze_bytecode_signals
from services.scanner_engine.mempool_mev_boundary import analyze_mempool_mev_risk
from services.scanner_engine.nft_zora_heuristics import analyze_nft_zora_risk
from services.scanner_engine.router_pool_heuristics import analyze_router_pool_risk
from services.scanner_engine.simulation_provider_adapter import run_simulation_provider
from services.scanner_engine.source_proxy_admin import analyze_source_proxy_admin


DEFAULT_FIXTURE_PATH = Path("tests/fixtures/base_contracts")


def load_base_fixture_dataset(path=None):
    base = Path(path) if path else DEFAULT_FIXTURE_PATH
    fixtures: list[dict] = []
    for file in sorted(base.glob("*.json")):
        fixtures.append(json.loads(file.read_text(encoding="utf-8")))
    return fixtures


def _build_chain_read_fixture_context(fixture: dict) -> dict:
    fixture_type = str(fixture.get("fixture_type") or "").lower()
    if "eoa" in fixture_type:
        return {
            "chain_read_status": "ok",
            "account_type": "eoa",
            "contract_code_available": False,
        }
    return {
        "chain_read_status": "ok",
        "account_type": "contract",
        "contract_code_available": True,
    }


def _flatten_observed_signals(result: dict) -> dict:
    flat: dict = {}
    asset = result["asset"]
    spa = result["source_proxy_admin"]
    erc20 = result["erc20"]
    nft = result["nft_zora"]
    bytecode = result["bytecode"]
    router_pool = result["router_pool"]
    sim_provider = result["simulation_provider"]
    mempool = result["mempool_mev"]

    flat["asset_type"] = asset.get("asset_type")
    flat["erc20_candidate"] = erc20.get("erc20_candidate")
    flat["erc721_candidate"] = nft.get("erc721_candidate")
    flat["erc1155_candidate"] = nft.get("erc1155_candidate")
    flat["proxy_candidate"] = True if asset.get("asset_type") == "proxy_candidate" else False
    flat["proxy_pattern_possible"] = bytecode.get("proxy_pattern_possible")
    flat["delegatecall_present"] = bytecode.get("delegatecall_present")
    flat["selfdestruct_present"] = bytecode.get("selfdestruct_present")
    flat["external_call_present"] = bytecode.get("external_call_present")
    flat["selector_candidate_present"] = len(bytecode.get("selector_candidates") or []) > 0
    flat["source_proxy_admin_unknown"] = (
        spa.get("verified_source_status") in {"unknown", "unavailable"}
        and spa.get("owner_admin_permissions") == "unknown"
    )
    flat["transfer_tax_possible"] = erc20.get("transfer_tax_possible")
    flat["blacklist_possible"] = erc20.get("blacklist_possible")
    flat["mint_possible"] = erc20.get("mint_possible")
    flat["operator_approval_risk_possible"] = nft.get("operator_approval_risk")
    flat["router_candidate"] = router_pool.get("router_candidate")
    flat["pool_candidate"] = router_pool.get("pool_candidate")
    flat["live_simulation_available"] = sim_provider.get("live_simulation_available")
    flat["mempool_signal_available"] = mempool.get("mempool_signal_available")
    return flat


def evaluate_fixture(fixture):
    address = fixture.get("address")
    chain = fixture.get("chain", "base")
    abi_result = fixture.get("abi_result") if isinstance(fixture.get("abi_result"), dict) else {}
    chain_read = _build_chain_read_fixture_context(fixture)
    bytecode = fixture.get("bytecode") if isinstance(fixture.get("bytecode"), str) else None

    # v6.2/v6.4-compatible local fixture context (no network/provider dependency).
    abi_source = analyze_abi_source_status(
        address=address,
        chain=chain,
        provider_context={
            "provider_name": "local_fixture",
            "verified_source_status": "verified" if abi_result.get("available") else "unknown",
            "abi": [{"type": "function", "name": fn} for fn in abi_result.get("functions", [])],
        },
    )
    merged_abi = dict(abi_result)
    if not merged_abi:
        merged_abi = {
            "available": abi_source.get("abi_available") is True,
            "abi_available": abi_source.get("abi_available") is True,
            "verified_source": abi_source.get("verified_source_status") == "verified",
            "functions": abi_source.get("abi_function_names") or [],
            "selectors": [],
        }

    asset = classify_asset_type(address, chain, chain_read_result=chain_read, abi_result=merged_abi)
    source_proxy_admin = analyze_source_proxy_admin(
        address,
        chain,
        asset_result=asset,
        chain_read_result=chain_read,
        abi_result=merged_abi,
    )
    erc20 = analyze_erc20_risk(
        address,
        chain,
        asset_result=asset,
        source_proxy_admin_result=source_proxy_admin,
        abi_result=merged_abi,
        chain_read_result=chain_read,
    )
    nft_zora = analyze_nft_zora_risk(
        address,
        chain,
        asset_result=asset,
        source_proxy_admin_result=source_proxy_admin,
        abi_result=merged_abi,
        chain_read_result=chain_read,
    )
    bytecode_analysis = analyze_bytecode_signals(
        address=address,
        chain=chain,
        bytecode=bytecode,
        chain_read_result=chain_read,
    )
    router_pool = analyze_router_pool_risk(
        address=address,
        chain=chain,
        asset_result=asset,
        abi_result=merged_abi,
        bytecode_result=bytecode_analysis,
        source_proxy_admin_result=source_proxy_admin,
    )
    simulation_provider = run_simulation_provider(
        {"chain": chain, "address": address, "action": "evaluate_fixture"},
        provider_backend=None,
    )
    mempool_mev = analyze_mempool_mev_risk(
        address=address,
        chain=chain,
        asset_result=asset,
        simulation_result={"simulation_available": simulation_provider.get("live_simulation_available")},
        mempool_context={},
        config={},
    )

    observed = _flatten_observed_signals(
        {
            "asset": asset,
            "source_proxy_admin": source_proxy_admin,
            "erc20": erc20,
            "nft_zora": nft_zora,
            "bytecode": bytecode_analysis,
            "router_pool": router_pool,
            "simulation_provider": simulation_provider,
            "mempool_mev": mempool_mev,
        }
    )
    expected = fixture.get("expected_signals", {}) if isinstance(fixture.get("expected_signals"), dict) else {}

    matched = []
    missing = []
    for key, val in expected.items():
        if observed.get(key) == val:
            matched.append(key)
        else:
            missing.append(key)

    unexpected = [k for k, v in observed.items() if v is True and k not in expected]
    status = "pass" if not missing else "review"

    return {
        "fixture_name": fixture.get("name"),
        "fixture_type": fixture.get("fixture_type"),
        "expected_signals": expected,
        "observed_signals": observed,
        "matched_signals": matched,
        "missing_expected_signals": missing,
        "unexpected_signals": unexpected,
        "evaluation_status": status,
        "notes": [
            "Local regression evaluation only; not a security guarantee.",
            "Offline fixture-based result; no live provider/network dependency.",
        ],
    }


def evaluate_fixture_dataset(fixtures):
    return [evaluate_fixture(fx) for fx in fixtures]


def summarize_evaluation_results(results):
    total = len(results)
    passed = sum(1 for r in results if r.get("evaluation_status") == "pass")
    review = total - passed
    by_type = Counter(str(r.get("fixture_type") or "unknown") for r in results)
    missing_by_fixture = {
        str(r.get("fixture_name") or "unknown"): r.get("missing_expected_signals", [])
        for r in results
        if r.get("missing_expected_signals")
    }
    return {
        "total_fixtures": total,
        "passed": passed,
        "review": review,
        "coverage_by_fixture_type": dict(by_type),
        "missing_expected_signals": missing_by_fixture,
        "notes": [
            "Evaluation harness is local/offline only.",
            "Results are regression checks, not security guarantees.",
            "Does not prove honeypot detection or full bytecode coverage.",
        ],
    }
