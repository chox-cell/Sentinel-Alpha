from fastapi.testclient import TestClient

from apps.api import main as api_main
from apps.api.main import app


def _payload() -> dict:
    return {
        "contract_address": "0x1111111111111111111111111111111111111111",
        "chain": "base",
        "context": {},
    }


def test_rate_limit_disabled_by_default_no_429(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "demo")
    monkeypatch.setenv("PAYMENT_DEMO_SIGNATURE", "demo")
    monkeypatch.delenv("RATE_LIMIT_ENABLED", raising=False)
    monkeypatch.delenv("RATE_LIMIT_PER_MINUTE", raising=False)
    api_main._RATE_LIMIT_BUCKETS.clear()

    client = TestClient(app)
    r1 = client.post("/contracts/risk-score", json=_payload(), headers={"PAYMENT-SIGNATURE": "demo"})
    r2 = client.post("/contracts/risk-score", json=_payload(), headers={"PAYMENT-SIGNATURE": "demo"})
    assert r1.status_code == 200
    assert r2.status_code == 200


def test_rate_limit_enabled_blocks_after_threshold(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "demo")
    monkeypatch.setenv("PAYMENT_DEMO_SIGNATURE", "demo")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "true")
    monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "1")
    api_main._RATE_LIMIT_BUCKETS.clear()

    client = TestClient(app)
    r1 = client.post("/contracts/risk-score", json=_payload(), headers={"PAYMENT-SIGNATURE": "demo"})
    r2 = client.post("/contracts/risk-score", json=_payload(), headers={"PAYMENT-SIGNATURE": "demo"})

    assert r1.status_code == 200
    assert r2.status_code == 429
    assert r2.json()["detail"]["error"] == "rate_limit_exceeded"
