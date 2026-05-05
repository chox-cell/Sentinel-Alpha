import os
from scripts import production_env_check as prod_check


def test_production_env_check_ready_and_secret_safe(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("PUBLIC_BASE_URL", "https://api.sentinel-alpha.example")
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_MOCK_ONCHAIN_VERIFY", "false")
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://base-rpc.example/secret")
    monkeypatch.setenv("QUICKNODE_SIGNATURE_REQUIRED", "true")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "true")
    monkeypatch.setenv("AGENT_WALLET_ADDRESS", "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    report = prod_check.build_production_report()
    out = prod_check.format_report(report)
    assert "APP_ENV=production: true" in out
    assert "PUBLIC_BASE_URL configured: true" in out
    assert "PAYMENT_MODE=real: true" in out
    assert "X402_ENABLED=true: true" in out
    assert "X402_MOCK_ONCHAIN_VERIFY=false: true" in out
    assert "X402_ONCHAIN_VERIFY=true: true" in out
    assert "BASE_RPC_URL configured: true" in out
    assert "QUICKNODE_SIGNATURE_REQUIRED=true: true" in out
    assert "RATE_LIMIT_ENABLED=true: true" in out
    assert "wallet configured: true" in out
    assert "treasury configured: true" in out
    assert "production ready: true" in out
    assert "token" not in out.lower()


def test_production_env_check_not_ready_when_required_flags_missing(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("PUBLIC_BASE_URL", "https://api.sentinel-alpha.example")
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_MOCK_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("X402_ONCHAIN_VERIFY", "false")
    monkeypatch.setenv("BASE_RPC_URL", "")
    monkeypatch.setenv("QUICKNODE_SIGNATURE_REQUIRED", "false")
    monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")
    monkeypatch.setenv("AGENT_WALLET_ADDRESS", "")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "")

    report = prod_check.build_production_report()
    out = prod_check.format_report(report)
    assert "X402_MOCK_ONCHAIN_VERIFY=false: false" in out
    assert "X402_ONCHAIN_VERIFY=true: false" in out
    assert "BASE_RPC_URL configured: false" in out
    assert "production ready: false" in out
