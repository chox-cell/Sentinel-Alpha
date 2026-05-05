from fastapi.testclient import TestClient

from apps.api.main import app
from services.risk_service import service
from services.scanner_engine.erc20_heuristics import analyze_erc20_risk


def test_eoa_is_not_applicable(monkeypatch):
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
    erc20 = result["meta"]["security_signals"]["erc20"]
    assert erc20["erc20_analysis_status"] == "not_applicable"
    assert erc20["erc20_candidate"] is False


def test_generic_contract_without_abi_stays_unknown(monkeypatch):
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
    erc20 = result["meta"]["security_signals"]["erc20"]
    assert erc20["erc20_analysis_status"] in {"unknown", "unavailable"}
    assert erc20["transfer_tax_possible"] == "unknown"
    assert erc20["blacklist_possible"] == "unknown"
    assert erc20["mint_possible"] == "unknown"
    assert erc20["owner_can_change_fees"] == "unknown"


def test_abi_hints_set_possible_flags_conservatively():
    out = analyze_erc20_risk(
        "0x1111111111111111111111111111111111111111",
        "base",
        asset_result={"asset_type": "erc20_candidate"},
        source_proxy_admin_result={"abi_available": True},
        chain_read_result={"chain_read_status": "ok"},
        abi_result={
            "available": True,
            "functions": ["pause", "blacklist", "mint", "setTaxFee"],
            "selectors": ["0x8456cb59"],
        },
    )
    assert out["erc20_analysis_status"] == "analyzed"
    assert out["pause_possible"] is True
    assert out["blacklist_possible"] is True
    assert out["mint_possible"] is True
    assert out["transfer_tax_possible"] is True


def test_honeypot_simulation_unavailable_and_no_detection_claim(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)

    result = service.evaluate_contract("0x1111111111111111111111111111111111111111", "base")
    erc20 = result["meta"]["security_signals"]["erc20"]
    assert erc20["honeypot_simulation_available"] is False
    assert "honeypot detected" not in " ".join(erc20["notes"]).lower()


def test_additive_metadata_and_top_level_schema_unchanged(monkeypatch):
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
    assert "erc20" in body["meta"]["security_signals"]


def test_no_false_absent_without_abi_and_zero_address_preserved_no_secrets(monkeypatch):
    monkeypatch.setattr(service, "get_cache", lambda _key: None)
    monkeypatch.setattr(service, "set_cache", lambda _key, _value, ttl=300: None)
    monkeypatch.delenv("BASE_RPC_URL", raising=False)

    result = service.evaluate_contract("0x0000000000000000000000000000000000000000", "base")
    dumped = str(result)
    for marker in ["BASE_RPC_URL", "PRIVATE_KEY", "SECRET_KEY", "API_KEY"]:
        assert marker not in dumped
    assert result["risk_metrics"]["score"] >= 95
    erc20 = result["meta"]["security_signals"]["erc20"]
    assert erc20["honeypot_simulation_available"] is False
    assert erc20["erc20_analysis_status"] in {"unavailable", "unknown"}
