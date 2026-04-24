import os
import json
from pathlib import Path
from dotenv import load_dotenv

from fastapi import BackgroundTasks, FastAPI, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any

from apps.webhooks.quicknode import router as quicknode_router
from services.x402.payment import require_payment
from services.risk_service.service import evaluate_contract_with_meta
from services.cache.metrics import get_cache_metrics
from services.dlq.dead_letter import DLQ_PATH, read_dlq
from services.identity.identity_config import get_identity_status
from services.latency_shield.background import schedule_post_risk_tasks
from shared.config.env import get_env_bool, get_quicknode_env_status
from shared.config.limits import get_ingestion_limits

load_dotenv()

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

@app.post("/contracts/risk-score")
def risk_score(
    req: RequestModel,
    background_tasks: BackgroundTasks,
    payment_signature: str | None = Header(default=None, alias="PAYMENT-SIGNATURE"),
):
    require_payment(payment_signature)

    result = evaluate_contract_with_meta(
        contract_address=req.contract_address,
        chain=req.chain,
        context=req.context,
    )
    response = result["response"]

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
