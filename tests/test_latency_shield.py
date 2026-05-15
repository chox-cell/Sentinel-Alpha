from fastapi.testclient import TestClient

from apps.api import main


def test_background_tasks_scheduled_for_non_cache(monkeypatch):
    monkeypatch.setattr(main, "require_x402_payment", lambda _headers, lane="basic": None)
    monkeypatch.setattr(
        main,
        "evaluate_contract_with_meta",
        lambda **kwargs: {
            "response": {
                "api_version": "2026.8.0",
                "decision": {"action": "ALLOW", "emergency_signal": "NONE", "confidence": 0.6},
                "risk_metrics": {"score": 15, "threat_class": "normal"},
                "signals": {},
                "attestation": {},
                "latency": {"lane": "standard", "latency_ms": 1},
                "meta": {"ttl_seconds": 300, "trace_id": "trace"},
                "billing": {"amount": "0.02", "method": "x402", "status": "demo"},
            },
            "cache_hit": False,
            "outcome_record": {"trace_id": "trace", "action": "ALLOW"},
        },
    )

    captured: list[tuple[str, dict | None]] = []

    def fake_schedule(background_tasks, *, event_payload, outcome_record):
        captured.append(("log", event_payload))
        if outcome_record:
            captured.append(("outcome", outcome_record))

    monkeypatch.setattr(main, "schedule_post_risk_tasks", fake_schedule)

    client = TestClient(main.app)
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
    assert response.json()["api_version"] == "2026.8.0"
    assert len(captured) == 2


def test_cache_hit_does_not_schedule_outcome_record_task(monkeypatch):
    monkeypatch.setattr(main, "require_x402_payment", lambda _headers, lane="basic": None)
    monkeypatch.setattr(
        main,
        "evaluate_contract_with_meta",
        lambda **kwargs: {
            "response": {
                "api_version": "2026.8.0",
                "decision": {"action": "ALLOW", "emergency_signal": "NONE", "confidence": 0.6},
                "risk_metrics": {"score": 15, "threat_class": "normal"},
                "signals": {},
                "attestation": {},
                "latency": {"lane": "standard", "latency_ms": 1},
                "meta": {"ttl_seconds": 300, "trace_id": "cached-trace"},
                "billing": {"amount": "0.02", "method": "x402", "status": "demo"},
            },
            "cache_hit": True,
            "outcome_record": None,
        },
    )

    captured: list[tuple[str, dict | None]] = []

    def fake_schedule(background_tasks, *, event_payload, outcome_record):
        captured.append(("log", event_payload))
        if outcome_record:
            captured.append(("outcome", outcome_record))

    monkeypatch.setattr(main, "schedule_post_risk_tasks", fake_schedule)

    client = TestClient(main.app)
    client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
            "context": {"event_type": "new_deploy"},
        },
        headers={"PAYMENT-SIGNATURE": "demo"},
    )

    assert len(captured) == 1
