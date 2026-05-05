from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service


def test_eoa_classification(monkeypatch):
    class _RpcOkEoa:
        status_code = 200

        def json(self):
            return {"jsonrpc": "2.0", "id": 1, "result": "0x"}

    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setenv("BASE_RPC_URL", "http://fixture.local.invalid")
    monkeypatch.setenv("SENTINEL_CHAIN_READ_ENABLED", "true")
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "true")
    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        lambda *_a, **_k: _RpcOkEoa(),
    )

    result = service.evaluate_contract("0x2222222222222222222222222222222222222222", "base")
    asset = result["meta"]["asset"]
    assert asset["asset_type"] == "eoa"
    assert asset["fallback_mode"] is False
    assert asset["unsupported_asset_type"] is False
    assert "account_type:eoa" in asset["classification_basis"]


def test_generic_contract_classification_when_bytecode_exists(monkeypatch):
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
    asset = result["meta"]["asset"]
    assert asset["asset_type"] == "generic_contract"
    assert asset["fallback_mode"] is False
    assert asset["unsupported_asset_type"] is False
    assert asset["asset_confidence"] <= 0.7


def test_unknown_provider_fallback_classification(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")

    result = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    asset = result["meta"]["asset"]
    assert asset["asset_type"] == "unknown"
    assert asset["fallback_mode"] is True
    assert asset["unsupported_asset_type"] is False


def test_zero_address_high_risk_preserved(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)

    result = service.evaluate_contract("0x0000000000000000000000000000000000000000", "base")
    assert result["risk_metrics"]["score"] >= 95
    assert result["signals"]["zero_address"] == 1
    assert result["meta"]["asset"]["asset_type"] == "unknown"
    assert "zero_address" in result["meta"]["asset"]["classification_basis"]


def test_risk_score_response_fields_are_backward_compatible(monkeypatch):
    from apps.api import main

    monkeypatch.setattr(main, "require_x402_payment", lambda _headers, lane="basic": None)
    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
        },
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
    assert "asset" in body["meta"]


def test_no_secrets_and_candidate_wording_is_conservative(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)

    result = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    dumped = str(result)
    for marker in ["BASE_RPC_URL", "PRIVATE_KEY", "SECRET_KEY", "API_KEY"]:
        assert marker not in dumped
    asset_type = result["meta"]["asset"]["asset_type"]
    allowed = {
        "eoa",
        "generic_contract",
        "erc20_candidate",
        "erc721_candidate",
        "erc1155_candidate",
        "proxy_candidate",
        "router_candidate",
        "pool_candidate",
        "vault_candidate",
        "unknown",
    }
    assert asset_type in allowed
