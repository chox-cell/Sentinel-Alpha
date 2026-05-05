from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service


def test_provider_unavailable_has_fallback_explanation(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    result = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    exp = result["meta"]["security_explanation"]
    assert exp["fallback_reason"] is not None
    assert "provider unavailable" in " ".join(exp["explanation"]).lower()


def test_simulation_not_configured_explains_honeypot_unknown(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    res = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    exp = res["meta"]["security_explanation"]
    text = " ".join(exp["explanation"]).lower()
    assert "simulation is not configured" in text
    assert "honeypot status remains unknown" in text


def test_eoa_explains_contract_not_applicable(monkeypatch):
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
    res = service.evaluate_contract("0x2222222222222222222222222222222222222222", "base")
    text = " ".join(res["meta"]["security_explanation"]["explanation"]).lower()
    assert "target is an eoa" in text


def test_generic_contract_without_abi_explains_uncertainty(monkeypatch):
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
    res = service.evaluate_contract("0x4444444444444444444444444444444444444444", "base")
    combined = " ".join(res["meta"]["security_explanation"]["explanation"]).lower()
    assert "abi/source context is unavailable" in combined


def test_zero_address_explanation_present(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    res = service.evaluate_contract("0x0000000000000000000000000000000000000000", "base")
    text = " ".join(res["meta"]["security_explanation"]["explanation"]).lower()
    assert "zero address detected" in text
    assert res["risk_metrics"]["score"] >= 95


def test_additive_metadata_and_top_level_schema_preserved(monkeypatch):
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
    assert "security_explanation" in body["meta"]


def test_no_secrets_or_forbidden_claims_in_explanation(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    res = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    dumped = str(res["meta"]["security_explanation"]).lower()
    for marker in ["base_rpc_url", "private_key", "secret_key", "api_key"]:
        assert marker not in dumped
    assert "honeypot detected" not in dumped
    assert "guaranteed protection" not in dumped
    assert "mev prevention" not in dumped
    assert "automatic x402 settlement" not in dumped
