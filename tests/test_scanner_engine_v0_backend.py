from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service


def test_risk_score_required_fields_compatible(monkeypatch):
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
    assert "decision" in body
    assert "risk_metrics" in body
    assert "attestation" in body
    assert "signals" in body
    assert "score" in body["risk_metrics"]
    assert "confidence" in body["decision"]
    assert "action" in body["decision"]
    assert "emergency_signal" in body["decision"]


def test_invalid_address_handled_cleanly(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)

    result = service.evaluate_contract(contract_address="not-an-address", chain="base")
    assert "risk_metrics" in result
    assert "decision" in result
    assert result["signals"]["invalid_address"] == 1


def test_adapter_unavailable_fallback_mode(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")

    result = service.evaluate_contract(contract_address="0x1111111111111111111111111111111111111111", chain="base")
    assert result["meta"]["scanner_engine_version"] == "sentinel-scanner-v0"
    assert result["meta"]["fallback_mode"] is True


def test_response_contains_no_env_or_secret_markers(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)

    result = service.evaluate_contract(contract_address="0x1111111111111111111111111111111111111111", chain="base")
    dumped = str(result)
    forbidden = [
        "BASE_RPC_URL",
        "PRIVATE_KEY",
        "SECRET_KEY",
        "API_KEY",
    ]
    for marker in forbidden:
        assert marker not in dumped

