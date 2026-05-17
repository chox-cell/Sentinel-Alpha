import base64
import json as json_stdlib
import os
import uuid
from dotenv import load_dotenv
from fastapi import HTTPException
from services.x402.coinbase import verify_demo_payment, verify_real_payment
from services.x402.payment_config import get_pricing_tiers
from services.x402.replay_guard import is_payment_replay, record_payment_fingerprint
from services.x402.settlement_ledger import write_settlement_record

load_dotenv()

# x402scan v1 schema / directory validators (top-level discovery body + PAYMENT-REQUIRED).
X402_V1_DISCOVERY_ERROR = "X-PAYMENT header is required"


def _x402_env_network_slug() -> str:
    return (os.getenv("X402_NETWORK", "base") or "base").strip().lower() or "base"


def _x402_challenge_network() -> str:
    """Legacy top-level network id (CAIP-2). Base mainnet -> eip155:8453."""
    net = _x402_env_network_slug()
    if net == "base":
        return "eip155:8453"
    return net


def _accepts_item_network() -> str:
    """`accepts[]` network slug for x402scan v1 (Base -> ``base``, not CAIP-2)."""
    net = _x402_env_network_slug()
    if net in {"base", "eip155:8453"}:
        return "base"
    return net


def _risk_score_resource_public_url() -> str:
    base = (
        (os.getenv("PUBLIC_BASE_URL") or "https://api.beezshield.com").strip().rstrip("/")
        or "https://api.beezshield.com"
    )
    return f"{base}/contracts/risk-score"


USDC_DECIMALS = 6

# Base mainnet USDC — used in `accepts[]` / PAYMENT-REQUIRED for exact EVM compatibility (CAIP-2 eip155:8453).
BASE_MAINNET_USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"


def _usdc_amount_atomic_string(usdc_human: float) -> str:
    return str(int(round(usdc_human * (10**USDC_DECIMALS))))


def _accepts_evm_asset_for_network() -> str:
    """Prefer USDC contract address on Base mainnet; symbolic USDC if network is non-Base."""
    return BASE_MAINNET_USDC_CONTRACT if _accepts_item_network() == "base" else "USDC"


def build_accepts_exact_evm_item(*, pay_to: str, amount_float: float) -> dict:
    """Single `accepts[]` entry for discovery / PAYMENT-REQUIRED (exact scheme, Base USDC atomic units)."""
    atomic = _usdc_amount_atomic_string(amount_float)
    return {
        "scheme": "exact",
        "network": _accepts_item_network(),
        "asset": _accepts_evm_asset_for_network(),
        "amount": atomic,
        "maxAmountRequired": atomic,
        "payTo": pay_to,
        "maxTimeoutSeconds": 60,
        "resource": _risk_score_resource_public_url(),
        "description": "BeezShield Sentinel Alpha risk score",
        "mimeType": "application/json",
        "extra": {"name": "USD Coin", "version": "2"},
    }


def encode_payment_required_header(challenge_body: dict) -> str:
    """
    Compatibility header used by some x402 clients/directory validators alongside HTTP 402.
    Value is standard base64 (no PEM wrapping) over compact JSON {"x402Version","accepts"} only.
    Not an official-protocol claim; aligns with Coinbase/x402-era PAYMENT-REQUIRED patterns for discovery.
    """
    envelope = {
        "x402Version": challenge_body["x402Version"],
        "error": challenge_body["error"],
        "accepts": challenge_body["accepts"],
    }
    raw = json_stdlib.dumps(envelope, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


def x402_payment_discovery_headers(challenge_body: dict) -> dict[str, str]:
    return {
        "PAYMENT-REQUIRED": encode_payment_required_header(challenge_body),
        "Access-Control-Expose-Headers": "PAYMENT-REQUIRED",
    }


def build_x402_challenge(lane: str = "basic") -> dict:
    pricing = get_pricing_tiers()
    selected_lane = lane if lane in {"basic", "executive", "premium", "priority"} else "basic"
    pay_to = (
        (os.getenv("X402_REVENUE_ADDRESS") or "").strip()
        or (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    )
    amount_float = pricing[selected_lane]

    accepts_item = build_accepts_exact_evm_item(pay_to=pay_to, amount_float=amount_float)

    return {
        "x402_version": "0.2",
        "payment_method": "x402",
        "network": _x402_challenge_network(),
        "pay_to": pay_to,
        "amount_usdc": f"{amount_float:.2f}",
        "asset": "USDC",
        "resource": "/contracts/risk-score",
        "instructions": "Submit X402-PAYMENT header to access this resource.",
        "lane": selected_lane,
        # Discovery / validator-adjacent fields (preserve legacy snake_case keys above).
        "x402Version": 1,
        "error": X402_V1_DISCOVERY_ERROR,
        "accepts": [accepts_item],
    }


def require_x402_payment(headers: dict, lane: str = "basic") -> dict:
    mode = (os.getenv("PAYMENT_MODE", "demo") or "demo").strip().lower()
    x402_enabled = (os.getenv("X402_ENABLED", "false") or "false").strip().lower() in {"1", "true", "yes", "on"}
    pricing = get_pricing_tiers()
    selected_lane = lane if lane in {"basic", "executive", "premium", "priority"} else "basic"
    lane_amount = pricing[selected_lane]

    payment_signature = headers.get("PAYMENT-SIGNATURE") if isinstance(headers, dict) else None
    x402_payment_header = None
    if isinstance(headers, dict):
        x402_payment_header = headers.get("X402-PAYMENT") or headers.get("x402-payment")

    if mode == "demo":
        if not verify_demo_payment(payment_signature):
            raise HTTPException(status_code=402, detail="Payment Required")
        return {
            "amount": f"{lane_amount:.2f}",
            "method": "x402",
            "status": "demo",
            "lane": selected_lane,
        }

    # PAYMENT_MODE=real
    if not x402_enabled:
        raise HTTPException(status_code=402, detail={"error": "x402_disabled"})

    if not x402_payment_header:
        challenge = build_x402_challenge(selected_lane)
        raise HTTPException(
            status_code=402,
            detail=challenge,
            headers=x402_payment_discovery_headers(challenge),
        )

    verification = verify_real_payment(x402_payment_header, lane=selected_lane)
    if verification["status"] not in {"tx_format_valid_unverified", "verified"}:
        raise HTTPException(status_code=402, detail={"error": "invalid_x402_payment"})
    if is_payment_replay(x402_payment_header):
        raise HTTPException(status_code=402, detail={"error": "x402_replay_detected"})
    trace_id = str(uuid.uuid4())
    replay_record = record_payment_fingerprint(x402_payment_header, trace_id=trace_id)
    network = (os.getenv("X402_NETWORK", "base") or "base").strip().lower() or "base"
    treasury_wallet = (
        (os.getenv("X402_REVENUE_ADDRESS") or "").strip()
        or (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    )
    write_settlement_record(
        {
            "trace_id": trace_id,
            "tx_hash": verification.get("tx_hash"),
            "payment_fingerprint": replay_record.get("fingerprint"),
            "lane": selected_lane,
            "amount": verification["amount"],
            "network": network,
            "treasury_wallet": treasury_wallet,
            "verification_status": verification["status"],
        }
    )

    return {
        "amount": verification["amount"],
        "method": "x402",
        "status": verification["status"],
        "lane": selected_lane,
    }


def require_payment(payment_signature: str | None):
    # Backward-compatible wrapper for existing API handler.
    require_x402_payment({"PAYMENT-SIGNATURE": payment_signature}, lane="basic")
