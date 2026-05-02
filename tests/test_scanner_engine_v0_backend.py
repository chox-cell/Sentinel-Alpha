from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service
from services.scanner_engine.chain_read_adapter import get_contract_code


def test_risk_score_required_fields_compatible(monkeypatch):
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
    assert "decision" in body
    assert "risk_metrics" in body
    assert "attestation" in body
    assert "signals" in body
    assert "score" in body["risk_metrics"]
    assert "confidence" in body["decision"]
    assert "action" in body["decision"]
    assert "emergency_signal" in body["decision"]


def test_invalid_address_handled_cleanly(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)

    result = service.evaluate_contract(contract_address="not-an-address", chain="base")
    assert "risk_metrics" in result
    assert "decision" in result
    assert result["signals"]["invalid_address"] == 1


def test_adapter_unavailable_fallback_mode(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")

    result = service.evaluate_contract(contract_address="0x1111111111111111111111111111111111111111", chain="base")
    assert result["meta"]["scanner_engine_version"] == "sentinel-scanner-v0"
    assert result["meta"]["fallback_mode"] is True


def test_response_contains_no_env_or_secret_markers(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)

    result = service.evaluate_contract(contract_address="0x1111111111111111111111111111111111111111", chain="base")
    dumped = str(result)
    forbidden = [
        "BASE_RPC_URL",
        "PRIVATE_KEY",
        "SECRET_KEY",
        "API_KEY",
    ]
    for marker in forbidden:
        assert marker not in dumped


def test_zero_address_high_risk(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)

    result = service.evaluate_contract(
        contract_address="0x0000000000000000000000000000000000000000",
        chain="base",
    )
    assert result["risk_metrics"]["score"] >= 95
    assert result["risk_metrics"]["threat_class"] == "invalid_contract_address"
    assert result["signals"]["zero_address"] == 1
    cr = result["meta"]["chain_read"]
    assert cr["chain_read_status"] == "unavailable"
    assert cr["adapter_mode"] == "fallback"


def test_eoa_caps_confidence_when_rpc_configured(monkeypatch):
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

    result = service.evaluate_contract(
        contract_address="0x2222222222222222222222222222222222222222",
        chain="base",
    )
    assert result["signals"]["eoa_account"] == 1
    assert result["signals"]["contract_code_available"] == 0
    assert result["decision"]["confidence"] <= 0.48
    assert result["meta"]["chain_read"]["chain_read_status"] == "ok"
    assert "fixture.local.invalid" not in str(result)


def test_provider_rpc_error_unknown_and_fallback(monkeypatch):
    class _RpcErr:
        status_code = 200

        def json(self):
            return {"jsonrpc": "2.0", "id": 1, "error": {"code": -32603}}

    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setenv("BASE_RPC_URL", "http://fixture.local.invalid")
    monkeypatch.setenv("SENTINEL_CHAIN_READ_ENABLED", "true")
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")
    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        lambda *_a, **_k: _RpcErr(),
    )

    result = service.evaluate_contract(
        contract_address="0x3333333333333333333333333333333333333333",
        chain="base",
    )
    assert result["signals"]["unknown_account_kind"] == 1
    assert result["signals"]["chain_read_provider_unavailable"] == 1
    assert result["meta"]["chain_read"]["chain_read_status"] == "provider_error"
    assert result["meta"]["fallback_mode"] is True
    assert result["decision"]["confidence"] <= 0.48


def test_chain_read_fallback_false_when_contract_bytecode_readable(monkeypatch):
    class _RpcOkContract:
        status_code = 200

        def json(self):
            return {"jsonrpc": "2.0", "id": 1, "result": "0x6000"}

    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setenv("BASE_RPC_URL", "http://fixture.local.invalid")
    monkeypatch.setenv("SENTINEL_CHAIN_READ_ENABLED", "true")
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "true")
    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        lambda *_a, **_k: _RpcOkContract(),
    )

    result = service.evaluate_contract(
        contract_address="0x4444444444444444444444444444444444444444",
        chain="base",
    )
    assert result["signals"]["contract_code_available"] == 1
    assert result["signals"]["unknown_account_kind"] == 0
    assert result["meta"]["fallback_mode"] is False


def test_unsupported_chain_read_skips_live_rpc(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.setenv("BASE_RPC_URL", "http://fixture.local.invalid")
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")

    def _boom(*args, **kwargs):
        raise AssertionError("eth_getCode should not be invoked for unsupported chain")

    monkeypatch.setattr(
        "services.scanner_engine.chain_read_adapter.requests.post",
        _boom,
    )

    result = service.evaluate_contract(
        contract_address="0x5555555555555555555555555555555555555555",
        chain="monad",
    )
    assert result["meta"]["chain_read"]["chain_read_status"] == "unsupported_chain"
    assert result["meta"]["chain_read"]["adapter_mode"] == "fallback"
    assert result["meta"]["fallback_mode"] is True


def test_reads_disabled_skips_json_rpc(monkeypatch):
    monkeypatch.setenv("BASE_RPC_URL", "http://would-fail.local")
    monkeypatch.setenv("SENTINEL_CHAIN_READ_ENABLED", "false")

    def _boom(*_a, **_k):
        raise AssertionError("eth_getCode must not fire when reads are disabled")

    monkeypatch.setattr("services.scanner_engine.chain_read_adapter.requests.post", _boom)
    res = get_contract_code("0x1111111111111111111111111111111111111111", "base")
    assert res["status"] == "reads_disabled"


def test_risk_meta_includes_chain_read_block(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)
    monkeypatch.setenv("SENTINEL_WHATSABI_ENABLED", "false")

    result = service.evaluate_contract(
        contract_address="0x6666666666666666666666666666666666666666",
        chain="base",
    )
    cr = result["meta"]["chain_read"]
    assert set(cr.keys()) == {
        "chain_read_status",
        "account_type",
        "adapter_mode",
        "contract_code_available",
    }

