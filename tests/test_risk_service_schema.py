from services.risk_service import service


def test_evaluate_contract_preserves_real_signals_v0_schema(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)

    result = service.evaluate_contract(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"event_type": "new_deploy"},
    )

    assert set(result.keys()) == {
        "api_version",
        "decision",
        "risk_metrics",
        "signals",
        "attestation",
        "latency",
        "meta",
        "billing",
    }

    assert set(result["decision"].keys()) == {"action", "emergency_signal", "confidence"}
    assert set(result["risk_metrics"].keys()) == {"score", "threat_class"}
