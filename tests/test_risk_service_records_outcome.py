from services.risk_service import service


def _build_cached_response():
    return {
        "api_version": "2026.8.0",
        "decision": {"action": "ALLOW", "emergency_signal": "NONE", "confidence": 0.6},
        "risk_metrics": {"score": 15, "threat_class": "normal"},
        "signals": {"new_deploy": 1},
        "attestation": {
            "decision_fingerprint": "sha256:test",
            "engine_version": "mycelium-wrsi-0.2",
            "signed_at": "2026-01-01T00:00:00+00:00",
        },
        "latency": {"lane": "standard", "latency_ms": 1},
        "meta": {"ttl_seconds": 300, "trace_id": "cached-trace"},
        "billing": {"amount": "0.02", "method": "x402", "status": "demo"},
    }


def test_evaluate_contract_records_outcome_on_non_cached(monkeypatch):
    calls = {"count": 0}

    def fake_record(record):
        calls["count"] += 1
        calls["record"] = record
        return record

    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setattr(service, "record_decision", fake_record)

    result = service.evaluate_contract(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"event_type": "new_deploy"},
    )

    assert calls["count"] == 1
    assert calls["record"]["trace_id"] == result["meta"]["trace_id"]
    assert calls["record"]["action"] == result["decision"]["action"]
    assert calls["record"]["score"] == result["risk_metrics"]["score"]


def test_evaluate_contract_does_not_record_on_cache_hit(monkeypatch):
    calls = {"count": 0}
    cached = _build_cached_response()

    monkeypatch.setattr(service, "get_cache", lambda _key: cached)
    monkeypatch.setattr(service, "record_decision", lambda _record: calls.__setitem__("count", calls["count"] + 1))

    result = service.evaluate_contract(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"event_type": "new_deploy"},
    )

    assert result == cached
    assert calls["count"] == 0
