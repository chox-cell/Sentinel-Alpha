import os
import json
import threading
import time
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_REPO_ROOT / ".env", override=True)

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, ValidationError
from typing import Optional, Dict, Any

from apps.webhooks.quicknode import router as quicknode_router
from services.x402.coinbase import verify_demo_payment
from services.x402.payment import require_x402_payment, build_x402_challenge, x402_payment_discovery_headers
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
from services.identity.erc8004_adapter import get_erc8004_status
from services.latency_shield.background import schedule_post_risk_tasks
from services.x402.payment_config import get_payment_status, get_pricing_tiers
from shared.config.env import get_env_bool, get_quicknode_env_status
from shared.config.limits import get_ingestion_limits

app = FastAPI(title="Sentinel Alpha API")
app.include_router(quicknode_router, include_in_schema=False)
MANIFEST_PATH = Path("docs/01_manifest/manifest.json")
_SUPPORTED_LANES = {"basic", "executive", "premium", "priority"}
_RATE_LIMIT_LOCK = threading.Lock()
_RATE_LIMIT_BUCKETS: dict[str, tuple[int, int]] = {}


def _get_rate_limit_config() -> tuple[bool, int]:
    enabled = get_env_bool("RATE_LIMIT_ENABLED", default=False)
    try:
        per_minute = int((os.getenv("RATE_LIMIT_PER_MINUTE", "60") or "60").strip())
    except ValueError:
        per_minute = 60
    if per_minute <= 0:
        per_minute = 60
    return enabled, per_minute


def _rate_limit_allow(client_ip: str | None) -> bool:
    enabled, per_minute = _get_rate_limit_config()
    if not enabled:
        return True
    key = (client_ip or "unknown").strip() or "unknown"
    window = int(time.time() // 60)
    with _RATE_LIMIT_LOCK:
        prev_window, count = _RATE_LIMIT_BUCKETS.get(key, (window, 0))
        if prev_window != window:
            count = 0
            prev_window = window
        count += 1
        _RATE_LIMIT_BUCKETS[key] = (prev_window, count)
        return count <= per_minute

class RequestModel(BaseModel):
    contract_address: str
    chain: str
    context: Optional[Dict[str, Any]] = None


_RISK_SCORE_POST_OPENAPI_EXTRA = {
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": RequestModel.model_json_schema(),
            }
        },
    }
}


_RISK_SCORE_OPTIONS_CORS_HEADERS = {
    "Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
    "Access-Control-Allow-Headers": "Content-Type,X-SENTINEL-LANE,X402-PAYMENT,PAYMENT-REQUIRED",
    "Access-Control-Expose-Headers": "PAYMENT-REQUIRED",
}


def _risk_score_discovery_challenge_json_response(request: Request) -> JSONResponse:
    """Same unpaid x402 discovery JSON body + headers as GET (basic lane); no scoring, no persistence."""
    client_ip = request.client.host if (request and request.client) else None
    if not _rate_limit_allow(client_ip):
        raise HTTPException(status_code=429, detail={"error": "rate_limit_exceeded"})

    challenge = build_x402_challenge(lane="basic")
    return JSONResponse(
        status_code=402,
        content=challenge,
        headers=x402_payment_discovery_headers(challenge),
    )


def _post_prepayment_discovery_response(lane: str) -> JSONResponse:
    """
    POST unpaid probes: preserve FastAPI's historical ``{"detail": challenge}`` shape for scanners
    (GET remains a flat JSON body).
    """
    challenge = build_x402_challenge(lane=lane)
    return JSONResponse(
        status_code=402,
        content={"detail": challenge},
        headers=x402_payment_discovery_headers(challenge),
    )


@app.get("/health", include_in_schema=False)
def health():
    return {
        "ok": True,
        "service": "Sentinel Alpha",
        "env": os.getenv("APP_ENV", "dev"),
    }


@app.get("/internal/env/source", include_in_schema=False)
def internal_env_source():
    payment_status = get_payment_status()
    return {
        "env_source": ".env",
        "override": True,
        "app_env": os.getenv("APP_ENV", "dev"),
        "payment_mode": payment_status["payment_mode"],
        "x402_enabled": get_env_bool("X402_ENABLED", default=False),
    }


