from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service
from services.scanner_engine.nft_zora_heuristics import analyze_nft_zora_risk


def test_eoa_not_applicable(monkeypatch):
    class _RpcOkEoa:
        status_code = 200

        def json(self):
            return {"jsonrpc": "2.0", "id": 1, "result": "0x"}

    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setenv("BASE_RPC_URL", "http://fixture.local.invalid")
    monkeypatch.setenv("SENTINEL_CHAIN_READ_ENABLED", "true")
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")
    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        lambda *_a, **_k: _RpcOkEoa(),
    )
    result = service.evaluate_contract("0x2222222222222222222222222222222222222222", "base")
    nz = result["meta"]["security_signals"]["nft_zora"]
    assert nz["nft_zora_analysis_status"] == "not_applicable"


def test_generic_contract_without_abi_stays_unknown(monkeypatch):
    class _RpcOkContract:
        status_code = 200

        def json(self):
            return {"jsonrpc": "2.0", "id": 1, "result": "0x60006000"}

    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setenv("BASE_RPC_URL", "http://fixture.local.invalid")
    monkeypatch.setenv("SENTINEL_CHAIN_READ_ENABLED", "true")
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")
    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        lambda *_a, **_k: _RpcOkContract(),
    )
    result = service.evaluate_contract("0x4444444444444444444444444444444444444444", "base")
    nz = result["meta"]["security_signals"]["nft_zora"]
    assert nz["nft_zora_analysis_status"] in {"unknown", "unavailable"}
    assert nz["erc721_candidate"] == "unknown"
    assert nz["erc1155_candidate"] == "unknown"


def test_erc721_candidate_from_abi_hints():
    out = analyze_nft_zora_risk(
        "0x1111111111111111111111111111111111111111",
        "base",
        asset_result={"asset_type": "generic_contract"},
        source_proxy_admin_result={"abi_available": True},
        chain_read_result={"chain_read_status": "ok"},
        abi_result={"available": True, "functions": ["ownerOf", "safeTransferFrom", "setApprovalForAll"], "selectors": []},
    )
    assert out["erc721_candidate"] is True


def test_erc1155_candidate_from_abi_hints():
    out = analyze_nft_zora_risk(
        "0x1111111111111111111111111111111111111111",
        "base",
        asset_result={"asset_type": "generic_contract"},
        source_proxy_admin_result={"abi_available": True},
        chain_read_result={"chain_read_status": "ok"},
        abi_result={"available": True, "functions": ["safeBatchTransferFrom", "balanceOfBatch", "setApprovalForAll"], "selectors": []},
    )
    assert out["erc1155_candidate"] is True


def test_zora_context_possible_from_hints():
    out = analyze_nft_zora_risk(
        "0x1111111111111111111111111111111111111111",
        "base",
        asset_result={"asset_type": "generic_contract"},
        source_proxy_admin_result={"abi_available": True},
        chain_read_result={"chain_read_status": "ok"},
        abi_result={"available": True, "functions": ["createEdition", "royaltyInfo", "mintWithRewards"], "selectors": ["0xzora"]},
    )
    assert out["zora_context_detected"] is True
    assert out["zora_creator_coin_candidate"] is True
    notes = " ".join(out["notes"]).lower()
    assert "does not claim full zora support" in notes
    assert "does not claim all nft transfer/metadata risks are covered" in notes


def test_additive_metadata_and_top_level_compat(monkeypatch):
    from apps.api import main

    monkeypatch.setattr(main, "require_x402_payment", lambda _headers, lane="basic": None)
    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json={"contract_address": "0x1111111111111111111111111111111111111111", "chain": "base"},
        headers={"PAYMENT-SIGNATURE": "demo"},
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "api_version",
        "decision",
        "risk_metrics",
        "signals",
        "attestation",
        "latency",
        "meta",
        "billing",
    }
    assert "nft_zora" in body["meta"]["security_signals"]


def test_zero_address_preserved_and_no_secrets(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    result = service.evaluate_contract("0x0000000000000000000000000000000000000000", "base")
    assert result["risk_metrics"]["score"] >= 95
    dumped = str(result)
    for marker in ["BASE_RPC_URL", "PRIVATE_KEY", "SECRET_KEY", "API_KEY"]:
        assert marker not in dumped
