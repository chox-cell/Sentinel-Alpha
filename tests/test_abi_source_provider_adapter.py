from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service
from services.scanner_engine.abi_source_adapter import analyze_abi_source_status


def test_default_provider_not_configured_safe_fallback():
    out = analyze_abi_source_status(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
    )
    assert out["source_provider_status"] in {"not_configured", "disabled"}
    assert out["verified_source_status"] in {"unknown", "unavailable"}
    assert out["abi_available"] == "unknown"
    assert out["abi_function_names"] == []
    assert out["abi_selector_count"] == 0
    assert out["fallback_mode"] is True
    assert "not configured by default" in " ".join(out["notes"]).lower()


def test_local_fixture_abi_returns_available_and_verified():
    out = analyze_abi_source_status(
        address="0x2222222222222222222222222222222222222222",
        chain="base",
        provider_context={
            "provider_name": "local_fixture",
            "verified_source_status": "verified",
            "abi": [
                {"type": "function", "name": "transfer"},
                {"type": "function", "name": "approve"},
                {"type": "event", "name": "Transfer"},
            ],
        },
    )
    assert out["provider_name"] == "local_fixture"
    assert out["source_provider_status"] == "available"
    assert out["verified_source_status"] == "verified"
    assert out["abi_available"] is True
    assert out["abi_selector_count"] == 2
    assert out["abi_function_names"] == ["transfer", "approve"]


def test_unknown_chain_fallback():
    out = analyze_abi_source_status(
        address="0x3333333333333333333333333333333333333333",
        chain="unknown_chain",
    )
    assert out["fallback_mode"] is True
    assert out["source_fetch_error_type"] == "unsupported_chain"
    assert out["verified_source_status"] in {"unknown", "unavailable"}


def test_additive_metadata_in_api_and_top_level_fields_preserved(monkeypatch):
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
    abi_source = body["meta"]["security_signals"]["abi_source"]
    assert abi_source["source_provider_status"] in {"not_configured", "disabled"}
    assert abi_source["verified_source_status"] in {"unknown", "unavailable"}


def test_no_secrets_and_no_overclaims_by_default(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    result = service.evaluate_contract("0x4444444444444444444444444444444444444444", "base")
    text = str(result["meta"]["security_signals"]["abi_source"]).lower()
    assert "full abi coverage is live" not in text
    assert "verified source lookup is live" not in text
    dumped = str(result).lower()
    for marker in ["api_key", "secret_key", "private_key", "token", "password"]:
        assert marker not in dumped


def test_no_external_network_required_for_local_fixture_path(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("unexpected external call")),
    )
    result = service.evaluate_contract(
        "0x5555555555555555555555555555555555555555",
        "base",
        context={
            "provider_context": {
                "provider_name": "local_fixture",
                "verified_source_status": "verified",
                "abi": [
                    {"type": "function", "name": "transfer"},
                    {"type": "function", "name": "balanceOf"},
                ],
            }
        },
    )
    abi_source = result["meta"]["security_signals"]["abi_source"]
    assert abi_source["provider_name"] == "local_fixture"
    assert abi_source["abi_available"] is True
    assert "transfer" in abi_source["abi_function_names"]
