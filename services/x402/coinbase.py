import os
from dotenv import load_dotenv
from services.x402.payment_config import get_pricing_tiers

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

    return {
        "verified": False,
        "status": "tx_format_valid_unverified",
        "tx_hash": parsed["tx_hash"],
        "lane": selected_lane,
        "amount": f"{pricing[selected_lane]:.2f}",
        "reason": "onchain_verification_not_enabled",
    }
