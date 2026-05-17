from fastapi import HTTPException

from services.x402.payment import require_x402_payment


def test_real_mode_missing_payment_returns_challenge(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("X402_NETWORK", "base")
    monkeypatch.delenv("X402_REVENUE_ADDRESS", raising=False)
    monkeypatch.setenv("SENTINEL_TREASURY_WALLET", "0xtreasury")
    monkeypatch.setenv("PRICE_BASIC", "0.02")

    try:
        require_x402_payment({}, lane="basic")
        assert False, "Expected HTTPException challenge"
    except HTTPException as exc:
        assert exc.status_code == 402
        detail = exc.detail
        assert detail["x402_version"] == "0.2"
        assert detail["payment_method"] == "x402"
        assert detail["network"] == "eip155:8453"
        assert detail["pay_to"] == "0xtreasury"
        assert detail["amount_usdc"] == "0.02"
        assert detail["asset"] == "USDC"
        assert detail["resource"] == "/contracts/risk-score"
        assert detail["instructions"] == "Submit X402-PAYMENT header to access this resource."
        assert detail["x402Version"] == 1
        assert detail["error"] == "X-PAYMENT header is required"
        assert detail["accepts"][0]["scheme"] == "exact"
        assert detail["accepts"][0]["network"] == "base"
        h = {str(k).lower(): v for k, v in (exc.headers or {}).items()}
        assert h.get("payment-required") is None
        assert detail["accepts"][0]["amount"] == "20000"
        assert detail["accepts"][0]["maxAmountRequired"] == "20000"
        assert detail["accepts"][0]["maxTimeoutSeconds"] == 60
        assert detail["accepts"][0]["extra"]["name"] == "USD Coin"
        assert detail["accepts"][0]["outputSchema"]["input"]["method"] == "POST"


def test_real_mode_disabled_returns_x402_disabled_error(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "false")

    try:
        require_x402_payment({"X402-PAYMENT": "token"}, lane="basic")
        assert False, "Expected disabled x402 error"
    except HTTPException as exc:
        assert exc.status_code == 402
        assert exc.detail == {"error": "x402_disabled"}
