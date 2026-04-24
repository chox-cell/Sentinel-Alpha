from apps.api import main


class _FakeBackgroundTasks:
    def __init__(self):
        self.calls = []

    def add_task(self, func, *args, **kwargs):
        self.calls.append((func, args, kwargs))


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

    tasks = _FakeBackgroundTasks()
    req = main.RequestModel(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"event_type": "new_deploy"},
    )
    response = main.risk_score(req=req, background_tasks=tasks, payment_signature="demo")

    assert response["api_version"] == "2026.8.0"
    assert len(tasks.calls) == 2


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

    tasks = _FakeBackgroundTasks()
    req = main.RequestModel(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"event_type": "new_deploy"},
    )
    main.risk_score(req=req, background_tasks=tasks, payment_signature="demo")

    # log_event task is still expected, but no outcome recording task.
    assert len(tasks.calls) == 1
