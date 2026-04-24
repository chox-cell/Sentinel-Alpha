from fastapi import HTTPException

from services.x402.payment import require_x402_payment


def test_real_mode_rejects_when_x402_disabled(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "false")

    try:
        require_x402_payment({"X402-PAYMENT": "x402-token"}, lane="basic")
        assert False, "Expected HTTPException when X402 is disabled"
    except HTTPException as exc:
        assert exc.status_code == 402


def test_real_mode_requires_x402_payment_header(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")

    try:
        require_x402_payment({}, lane="basic")
        assert False, "Expected HTTPException for missing x402 payment header"
    except HTTPException as exc:
        assert exc.status_code == 402


def test_real_mode_returns_pending_validation(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("PRICE_PRIORITY", "0.21")

    billing = require_x402_payment({"X402-PAYMENT": "x402-proof"}, lane="priority")
    assert billing["status"] == "pending_real_validation"
    assert billing["method"] == "x402"
    assert billing["lane"] == "priority"
    assert billing["amount"] == "0.21"
