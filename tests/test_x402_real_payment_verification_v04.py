from fastapi import HTTPException

from services.x402.coinbase import verify_real_payment
from services.x402.payment import require_x402_payment


def test_verify_real_payment_valid_tx_format(monkeypatch):
    monkeypatch.setenv("PRICE_EXECUTIVE", "0.06")
    result = verify_real_payment(
        "tx:0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        lane="executive",
    )
    assert result == {
        "verified": False,
        "status": "tx_format_valid_unverified",
        "tx_hash": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "lane": "executive",
        "amount": "0.06",
        "reason": "onchain_verification_not_enabled",
    }


def test_verify_real_payment_invalid_header(monkeypatch):
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    result = verify_real_payment("bad-header", lane="basic")
    assert result["verified"] is False
    assert result["status"] == "invalid_payment_header"
    assert result["reason"] in {"invalid_prefix", "invalid_tx_hash_shape"}


def test_require_x402_payment_rejects_invalid_real_header(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    try:
        require_x402_payment({"X402-PAYMENT": "tx:0x1234"}, lane="basic")
        assert False, "Expected HTTPException for invalid payment header"
    except HTTPException as exc:
        assert exc.status_code == 402
        assert exc.detail == {"error": "invalid_x402_payment"}


def test_require_x402_payment_accepts_valid_real_header(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("PRICE_BASIC", "0.02")
    billing = require_x402_payment(
        {"X402-PAYMENT": "tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
        lane="basic",
    )
    assert billing["status"] == "tx_format_valid_unverified"
    assert billing["method"] == "x402"
    assert billing["amount"] == "0.02"
