"""x402 v2 + Bazaar discovery payloads (separate from x402scan v1 body-first /contracts/risk-score)."""

from __future__ import annotations

import base64
import json as json_stdlib
import os

from services.x402.payment import (
    BASE_MAINNET_USDC_CONTRACT,
    X402_V1_DISCOVERY_ERROR,
    _accepts_item_network,
    _usdc_amount_atomic_string,
)
from services.x402.payment_config import get_pricing_tiers

RISK_SCORE_V2_PATH = "/contracts/risk-score-v2"


def _public_api_base() -> str:
    return (
        (os.getenv("PUBLIC_BASE_URL") or "https://api.beezshield.com").strip().rstrip("/")
        or "https://api.beezshield.com"
    )


def risk_score_v2_resource_public_url() -> str:
    return f"{_public_api_base()}{RISK_SCORE_V2_PATH}"


def _treasury_pay_to() -> str:
    return (
        (os.getenv("X402_REVENUE_ADDRESS") or "").strip()
        or (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    )


def _bazaar_extensions() -> dict:
    return {
        "bazaar": {
            "info": {
                "title": "BeezShield Sentinel Alpha Risk Score",
                "description": (
                    "Pre-execution risk decision layer for autonomous agents on Base. "
                    "x402-gated policy assistance only — not a security guarantee, "
                    "partnership, or endorsement."
                ),
                "input": {
                    "contract_address": "0x1111111111111111111111111111111111111111",
                    "chain": "base",
                },
                "output": {
                    "risk_score": "number",
                    "decision": "allow|review|block",
                },
            },
            "schema": {
                "input": {
                    "type": "object",
                    "required": ["contract_address", "chain"],
                    "properties": {
                        "contract_address": {"type": "string"},
                        "chain": {"type": "string"},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "risk_score": {"type": "number"},
                        "decision": {"type": "string"},
                    },
                },
            },
        }
    }


def build_accepts_v2_item(*, pay_to: str, amount_float: float) -> dict:
    atomic = _usdc_amount_atomic_string(amount_float)
    return {
        "scheme": "exact",
        "network": _accepts_item_network(),
        "asset": BASE_MAINNET_USDC_CONTRACT,
        "amount": atomic,
        "payTo": pay_to,
        "maxTimeoutSeconds": 60,
    }


def build_x402_challenge_v2_bazaar(lane: str = "basic") -> dict:
    pricing = get_pricing_tiers()
    selected_lane = lane if lane in {"basic", "executive", "premium", "priority"} else "basic"
    pay_to = _treasury_pay_to()
    amount_float = pricing[selected_lane]
    return {
        "x402Version": 2,
        "error": X402_V1_DISCOVERY_ERROR,
        "resource": {
            "url": risk_score_v2_resource_public_url(),
            "type": "http",
            "method": "POST",
            "description": "BeezShield Sentinel Alpha risk score",
        },
        "accepts": [build_accepts_v2_item(pay_to=pay_to, amount_float=amount_float)],
        "extensions": _bazaar_extensions(),
    }


def encode_payment_required_header_v2(challenge_body: dict) -> str:
    """Standard base64 over full v2 payment-required JSON (resource + extensions included)."""
    raw = json_stdlib.dumps(challenge_body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


def decode_payment_required_header(value: str) -> dict:
    raw = base64.b64decode(value.encode("ascii"))
    return json_stdlib.loads(raw.decode("utf-8"))


def x402_v2_discovery_headers(challenge_body: dict) -> dict[str, str]:
    return {
        "PAYMENT-REQUIRED": encode_payment_required_header_v2(challenge_body),
        "Access-Control-Expose-Headers": "PAYMENT-REQUIRED",
    }
