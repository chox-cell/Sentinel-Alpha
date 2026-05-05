from scripts import print_real_payment_readiness as readiness


def test_real_payment_readiness_script_outputs_required_fields(monkeypatch):
    fixture_env = {
        "PAYMENT_MODE": "real",
        "X402_ENABLED": "true",
        "X402_ONCHAIN_VERIFY": "false",
        "BASE_RPC_URL": "https://secret-rpc.example",
        "X402_REVENUE_ADDRESS": "0x1111111111111111111111111111111111111111",
        "SENTINEL_TREASURY_WALLET": "0x2222222222222222222222222222222222222222",
        "PRICE_BASIC": "0.02",
        "PRICE_EXECUTIVE": "0.05",
        "PRICE_PREMIUM": "0.10",
        "PRICE_PRIORITY": "0.15",
    }
    monkeypatch.setattr(readiness, "_effective_env", lambda: dict(fixture_env))

    body = readiness.build_readiness_report()
    assert set(body.keys()) == {
        "env_source",
        "payment_mode",
        "x402_enabled",
        "onchain_verify_enabled",
        "base_rpc_configured",
        "treasury_configured",
        "wallet_address_configured",
        "pricing_tiers",
        "readiness_verdict",
    }
    assert body["env_source"] == ".env"
    assert body["payment_mode"] == "real"
    assert body["x402_enabled"] is True
    assert body["onchain_verify_enabled"] is False
    assert body["base_rpc_configured"] is True
    assert body["treasury_configured"] is True
    assert body["wallet_address_configured"] is True
    assert body["readiness_verdict"] == "not_ready"


def test_real_payment_readiness_wallet_vs_treasury_flags(monkeypatch):
    fixture_env = {
        "PAYMENT_MODE": "demo",
        "X402_ENABLED": "false",
        "X402_ONCHAIN_VERIFY": "false",
        "BASE_RPC_URL": "",
        "X402_REVENUE_ADDRESS": "",
        "SENTINEL_TREASURY_WALLET": "",
        "AGENT_WALLET_ADDRESS": "0x3333333333333333333333333333333333333333",
    }
    monkeypatch.setattr(readiness, "_effective_env", lambda: dict(fixture_env))
    body = readiness.build_readiness_report()
    assert body["wallet_address_configured"] is True
    assert body["treasury_configured"] is False


def test_real_payment_readiness_env_overrides_shell_payment_mode(monkeypatch):
    fixture_env = {
        "PAYMENT_MODE": "real",
        "X402_ENABLED": "true",
        "X402_ONCHAIN_VERIFY": "false",
    }
    monkeypatch.setattr(readiness, "_effective_env", lambda: dict(fixture_env))
    body = readiness.build_readiness_report()
    assert body["payment_mode"] == "real"
    assert body["x402_enabled"] is True
