from fastapi import HTTPException

from services.x402.payment import require_x402_payment
from services.x402 import replay_guard


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


def test_real_mode_returns_pending_validation(monkeypatch, tmp_path):
    monkeypatch.setattr(replay_guard, "PAYMENTS_LOG_PATH", tmp_path / "x402_payments.jsonl")
    monkeypatch.setenv("PAYMENT_MODE", "real")
    monkeypatch.setenv("X402_ENABLED", "true")
    monkeypatch.setenv("PRICE_PRIORITY", "0.21")

    tx_hash = "0x" + ("a" * 64)
    billing = require_x402_payment({"X402-PAYMENT": f"tx:{tx_hash}"}, lane="priority")
    assert billing["status"] == "tx_format_valid_unverified"
    assert billing["method"] == "x402"
    assert billing["lane"] == "priority"
    assert billing["amount"] == "0.21"
