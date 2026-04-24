from fastapi.testclient import TestClient

from apps.api.main import app


def test_webhook_quicknode_accepts_nested_payload(monkeypatch):
    from services.scout_cell import hunter

    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)

    captured = {}

    def fake_evaluate(contract_address: str, chain: str, context: dict | None = None) -> dict:
        captured["contract_address"] = contract_address
        captured["chain"] = chain
        captured["context"] = context or {}
        return {
            "api_version": "2026.8.0",
            "decision": {"action": "ALLOW", "emergency_signal": "NONE", "confidence": 0.6},
            "risk_metrics": {"score": 15, "threat_class": "normal"},
            "signals": {},
            "attestation": {},
            "latency": {"lane": "standard", "latency_ms": 1},
            "meta": {"ttl_seconds": 300, "trace_id": "test-trace"},
            "billing": {"amount": "0.02", "method": "x402", "status": "demo"},
        }

    monkeypatch.setattr(hunter, "evaluate_contract", fake_evaluate)

    client = TestClient(app)
    response = client.post(
        "/webhooks/quicknode",
        json={
            "data": {
                "address": "0x1111111111111111111111111111111111111111",
                "chain": "BASE",
                "event_type": "first_liquidity",
                "bad_cluster": True,
            }
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "ok"
    assert body["result"]["status"] == "ok"
    assert body["result"]["candidates"] == 1
    assert body["result"]["results"][0]["status_code"] == 200
    assert set(body["result"]["results"][0]["body"].keys()) == {
        "api_version",
        "decision",
        "risk_metrics",
        "signals",
        "attestation",
        "latency",
        "meta",
        "billing",
    }

    assert captured["contract_address"] == "0x1111111111111111111111111111111111111111"
    assert captured["chain"] == "base"
    assert captured["context"]["event_type"] == "first_liquidity"
    assert captured["context"]["bad_cluster"] is True


def test_webhook_quicknode_ignores_missing_contract(monkeypatch):
    monkeypatch.delenv("QUICKNODE_WEBHOOK_SECRET", raising=False)

    client = TestClient(app)
    response = client.post(
        "/webhooks/quicknode",
        json={"event": {"chain": "base", "event_type": "new_deploy"}},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["result"]["status"] == "ok"
    assert body["result"]["candidates"] == 0
