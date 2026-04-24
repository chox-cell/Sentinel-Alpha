from fastapi.testclient import TestClient

from apps.api.main import app


def test_risk_score_schema_unchanged_after_latency_shield(monkeypatch):
    from apps.api import main

    monkeypatch.setattr(main, "require_x402_payment", lambda _headers, lane="basic": None)

    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
            "context": {"event_type": "new_deploy"},
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
