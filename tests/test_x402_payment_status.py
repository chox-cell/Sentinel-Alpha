from services.x402.payment_config import get_payment_status


def test_x402_payment_status_defaults(monkeypatch):
    monkeypatch.delenv("PAYMENT_MODE", raising=False)
    monkeypatch.delenv("CDP_PROJECT_ID", raising=False)
    monkeypatch.delenv("CDP_API_KEY_NAME", raising=False)
    monkeypatch.delenv("CDP_API_KEY_PRIVATE_KEY", raising=False)
    monkeypatch.delenv("SENTINEL_TREASURY_WALLET", raising=False)
    monkeypatch.delenv("X402_NETWORK", raising=False)

    status = get_payment_status()
    assert status == {
        "payment_mode": "demo",
        "payment_method": "x402",
        "cdp_project_configured": False,
        "cdp_api_key_configured": False,
        "wallet_address_configured": False,
        "network": "base",
        "real_payments_enabled": False,
    }


def test_x402_payment_status_real_mode_requires_all_env(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("CDP_PROJECT_ID", "project")
    monkeypatch.setenv("CDP_API_KEY_NAME", "name")
    monkeypatch.setenv("CDP_API_KEY_PRIVATE_KEY", "private")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xabc")
    monkeypatch.setenv("X402_NETWORK", "base")

    status = get_payment_status()
    assert status["payment_mode"] == "real"
    assert status["cdp_project_configured"] is True
    assert status["cdp_api_key_configured"] is True
    assert status["wallet_address_configured"] is True
    assert status["real_payments_enabled"] is True
