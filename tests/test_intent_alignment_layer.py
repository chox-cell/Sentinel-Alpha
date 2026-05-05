from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service


def test_no_intent_defaults_to_not_provided(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    result = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    ia = result["meta"]["security_signals"]["intent_alignment"]
    assert ia["intent_alignment_status"] in {"not_provided", "unknown"}
    assert ia["policy_recommendation"] == "unknown"


def test_swap_intent_unknown_asset_is_review_not_block(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    result = service.evaluate_contract(
        "0x1111111111111111111111111111111111111111",
        "base",
        context={"requested_action": "swap"},
    )
    ia = result["meta"]["security_signals"]["intent_alignment"]
    assert ia["policy_recommendation"] in {"review", "unknown"}
    assert ia["policy_recommendation"] != "block"


def test_approve_intent_unknown_contract_review(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    result = service.evaluate_contract(
        "0x1111111111111111111111111111111111111111",
        "base",
        context={"requested_action": "approve"},
    )
    ia = result["meta"]["security_signals"]["intent_alignment"]
    assert ia["policy_recommendation"] in {"review", "unknown"}


def test_unsupported_chain_conservative_review(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    result = service.evaluate_contract(
        "0x1111111111111111111111111111111111111111",
        "mysterychain",
        context={"requested_action": "transfer"},
    )
    ia = result["meta"]["security_signals"]["intent_alignment"]
    assert ia["policy_recommendation"] in {"review", "unknown"}


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
    assert "intent_alignment" in body["meta"]["security_signals"]


def test_no_forbidden_claims_or_secrets(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    result = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    dumped = str(result["meta"]["security_signals"]["intent_alignment"]).lower()
    assert "prompt-injection prevention" not in dumped
    assert "full intent verification" not in dumped
    for marker in ["base_rpc_url", "private_key", "secret_key", "api_key"]:
        assert marker not in dumped


def test_zero_address_high_risk_preserved(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    result = service.evaluate_contract("0x0000000000000000000000000000000000000000", "base")
    assert result["risk_metrics"]["score"] >= 95