@app.get("/contracts/risk-score")
def risk_score_get_x402_discovery(request: Request):
    """
    Discovery/validation-only: return x402 challenge on GET for directory crawlers (e.g. x402scan).
    Does not run risk scoring, require a body, or write state.
    """
    return _risk_score_discovery_challenge_json_response(request)


@app.patch(
    "/contracts/risk-score",
    include_in_schema=False,
)
def risk_score_patch_discovery_x402_only(request: Request):
    """Scanner compatibility: identical 402 challenge as GET — not listed in OpenAPI; does not run scoring."""
    return _risk_score_discovery_challenge_json_response(request)


@app.put(
    "/contracts/risk-score",
    include_in_schema=False,
)
def risk_score_put_discovery_x402_only(request: Request):
    """Scanner compatibility: identical 402 challenge as GET — not listed in OpenAPI; does not run scoring."""
    return _risk_score_discovery_challenge_json_response(request)


@app.delete(
    "/contracts/risk-score",
    include_in_schema=False,
)
def risk_score_delete_discovery_x402_only(request: Request):
    """Scanner compatibility: identical 402 challenge as GET — not listed in OpenAPI; does not run scoring."""
    return _risk_score_discovery_challenge_json_response(request)


@app.head("/contracts/risk-score")
def risk_score_head_x402_discovery(request: Request):
    """
    Discovery-only: same payment requirement signal as GET (402 + PAYMENT-REQUIRED), no JSON body,
    for validators that probe with HEAD (e.g. some directory scanners). No scoring, no DB writes.
    """
    client_ip = request.client.host if (request and request.client) else None
    if not _rate_limit_allow(client_ip):
        raise HTTPException(status_code=429, detail={"error": "rate_limit_exceeded"})

    challenge = build_x402_challenge(lane="basic")
    return Response(
        status_code=402,
        headers=x402_payment_discovery_headers(challenge),
    )


@app.options("/contracts/risk-score")
def risk_score_options_x402_discovery(request: Request):
    """
    Preflight-safe handler for scanners / browsers probing OPTIONS without running scoring or DB writes.
    """
    client_ip = request.client.host if (request and request.client) else None
    if not _rate_limit_allow(client_ip):
        raise HTTPException(status_code=429, detail={"error": "rate_limit_exceeded"})

    return Response(status_code=204, headers=_RISK_SCORE_OPTIONS_CORS_HEADERS)


