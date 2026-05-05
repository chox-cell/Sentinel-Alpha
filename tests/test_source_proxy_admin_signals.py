from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service


def test_source_proxy_admin_unknown_when_unavailable(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")

    result = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    spa = result["meta"]["security_signals"]["source_proxy_admin"]
    assert spa["verified_source_status"] == "unavailable"
    assert spa["abi_available"] == "unknown"
    assert spa["proxy_detected"] == "unknown"
    assert spa["owner_admin_permissions"] == "unknown"


def test_eoa_handled_safely_without_false_absent_claims(monkeypatch):
    class _RpcOkEoa:
        status_code = 200

        def json(self):
            return {"jsonrpc": "2.0", "id": 1, "result": "0x"}

    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setenv("BASE_RPC_URL", "http://fixture.local.invalid")
    monkeypatch.setenv("SENTINEL_CHAIN_READ_ENABLED", "true")
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")
    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        lambda *_a, **_k: _RpcOkEoa(),
    )

    result = service.evaluate_contract("0x2222222222222222222222222222222222222222", "base")
    spa = result["meta"]["security_signals"]["source_proxy_admin"]
    assert result["meta"]["asset"]["asset_type"] == "eoa"
    assert spa["owner_admin_permissions"] == "unknown"
    assert spa["proxy_detected"] == "unknown"
    assert spa["owner_admin_permissions"] != "absent"


def test_generic_contract_unknown_proxy_admin_without_abi(monkeypatch):
    class _RpcOkContract:
        status_code = 200

        def json(self):
            return {"jsonrpc": "2.0", "id": 1, "result": "0x60006000"}

    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setenv("BASE_RPC_URL", "http://fixture.local.invalid")
    monkeypatch.setenv("SENTINEL_CHAIN_READ_ENABLED", "true")
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")
    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        lambda *_a, **_k: _RpcOkContract(),
    )

    result = service.evaluate_contract("0x4444444444444444444444444444444444444444", "base")
    spa = result["meta"]["security_signals"]["source_proxy_admin"]
    assert result["meta"]["asset"]["asset_type"] == "generic_contract"
    assert spa["proxy_detected"] == "unknown"
    assert spa["owner_admin_permissions"] == "unknown"


def test_additive_metadata_and_top_level_compat(monkeypatch):
    from apps.api import main

    monkeypatch.setattr(main, "require_x402_payment", lambda _headers, lane="basic": None)
    client = TestClient(app)
    response = client.post(
        "/contracts/risk-score",
        json={
            "contract_address": "0x1111111111111111111111111111111111111111",
            "chain": "base",
        },
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
    assert "security_signals" in body["meta"]
    assert "source_proxy_admin" in body["meta"]["security_signals"]


def test_no_secrets_in_response_and_zero_address_high_risk_preserved(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)

    result = service.evaluate_contract("0x0000000000000000000000000000000000000000", "base")
    dumped = str(result)
    for marker in ["BASE_RPC_URL", "PRIVATE_KEY", "SECRET_KEY", "API_KEY"]:
        assert marker not in dumped
    assert result["risk_metrics"]["score"] >= 95
    spa = result["meta"]["security_signals"]["source_proxy_admin"]
    assert spa["verified_source_status"] == "unavailable"
