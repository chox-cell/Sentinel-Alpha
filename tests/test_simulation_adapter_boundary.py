from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service


def test_default_simulation_unavailable(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    result = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    sim = result["meta"]["security_signals"]["simulation"]
    assert sim["simulation_available"] is False
    assert sim["simulation_mode"] in {"disabled", "not_configured"}
    assert sim["buy_simulation_status"] in {"not_run", "unavailable"}
    assert sim["sell_simulation_status"] in {"not_run", "unavailable"}
    assert sim["call_simulation_status"] in {"not_run", "unavailable"}


def test_honeypot_unknown_by_default_no_confirmation(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    res = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    sim = res["meta"]["security_signals"]["simulation"]
    assert sim["honeypot_risk"] == "unknown"
    assert sim["honeypot_risk"] != "confirmed"
    notes = " ".join(sim["notes"]).lower()
    assert "not configured/live" in notes


def test_no_paid_provider_call_or_external_dependency(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    # If requests.post gets called unexpectedly in this path, fail hard.
    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("unexpected external call")),
    )
    # Keep reads disabled so simulation remains boundary-only and does not force external call path.
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    res = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    sim = res["meta"]["security_signals"]["simulation"]
    assert sim["simulation_available"] is False


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
    assert "simulation" in body["meta"]["security_signals"]


def test_zero_address_high_risk_preserved_and_no_secrets(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    result = service.evaluate_contract("0x0000000000000000000000000000000000000000", "base")
    assert result["risk_metrics"]["score"] >= 95
    dumped = str(result)
    for marker in ["BASE_RPC_URL", "PRIVATE_KEY", "SECRET_KEY", "API_KEY"]:
        assert marker not in dumped
    sim = result["meta"]["security_signals"]["simulation"]
    assert sim["simulation_available"] is False
    assert sim["honeypot_risk"] == "unknown"