@app.post("/contracts/risk-score", openapi_extra=_RISK_SCORE_POST_OPENAPI_EXTRA)
async def risk_score(
    request: Request,
    background_tasks: BackgroundTasks,
    payment_signature: str | None = Header(default=None, alias="PAYMENT-SIGNATURE"),
    x402_payment_hdr: str | None = Header(default=None, alias="X402-PAYMENT"),
    x_sentinel_lane: str | None = Header(default=None, alias="X-SENTINEL-LANE"),
):
    """
    Paid execution uses JSON body validated only after payment headers pass.
    Unpaid scanners may send empty/invalid JSON — route returns ``402`` + ``detail`` challenge first.
    """
    client_ip = request.client.host if (request and request.client) else None
    if not _rate_limit_allow(client_ip):
        raise HTTPException(status_code=429, detail={"error": "rate_limit_exceeded"})

    payment_signature = payment_signature if isinstance(payment_signature, str) else None
    x402_payment_hdr = x402_payment_hdr if isinstance(x402_payment_hdr, str) else None
    lane_raw = x_sentinel_lane if isinstance(x_sentinel_lane, str) else None
    lane = (lane_raw.strip().lower() if isinstance(lane_raw, str) and lane_raw.strip() else "basic")
    if lane not in _SUPPORTED_LANES:
        return JSONResponse(status_code=400, content={"error": "invalid_lane"})

    mode = (os.getenv("PAYMENT_MODE", "demo") or "demo").strip().lower()

    # Before reading the body: return challenge for probes that omit payment signals (avoids 422 noise).
    if mode == "demo":
        if not verify_demo_payment(payment_signature):
            return _post_prepayment_discovery_response(lane)
    else:
        x402_enabled = (os.getenv("X402_ENABLED", "false") or "false").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        if not x402_enabled:
            return JSONResponse(status_code=402, content={"detail": {"error": "x402_disabled"}})
        xp = (x402_payment_hdr or "").strip()
        if not xp:
            return _post_prepayment_discovery_response(lane)

    raw = await request.body()
    if not raw.strip():
        payload: dict[str, Any] = {}
    else:
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=422,
                detail=[{"loc": ["body"], "msg": "Invalid JSON payload", "type": "json_invalid"}],
            )
        if parsed is None:
            payload = {}
        elif not isinstance(parsed, dict):
            raise HTTPException(
                status_code=422,
                detail=[{"loc": ["body"], "msg": "JSON body must be an object", "type": "value_error"}],
            )
        else:
            payload = parsed

    try:
        req = RequestModel.model_validate(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    payment_billing = require_x402_payment(
        {
            "PAYMENT-SIGNATURE": payment_signature,
            "X402-PAYMENT": x402_payment_hdr,
        },
        lane=lane,
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


@app.get("/internal/cache-metrics", include_in_schema=False)
def internal_cache_metrics():
    return get_cache_metrics()


@app.get("/internal/manifest", include_in_schema=False)
def internal_manifest():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    public_base_url = (os.getenv("PUBLIC_BASE_URL") or "").strip()
    if public_base_url:
        manifest["public_base_url"] = public_base_url
    return manifest


@app.get("/internal/quicknode-live-check", include_in_schema=False)
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


@app.get("/internal/rate-limit/status", include_in_schema=False)
def internal_rate_limit_status():
    enabled, per_minute = _get_rate_limit_config()
    with _RATE_LIMIT_LOCK:
        keys_tracked = len(_RATE_LIMIT_BUCKETS)
    return {
        "rate_limit_enabled": enabled,
        "rate_limit_per_minute": per_minute,
        "key_strategy": "client_ip",
        "keys_tracked": keys_tracked,
    }


@app.get("/internal/security/status", include_in_schema=False)
def internal_security_status():
    enabled, per_minute = _get_rate_limit_config()
    return {
        "quicknode_signature_required": get_env_bool("QUICKNODE_SIGNATURE_REQUIRED", default=False),
        "rate_limit_enabled": enabled,
        "rate_limit_per_minute": per_minute,
    }


@app.get("/internal/dlq/status", include_in_schema=False)
def internal_dlq_status():
    return {
        "count_estimate": len(read_dlq(limit=1000)),
        "dlq_path": str(DLQ_PATH),
    }


@app.get("/internal/ingestion/status", include_in_schema=False)
def internal_ingestion_status():
    return get_ingestion_limits()


@app.get("/internal/identity/status", include_in_schema=False)
def internal_identity_status():
    return get_identity_status()


@app.get("/internal/identity/erc8004/status", include_in_schema=False)
def internal_identity_erc8004_status():
    return get_erc8004_status()


@app.get("/internal/attestation/status", include_in_schema=False)
def internal_attestation_status():
    return {
        "attestation_version": "attestation-0.1",
        "signing_mode": get_signing_mode(),
        "public_key_configured": bool(get_attestation_public_key()),
        "private_key_configured": bool(get_attestation_private_key()),
    }


@app.get("/internal/x402/status", include_in_schema=False)
def internal_x402_status():
    return get_payment_status()


@app.get("/internal/x402/pricing", include_in_schema=False)
def internal_x402_pricing():
    return {
        "pricing_tiers": get_pricing_tiers(),
        "default_lane": "basic",
    }


@app.get("/internal/x402/lanes", include_in_schema=False)
def internal_x402_lanes():
    return {
        "supported_lanes": ["basic", "executive", "premium", "priority"],
        "default_lane": "basic",
        "pricing_tiers": get_pricing_tiers(),
    }


@app.get("/internal/x402/challenge", include_in_schema=False)
def internal_x402_challenge(lane: str = "basic"):
    return build_x402_challenge(lane=lane)


@app.get("/internal/x402/verification/status", include_in_schema=False)
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


@app.get("/internal/x402/replay/status", include_in_schema=False)
def internal_x402_replay_status():
    return get_replay_status()


@app.get("/internal/x402/settlements/status", include_in_schema=False)
def internal_x402_settlements_status():
    return get_settlement_status()


@app.get("/internal/x402/onchain/status", include_in_schema=False)
def internal_x402_onchain_status():
    return get_onchain_verification_status()
