from services.risk_service import service


def test_risk_response_uses_hmac_signature_with_private_key(monkeypatch):
    monkeypatch.setenv("SENTINEL_ATTESTATION_PRIVATE_KEY", "secret")
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)

    result = service.evaluate_contract(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"event_type": "new_deploy"},
    )

    att = result["attestation"]
    assert att["signing_mode"] == "real_key"
    assert att["signature"].startswith("hmac-sha256:")
