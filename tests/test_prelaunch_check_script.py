import os
from scripts import prelaunch_check


def test_prelaunch_script_ready_path_and_required_lines(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_MOCK_ONCHAIN_VERIFY", "false")
    monkeypatch.setenv("BASE_RPC_URL", "https://base-rpc.example/from-dotenv")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    monkeypatch.setenv("AGENT_WALLET_ADDRESS", "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

    report = prelaunch_check.build_prelaunch_report()
    out = prelaunch_check.format_prelaunch_report(report)
    assert "pytest command reminder: python3 -m pytest tests/ -q --tb=no" in out
    assert "env source: .env" in out
    assert "PAYMENT_MODE: real" in out
    assert "payment real mode ready: true" in out
    assert "X402_ENABLED: true" in out
    assert "x402 enabled: true" in out
    assert "mock mode disabled: true" in out
    assert "BASE_RPC_URL configured: true" in out
    assert "wallet configured: true" in out
    assert "treasury configured: true" in out
    assert "agentic-market.json exists: true" in out
    assert "README exists: true" in out
    assert "SDK docs exist: true" in out
    assert "launch docs exist: true" in out
    assert "launch ready: true" in out
    assert "readiness verdict: ready" in out


def test_prelaunch_script_not_ready_and_does_not_print_secret_values(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "demo")
    monkeypatch.setenv("X402_ENABLED", "false")
    monkeypatch.setenv("X402_MOCK_ONCHAIN_VERIFY", "true")
    monkeypatch.setenv("BASE_RPC_URL", "https://super-secret-rpc.example/token-value")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "")
    monkeypatch.setenv("AGENT_WALLET_ADDRESS", "")

    report = prelaunch_check.build_prelaunch_report()
    out = prelaunch_check.format_prelaunch_report(report)
    assert "PAYMENT_MODE: demo" in out
    assert "X402_ENABLED: false" in out
    assert "mock mode disabled: false" in out
    assert "launch ready: false" in out
    assert "readiness verdict: not_ready" in out
    assert "token-value" not in out
