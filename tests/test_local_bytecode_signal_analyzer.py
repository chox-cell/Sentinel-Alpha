from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service
from services.scanner_engine.local_bytecode_analyzer import analyze_bytecode_signals


def test_unavailable_bytecode_returns_unavailable():
    out = analyze_bytecode_signals(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
        bytecode=None,
        chain_read_result={"chain_read_status": "ok", "account_type": "contract", "contract_code_available": True},
    )
    assert out["bytecode_analysis_status"] == "unavailable"
    assert out["bytecode_available"] is False


def test_invalid_hex_returns_invalid():
    out = analyze_bytecode_signals(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
        bytecode="0xzz11",
        chain_read_result={"chain_read_status": "ok", "account_type": "contract", "contract_code_available": True},
    )
    assert out["bytecode_analysis_status"] == "invalid"


def test_simple_bytecode_analyzed_and_selectors_extracted():
    out = analyze_bytecode_signals(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
        bytecode="0x600063a9059cbb6000f3",
        chain_read_result={"chain_read_status": "ok", "account_type": "contract", "contract_code_available": True},
    )
    assert out["bytecode_analysis_status"] == "analyzed"
    assert "0xa9059cbb" in out["selector_candidates"]


def test_opcode_detection_delegatecall_selfdestruct_external_call():
    out = analyze_bytecode_signals(
        address="0x1111111111111111111111111111111111111111",
        chain="base",
        bytecode="0x6000f16000f46000ff",
        chain_read_result={"chain_read_status": "ok", "account_type": "contract", "contract_code_available": True},
    )
    assert out["external_call_present"] is True
    assert out["delegatecall_present"] is True
    assert out["selfdestruct_present"] is True


def test_additive_metadata_appears_in_risk_score_response(monkeypatch):
    from apps.api import main

    monkeypatch.setattr(main, "require_x402_payment", lambda _headers, lane="basic": None)
    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
            "context": {"bytecode": "0x600063a9059cbb6000f3"},
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
    assert "bytecode" in body["meta"]["security_signals"]
    assert body["meta"]["security_signals"]["bytecode"]["bytecode_analysis_status"] == "analyzed"


def test_no_malicious_certainty_or_honeypot_claim_and_no_secrets(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    result = service.evaluate_contract(
        "0x1111111111111111111111111111111111111111",
        "base",
        context={"bytecode": "0x6000f46000ff"},
    )
    text = str(result["meta"]["security_signals"]["bytecode"]).lower()
    assert "malicious certainty" not in text
    assert "honeypot detected" not in text
    dumped = str(result).lower()
    for marker in ["base_rpc_url", "private_key", "secret_key", "api_key"]:
        assert marker not in dumped
