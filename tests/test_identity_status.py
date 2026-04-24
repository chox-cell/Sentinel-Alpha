from services.identity.identity_config import get_identity_status


def test_identity_status_defaults(monkeypatch):
    monkeypatch.delenv("SENTINEL_IDENTITY_MODE", raising=False)
    monkeypatch.delenv("SENTINEL_AGENT_DID", raising=False)
    monkeypatch.delenv("SENTINEL_ERC8004_CONTRACT_ADDRESS", raising=False)
    monkeypatch.delenv("SENTINEL_ATTESTATION_PUBLIC_KEY", raising=False)

    status = get_identity_status()
    assert status["identity_mode"] == "local_stub"
    assert status["did"] == "did:sentinel-alpha:local"
    assert status["agent_name"] == "Sentinel Alpha"
    assert status["engine_name"] == "Mycelium Engine"
    assert status["attestation_version"] == "attestation-0.1"
    assert status["erc8004_enabled"] is False
    assert status["real_key_enabled"] is False


def test_identity_status_modes(monkeypatch):
    monkeypatch.setenv("SENTINEL_IDENTITY_MODE", "erc8004")
    monkeypatch.setenv("SENTINEL_ERC8004_CONTRACT_ADDRESS", "0x1111111111111111111111111111111111111111")
    monkeypatch.delenv("SENTINEL_ATTESTATION_PUBLIC_KEY", raising=False)
    status = get_identity_status()
    assert status["erc8004_enabled"] is True
    assert status["real_key_enabled"] is False
