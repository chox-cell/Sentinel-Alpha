from fastapi import HTTPException

from services.x402.payment import require_x402_payment


def test_demo_mode_accepts_demo_signature(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "demo")
    monkeypatch.setenv("PAYMENT_DEMO_SIGNATURE", "demo")

    billing = require_x402_payment({"PAYMENT-SIGNATURE": "demo"}, lane="basic")
    assert billing["status"] == "demo"
    assert billing["method"] == "x402"
    assert billing["lane"] == "basic"


def test_demo_mode_rejects_bad_signature(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "demo")
    monkeypatch.setenv("PAYMENT_DEMO_SIGNATURE", "demo")

    try:
        require_x402_payment({"PAYMENT-SIGNATURE": "wrong"}, lane="basic")
        assert False, "Expected HTTPException for missing demo signature"
    except HTTPException as exc:
        assert exc.status_code == 402
