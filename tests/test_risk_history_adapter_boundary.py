import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_history.adapter import build_scan_record, get_risk_history_status, persist_scan_result
from services.risk_service import service


def test_default_status_is_disabled_or_not_configured():
    status = get_risk_history_status()
    assert status["persistence_enabled"] is False
    assert status["persistence_mode"] in {"disabled", "not_configured"}
    assert status["database_url_required"] is False
    assert status["write_attempted"] is False
    assert status["write_status"] == "not_run"
    assert status["error_type"] is None


def test_no_database_url_required_by_default():
    status = get_risk_history_status(config={"enabled": False})
    assert status["database_url_required"] is False
    notes = " ".join(status["notes"]).lower()
    assert "no database_url is required" in notes


def test_persist_scan_result_does_not_write_by_default():
    out = persist_scan_result({"request_id": "abc"})
    assert out["write_attempted"] is False
    assert out["write_status"] == "not_run"
    assert out["record_id"] is None


def test_build_scan_record_sanitized_and_no_raw_headers_or_secrets():
    response = {
        "decision": {"action": "ALLOW", "confidence": 0.7},
        "risk_metrics": {"score": 12},
        "meta": {"trace_id": "trace-1", "security_signals": {"erc20": {"erc20_candidate": True}}},
        "attestation": {"attestation_id": "att-1"},
    }
    record = build_scan_record(
        response,
        request_meta={
            "request_id": "req-1",
            "chain": "base",
            "contract_address": "0x1111111111111111111111111111111111111111",
            "headers": {"authorization": "secret-token"},
        },
    )
    assert record["request_id"] == "req-1"
    assert record["chain"] == "base"
    assert record["contract_address_hash"] != "0x1111111111111111111111111111111111111111"
    dumped = str(record).lower()
    for marker in ["private_key", "authorization", "secret-token"]:
        assert marker not in dumped


def test_top_level_response_fields_preserved_if_service_untouched(monkeypatch):
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


def test_env_unchanged_during_adapter_tests(monkeypatch):
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    _ = service.evaluate_contract("0x2222222222222222222222222222222222222222", "base")
    _ = get_risk_history_status()
    _ = persist_scan_result({"request_id": "x"})
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
