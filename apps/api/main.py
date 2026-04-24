import os
from dotenv import load_dotenv

from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any

from apps.webhooks.quicknode import router as quicknode_router
from services.x402.payment import require_payment
from services.risk_service.service import evaluate_contract
from services.cache.metrics import get_cache_metrics
from shared.utils.logger import log_event

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
    payment_signature: str | None = Header(default=None, alias="PAYMENT-SIGNATURE"),
):
    require_payment(payment_signature)

    response = evaluate_contract(
        contract_address=req.contract_address,
        chain=req.chain,
        context=req.context,
    )

    log_event("risk_score_generated", {
        "contract_address": req.contract_address,
        "chain": req.chain,
        "context": req.context,
        "response": response,
    })

    return response


@app.get("/internal/cache-metrics")
def internal_cache_metrics():
    return get_cache_metrics()
