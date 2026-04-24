import os
from dotenv import load_dotenv
from fastapi import HTTPException
from services.x402.coinbase import verify_demo_payment, verify_real_payment_placeholder
from services.x402.payment_config import get_pricing_tiers

load_dotenv()


def build_x402_challenge(lane: str = "basic") -> dict:
    pricing = get_pricing_tiers()
    selected_lane = lane if lane in {"basic", "executive", "premium", "priority"} else "basic"
    network = (os.getenv("X402_NETWORK", "base") or "base").strip().lower() or "base"
    pay_to = (
        (os.getenv("X402_REVENUE_ADDRESS") or "").strip()
        or (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    )

    return {
        "x402_version": "0.2",
        "payment_method": "x402",
        "network": network,
        "pay_to": pay_to,
        "amount_usdc": f"{pricing[selected_lane]:.2f}",
        "asset": "USDC",
        "resource": "/contracts/risk-score",
        "instructions": "Submit X402-PAYMENT header to access this resource.",
        "lane": selected_lane,
    }


def require_x402_payment(headers: dict, lane: str = "basic") -> dict:
    mode = (os.getenv("PAYMENT_MODE", "demo") or "demo").strip().lower()
    x402_enabled = (os.getenv("X402_ENABLED", "false") or "false").strip().lower() in {"1", "true", "yes", "on"}
    pricing = get_pricing_tiers()
    selected_lane = lane if lane in {"basic", "executive", "premium", "priority"} else "basic"
    amount = pricing[selected_lane]

    payment_signature = headers.get("PAYMENT-SIGNATURE") if isinstance(headers, dict) else None
    x402_payment_header = None
    if isinstance(headers, dict):
        x402_payment_header = headers.get("X402-PAYMENT") or headers.get("x402-payment")

    if mode == "demo":
        if not verify_demo_payment(payment_signature):
            raise HTTPException(status_code=402, detail="Payment Required")
        return {
            "amount": f"{amount:.2f}",
            "method": "x402",
            "status": "demo",
            "lane": selected_lane,
        }

    # PAYMENT_MODE=real
    if not x402_enabled:
        raise HTTPException(status_code=402, detail={"error": "x402_disabled"})

    if not verify_real_payment_placeholder(x402_payment_header):
        raise HTTPException(status_code=402, detail=build_x402_challenge(selected_lane))

    return {
        "amount": f"{amount:.2f}",
        "method": "x402",
        "status": "pending_real_validation",
        "lane": selected_lane,
    }


def require_payment(payment_signature: str | None):
    # Backward-compatible wrapper for existing API handler.
    require_x402_payment({"PAYMENT-SIGNATURE": payment_signature}, lane="basic")
