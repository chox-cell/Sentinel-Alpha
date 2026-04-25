import json

from services.identity import erc8004_adapter


def test_get_erc8004_status_default_planned(monkeypatch):
    monkeypatch.delenv("ERC8004_ENABLED", raising=False)
    monkeypatch.delenv("ERC8004_REGISTRY_ADDRESS", raising=False)
    monkeypatch.delenv("ERC8004_AGENT_ID", raising=False)
    st = erc8004_adapter.get_erc8004_status()
    assert st == {
        "enabled": False,
        "registry_configured": False,
        "agent_id_configured": False,
        "status": "planned",
    }


def test_get_erc8004_status_configured_not_registered_partial(monkeypatch):
    monkeypatch.setenv("ERC8004_ENABLED", "true")
    monkeypatch.setenv("ERC8004_REGISTRY_ADDRESS", "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    monkeypatch.delenv("ERC8004_AGENT_ID", raising=False)
    st = erc8004_adapter.get_erc8004_status()
    assert st["enabled"] is True
    assert st["registry_configured"] is True
    assert st["agent_id_configured"] is False
    assert st["status"] == "configured_not_registered"


def test_get_erc8004_status_registered_unverified_when_both_set(monkeypatch):
    monkeypatch.setenv("ERC8004_ENABLED", "true")
    monkeypatch.setenv("ERC8004_REGISTRY_ADDRESS", "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    monkeypatch.setenv("ERC8004_AGENT_ID", "42")
    st = erc8004_adapter.get_erc8004_status()
    assert st["status"] == "registered_unverified"
    assert st["registry_configured"] is True
    assert st["agent_id_configured"] is True


def test_build_agent_identity_payload_no_secret_values(monkeypatch):
    secret = "https://registry.example/secret-token-path"
    monkeypatch.setenv("ERC8004_ENABLED", "true")
    monkeypatch.setenv("ERC8004_REGISTRY_ADDRESS", secret)
    monkeypatch.setenv("ERC8004_AGENT_ID", "agent-1")
    payload = erc8004_adapter.build_agent_identity_payload()
    dumped = json.dumps(payload)
    assert secret not in dumped
    assert payload["erc8004_adapter"]["chain_verification"] == "stub_offline"
    assert payload["agent_name"] == "Sentinel Alpha"
    assert payload["did"] == "did:sentinel-alpha:local" or payload["did"].startswith("did:")


def test_build_agent_identity_payload_uses_sentinel_did(monkeypatch):
    monkeypatch.setenv("SENTINEL_AGENT_DID", "did:sentinel-alpha:local")
    monkeypatch.delenv("ERC8004_ENABLED", raising=False)
    payload = erc8004_adapter.build_agent_identity_payload()
    assert payload["did"] == "did:sentinel-alpha:local"
