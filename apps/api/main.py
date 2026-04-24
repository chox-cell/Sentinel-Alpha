import os
from dotenv import load_dotenv

from fastapi import BackgroundTasks, FastAPI, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any

from apps.webhooks.quicknode import router as quicknode_router
from services.x402.payment import require_payment
from services.risk_service.service import evaluate_contract_with_meta
from services.cache.metrics import get_cache_metrics
from services.latency_shield.background import schedule_post_risk_tasks

load_dotenv()

app = FastAPI(title="Sentinel Alpha API")
app.include_router(quicknode_router)

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
