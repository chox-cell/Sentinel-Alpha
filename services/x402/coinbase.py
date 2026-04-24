import os
from fastapi import HTTPException
from dotenv import load_dotenv
from services.x402.payment_config import get_pricing_tiers
from services.x402.onchain_verifier import verify_usdc_transfer_tx

load_dotenv()


def verify_demo_payment(payment_signature: str | None) -> bool:
    expected = os.getenv("PAYMENT_DEMO_SIGNATURE", "demo")
    return payment_signature == expected


def parse_x402_payment_header(header: str) -> dict:
    value = (header or "").strip()
    prefix = "tx:"
    if not value.startswith(prefix):
        return {"ok": False, "error": "invalid_prefix"}

    tx_hash = value[len(prefix) :].strip()
    if not tx_hash.startswith("0x"):
        return {"ok": False, "error": "invalid_tx_hash_shape"}
    if len(tx_hash) != 66:
        return {"ok": False, "error": "invalid_tx_hash_shape"}
    if not all(ch in "0123456789abcdefABCDEF" for ch in tx_hash[2:]):
        return {"ok": False, "error": "invalid_tx_hash_shape"}

    return {"ok": True, "kind": "tx", "tx_hash": tx_hash}


def verify_real_payment(payment_header: str, lane: str = "basic") -> dict:
    selected_lane = lane if lane in {"basic", "executive", "premium", "priority"} else "basic"
    pricing = get_pricing_tiers()
    parsed = parse_x402_payment_header(payment_header)

    if not parsed.get("ok"):
        return {
            "verified": False,
            "status": "invalid_payment_header",
            "tx_hash": None,
            "lane": selected_lane,
            "amount": f"{pricing[selected_lane]:.2f}",
            "reason": parsed.get("error", "invalid_x402_payment"),
        }

    result = {
        "verified": False,
        "status": "tx_format_valid_unverified",
        "tx_hash": parsed["tx_hash"],
        "lane": selected_lane,
        "amount": f"{pricing[selected_lane]:.2f}",
        "reason": "onchain_verification_not_enabled",
    }
    onchain_enabled = (os.getenv("X402_ONCHAIN_VERIFY", "false") or "false").strip().lower() in {"1", "true", "yes", "on"}
    if not onchain_enabled:
        return result

    treasury_wallet = (
        (os.getenv("X402_REVENUE_ADDRESS") or "").strip()
        or (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    )
    onchain = verify_usdc_transfer_tx(
        tx_hash=parsed["tx_hash"],
        expected_amount=float(pricing[selected_lane]),
        treasury_wallet=treasury_wallet,
    )
    if onchain.get("verified") is True:
        result["verified"] = True
        result["status"] = "verified"
        result["reason"] = "onchain_verified"
        return result

    raise HTTPException(
        status_code=402,
        detail={"error": "x402_payment_not_verified", "status": onchain.get("status", "verification_failed")},
    )
