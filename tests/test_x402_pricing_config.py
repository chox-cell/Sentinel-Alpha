from services.x402.payment_config import get_payment_status


def test_pricing_tiers_visible_and_valid(monkeypatch):
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    monkeypatch.setenv("PRICE_EXECUTIVE", "0.05")
    monkeypatch.setenv("PRICE_PREMIUM", "0.10")
    monkeypatch.setenv("PRICE_PRIORITY", "0.15")
    monkeypatch.setenv("X402_DEFAULT_PRICE_USDC", "0.05")

    status = get_payment_status()
    assert status["pricing_tiers"]["basic"] == 0.02
    assert status["pricing_tiers"]["premium"] == 0.10
    assert status["pricing_valid"] is True


def test_pricing_invalid_order_fails_validation(monkeypatch):
    monkeypatch.setenv("PRICE_BASIC", "0.06")
    monkeypatch.setenv("PRICE_EXECUTIVE", "0.05")
    monkeypatch.setenv("PRICE_PREMIUM", "0.10")
    monkeypatch.setenv("PRICE_PRIORITY", "0.15")
    monkeypatch.setenv("X402_DEFAULT_PRICE_USDC", "0.05")
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("CDP_PROJECT_ID", "project")
    monkeypatch.setenv("CDP_API_KEY_NAME", "name")
    monkeypatch.setenv("CDP_API_KEY_PRIVATE_KEY", "private")
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xabc")

    status = get_payment_status()
    assert status["pricing_valid"] is False
    assert status["real_payments_enabled"] is False
