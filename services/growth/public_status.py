"""Public integration status payloads (no secrets, no env dump)."""

from __future__ import annotations

from services.growth.public_usage_metrics import get_public_usage_metrics
from services.x402.payment_config import get_pricing_tiers


def build_public_integration_status() -> dict:
    tiers = get_pricing_tiers()
    basic = tiers.get("basic", 0.02)
    return {
        "service": "BeezShield Sentinel Alpha",
        "api_status": "live",
        "x402_resource": "/contracts/risk-score",
        "x402scan_registered": True,
        "payment_network": "base",
        "asset": "USDC",
        "basic_lane_amount_usdc": f"{basic:.2f}",
        "no_guarantee": True,
        "disclaimer": (
            "Pre-execution risk decision layer for agents. "
            "Not a security guarantee, partnership, or x402 endorsement."
        ),
        "directory_note": (
            "x402scan listing is marketplace discoverability only."
        ),
    }


def build_public_metrics_payload() -> dict:
    return get_public_usage_metrics()
