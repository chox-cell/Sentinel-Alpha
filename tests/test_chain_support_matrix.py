from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service
from services.scanner_engine.chain_support import get_chain_support


def test_base_primary_support():
    info = get_chain_support("base")
    assert info["support_status"] == "primary"
    assert info["network_family"] == "evm"
    assert info["paid_rpc_required"] is False


def test_ethereum_not_full_primary():
    info = get_chain_support("ethereum")
    assert info["support_status"] in {"partial", "roadmap"}
    assert info["risk_engine_support"] != "full_v5_primary"


def test_zora_not_full_support():
    info = get_chain_support("zora")
    assert info["support_status"] in {"roadmap", "partial"}
    assert info["risk_engine_support"] != "full_v5_primary"


def test_unknown_chain_fallback():
    info = get_chain_support("mysterychain")
    assert info["support_status"] in {"unsupported", "unknown"}
    assert info["network_family"] == "unknown"


def test_additive_metadata_and_top_level_schema(monkeypatch):
    from apps.api import main

    monkeypatch.setattr(main, "require_x402_payment", lambda _headers, lane="basic": None)
    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json={"contract_address": "0x1111111111111111111111111111111111111111", "chain": "base"},
        headers={"PAYMENT-SIGNATURE": "demo"},
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "api_version",
        "decision",
        "risk_metrics",
        "signals",
        "attestation",
        "latency",
        "meta",
        "billing",
    }
    assert "chain_support" in body["meta"]
    assert body["meta"]["chain_support"]["paid_rpc_required"] is False


def test_no_secrets_in_response(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    result = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    dumped = str(result).lower()
    for marker in ["base_rpc_url", "private_key", "secret_key", "api_key"]:
        assert marker not in dumped


def test_chain_support_doc_safe_wording():
    text = open("docs/16_launch/SENTINEL_CHAIN_SUPPORT_MATRIX.md", "r", encoding="utf-8").read().lower()
    assert "base is primary" in text
    assert "paid rpc/provider dependencies are not enabled by default" in text
    assert "no full zora support claim" in text
    assert "no full multi-chain support claim" in text
    assert "full multi-chain support" not in text.replace("no full multi-chain support claim", "")
