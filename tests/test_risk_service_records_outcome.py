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
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)

    result = service.evaluate_contract_with_meta(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"event_type": "new_deploy"},
    )

    assert result["cache_hit"] is False
    assert result["outcome_record"]["trace_id"] == result["response"]["meta"]["trace_id"]
    assert result["outcome_record"]["action"] == result["response"]["decision"]["action"]
    assert result["outcome_record"]["score"] == result["response"]["risk_metrics"]["score"]


def test_evaluate_contract_does_not_record_on_cache_hit(monkeypatch):
    cached = _build_cached_response()

    monkeypatch.setattr(service, "get_cache", lambda _key: cached)

    result = service.evaluate_contract_with_meta(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"event_type": "new_deploy"},
    )

    assert result["response"] == cached
    assert result["cache_hit"] is True
    assert result["outcome_record"] is None
