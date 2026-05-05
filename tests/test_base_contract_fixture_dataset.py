import json
from pathlib import Path

from services.scanner_engine.asset_classification import classify_asset_type
from services.scanner_engine.erc20_heuristics import analyze_erc20_risk
from services.scanner_engine.local_bytecode_analyzer import analyze_bytecode_signals
from services.scanner_engine.nft_zora_heuristics import analyze_nft_zora_risk
from services.scanner_engine.source_proxy_admin import analyze_source_proxy_admin


FIXTURE_DIR = Path("tests/fixtures/base_contracts")
FIXTURES = [
    "known_generic_contract.json",
    "known_erc20_like_contract.json",
    "known_erc721_like_contract.json",
    "known_erc1155_like_contract.json",
    "known_proxy_like_contract.json",
    "known_router_like_contract.json",
    "known_pool_like_contract.json",
    "known_bytecode_opcode_contract.json",
]


def _load(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def test_all_fixture_files_exist_and_have_base_chain_expected_signals():
    for name in FIXTURES:
        path = FIXTURE_DIR / name
        assert path.exists(), f"missing fixture: {path}"
        payload = _load(name)
        assert payload["chain"] == "base"
        assert "expected_signals" in payload


def test_erc20_fixture_triggers_candidate_and_heuristics():
    fx = _load("known_erc20_like_contract.json")
    chain_read = {"chain_read_status": "ok", "account_type": "contract", "contract_code_available": True}
    asset = classify_asset_type(fx["address"], fx["chain"], chain_read_result=chain_read, abi_result=fx["abi_result"])
    spa = analyze_source_proxy_admin(
        fx["address"], fx["chain"], asset_result=asset, chain_read_result=chain_read, abi_result=fx["abi_result"]
    )
    erc20 = analyze_erc20_risk(
        fx["address"],
        fx["chain"],
        asset_result=asset,
        source_proxy_admin_result=spa,
        abi_result=fx["abi_result"],
        chain_read_result=chain_read,
    )
    assert erc20["erc20_candidate"] is True
    assert erc20["mint_possible"] is True


def test_erc721_and_erc1155_fixtures_trigger_candidates():
    chain_read = {"chain_read_status": "ok", "account_type": "contract", "contract_code_available": True}

    fx721 = _load("known_erc721_like_contract.json")
    asset721 = classify_asset_type(
        fx721["address"], fx721["chain"], chain_read_result=chain_read, abi_result=fx721["abi_result"]
    )
    nft721 = analyze_nft_zora_risk(
        fx721["address"],
        fx721["chain"],
        asset_result=asset721,
        abi_result=fx721["abi_result"],
        chain_read_result=chain_read,
    )
    assert nft721["erc721_candidate"] is True

    fx1155 = _load("known_erc1155_like_contract.json")
    asset1155 = classify_asset_type(
        fx1155["address"], fx1155["chain"], chain_read_result=chain_read, abi_result=fx1155["abi_result"]
    )
    nft1155 = analyze_nft_zora_risk(
        fx1155["address"],
        fx1155["chain"],
        asset_result=asset1155,
        abi_result=fx1155["abi_result"],
        chain_read_result=chain_read,
    )
    assert nft1155["erc1155_candidate"] is True


def test_proxy_fixture_triggers_proxy_candidate_or_pattern():
    fx = _load("known_proxy_like_contract.json")
    chain_read = {"chain_read_status": "ok", "account_type": "contract", "contract_code_available": True}
    asset = classify_asset_type(fx["address"], fx["chain"], chain_read_result=chain_read, abi_result=fx["abi_result"])
    spa = analyze_source_proxy_admin(
        fx["address"], fx["chain"], asset_result=asset, chain_read_result=chain_read, abi_result=fx["abi_result"]
    )
    bytecode = analyze_bytecode_signals(fx["address"], fx["chain"], bytecode=fx["bytecode"], chain_read_result=chain_read)
    assert (spa.get("proxy_candidate") is True) or (bytecode.get("proxy_pattern_possible") is True)


def test_opcode_fixture_triggers_opcode_presence_signals():
    fx = _load("known_bytecode_opcode_contract.json")
    out = analyze_bytecode_signals(fx["address"], fx["chain"], bytecode=fx["bytecode"], chain_read_result={"chain_read_status": "ok"})
    assert out["delegatecall_present"] is True
    assert out["selfdestruct_present"] is True
    assert out["external_call_present"] is True


def test_fixture_notes_avoid_overclaims():
    forbidden = [
        "honeypot detection",
        "guaranteed protection",
        "malicious certainty",
    ]
    for name in FIXTURES:
        notes = str(_load(name).get("notes", "")).lower()
        for phrase in forbidden:
            assert phrase not in notes
