from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service


def test_default_mempool_unavailable(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    result = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    mm = result["meta"]["security_signals"]["mempool_mev"]
    assert mm["mempool_signal_available"] is False
    assert mm["mempool_mode"] in {"disabled", "not_configured"}
    assert mm["pending_activity_status"] == "unavailable"


def test_mev_and_front_run_unknown_by_default(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    res = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    mm = res["meta"]["security_signals"]["mempool_mev"]
    assert mm["mev_risk"] == "unknown"
    assert mm["front_run_observed"] == "unknown"
    notes = " ".join(mm["notes"]).lower()
    assert "not configured/live" in notes


def test_no_mev_or_front_run_prevention_claim(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    res = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    text = str(res["meta"]["security_signals"]["mempool_mev"]).lower()
    assert "mev prevention" not in text
    assert "front-run prevention" not in text


def test_no_paid_provider_call_or_external_dependency(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("unexpected external call")),
    )
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    res = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    assert res["meta"]["security_signals"]["mempool_mev"]["mempool_signal_available"] is False


def test_additive_metadata_and_top_level_schema(monkeypatch):
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
    assert "mempool_mev" in body["meta"]["security_signals"]


def test_unsupported_chain_conservative(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    res = service.evaluate_contract("0x1111111111111111111111111111111111111111", "mysterychain")
    mm = res["meta"]["security_signals"]["mempool_mev"]
    assert mm["mempool_signal_available"] is False
    assert mm["mev_risk"] == "unknown"


def test_no_secrets_in_response(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    res = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    dumped = str(res).lower()
    for marker in ["base_rpc_url", "private_key", "secret_key", "api_key"]:
        assert marker not in dumped
