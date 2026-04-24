from services.risk_service import service


def test_risk_response_attestation_contains_identity_fields(monkeypatch):
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

    att = result["attestation"]
    assert att["attestation_version"] == "attestation-0.1"
    assert att["agent_identity"]["primary_endpoint"] == "/contracts/risk-score"
    assert att["signature"].startswith("sha256:")
