import os
import json
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_REPO_ROOT / ".env", override=True)

from fastapi import BackgroundTasks, FastAPI, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any

from apps.webhooks.quicknode import router as quicknode_router
from services.x402.payment import require_x402_payment, build_x402_challenge
from services.x402.onchain_verifier import get_onchain_verification_status
from services.x402.replay_guard import get_replay_status
from services.x402.settlement_ledger import get_settlement_status
from services.risk_service.service import evaluate_contract_with_meta
from services.cache.metrics import get_cache_metrics
from services.attestation_layer.key_signing import (
    get_attestation_private_key,
    get_attestation_public_key,
    get_signing_mode,
)
from services.dlq.dead_letter import DLQ_PATH, read_dlq
from services.identity.identity_config import get_identity_status
from services.latency_shield.background import schedule_post_risk_tasks
from services.x402.payment_config import get_payment_status, get_pricing_tiers
from shared.config.env import get_env_bool, get_quicknode_env_status
from shared.config.limits import get_ingestion_limits

app = FastAPI(title="Sentinel Alpha API")
app.include_router(quicknode_router)
MANIFEST_PATH = Path("docs/01_manifest/manifest.json")

class RequestModel(BaseModel):
    contract_address: str
    chain: str
    context: Optional[Dict[str, Any]] = None

@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "Sentinel Alpha",
        "env": os.getenv("APP_ENV", "dev"),
    }


@app.get("/internal/env/source")
def internal_env_source():
    payment_status = get_payment_status()
    return {
        "env_source": ".env",
        "override": True,
        "app_env": os.getenv("APP_ENV", "dev"),
        "payment_mode": payment_status["payment_mode"],
        "x402_enabled": get_env_bool("X402_ENABLED", default=False),
    }


@app.post("/contracts/risk-score")
def risk_score(
    req: RequestModel,
    background_tasks: BackgroundTasks,
    payment_signature: str | None = Header(default=None, alias="PAYMENT-SIGNATURE"),
    x402_payment: str | None = Header(default=None, alias="X402-PAYMENT"),
):
    payment_billing = require_x402_payment(
        {
            "PAYMENT-SIGNATURE": payment_signature,
            "X402-PAYMENT": x402_payment,
        },
        lane="basic",
    )

    result = evaluate_contract_with_meta(
        contract_address=req.contract_address,
        chain=req.chain,
        context=req.context,
    )
    response = result["response"]
    if isinstance(payment_billing, dict):
        response["billing"] = {
            "amount": payment_billing.get("amount", response.get("billing", {}).get("amount", "0.02")),
            "method": payment_billing.get("method", response.get("billing", {}).get("method", "x402")),
            "status": payment_billing.get("status", response.get("billing", {}).get("status", "demo")),
        }

    schedule_post_risk_tasks(
        background_tasks,
        event_payload={
            "contract_address": req.contract_address,
            "chain": req.chain,
            "context": req.context,
            "response": response,
        },
        outcome_record=result.get("outcome_record"),
    )

    return response


@app.get("/internal/cache-metrics")
def internal_cache_metrics():
    return get_cache_metrics()


@app.get("/internal/manifest")
def internal_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


@app.get("/internal/quicknode-live-check")
def internal_quicknode_live_check():
    status = get_quicknode_env_status()
    chain = os.getenv("QUICKNODE_CHAIN", "base").strip().lower() or "base"
    checks = {
        "webhook_url_configured": status["webhook_url_configured"],
        "webhook_secret_configured": status["webhook_secret_configured"],
        "dry_run": get_env_bool("QUICKNODE_DRY_RUN", default=False),
        "chain": chain,
    }
    ready_for_live = (
        checks["webhook_url_configured"]
        and checks["webhook_secret_configured"]
        and not checks["dry_run"]
    )
    return {
        "ready_for_live": ready_for_live,
        "checks": checks,
    }


@app.get("/internal/dlq/status")
def internal_dlq_status():
    return {
        "count_estimate": len(read_dlq(limit=1000)),
        "dlq_path": str(DLQ_PATH),
    }


@app.get("/internal/ingestion/status")
def internal_ingestion_status():
    return get_ingestion_limits()


@app.get("/internal/identity/status")
def internal_identity_status():
    return get_identity_status()


@app.get("/internal/attestation/status")
def internal_attestation_status():
    return {
        "attestation_version": "attestation-0.1",
        "signing_mode": get_signing_mode(),
        "public_key_configured": bool(get_attestation_public_key()),
        "private_key_configured": bool(get_attestation_private_key()),
    }


@app.get("/internal/x402/status")
def internal_x402_status():
    return get_payment_status()


@app.get("/internal/x402/pricing")
def internal_x402_pricing():
    return {
        "pricing_tiers": get_pricing_tiers(),
        "default_lane": "basic",
    }


@app.get("/internal/x402/challenge")
def internal_x402_challenge(lane: str = "basic"):
    return build_x402_challenge(lane=lane)


@app.get("/internal/x402/verification/status")
def internal_x402_verification_status():
    onchain_verify = (os.getenv("X402_ONCHAIN_VERIFY", "false") or "false").strip().lower() in {"1", "true", "yes", "on"}
    network = (os.getenv("X402_NETWORK", "base") or "base").strip().lower() or "base"
    treasury = (
        (os.getenv("X402_REVENUE_ADDRESS") or "").strip()
        or (os.getenv("SENTINEL_TREASURY_WALLET") or "").strip()
    )
    return {
        "onchain_verify_enabled": onchain_verify,
        "accepted_payment_format": "tx:0x<64_hex_chars>",
        "network": network,
        "treasury_configured": bool(treasury),
    }


@app.get("/internal/x402/replay/status")
def internal_x402_replay_status():
    return get_replay_status()


@app.get("/internal/x402/settlements/status")
def internal_x402_settlements_status():
    return get_settlement_status()


@app.get("/internal/x402/onchain/status")
def internal_x402_onchain_status():
    return get_onchain_verification_status()
