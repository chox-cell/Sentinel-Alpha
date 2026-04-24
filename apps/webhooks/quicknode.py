import json
import os

from fastapi import APIRouter, HTTPException, Request
from services.scout_cell.hunter import handle_new_contract
from services.scout_cell.signature import verify_quicknode_signature
from shared.utils.logger import log_event

router = APIRouter()


def _is_truthy_env(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _signature_mode(secret: str | None) -> str:
    return "enabled" if bool((secret or "").strip()) else "dev-disabled"


@router.get("/webhooks/quicknode/health")
async def quicknode_webhook_health():
    secret = os.getenv("QUICKNODE_WEBHOOK_SECRET")
    return {
        "ok": True,
        "service": "quicknode-webhook",
        "signature_verification": _signature_mode(secret),
    }


@router.post("/webhooks/quicknode")
async def quicknode_webhook(req: Request):
    raw_body = await req.body()
    signature = req.headers.get("x-qn-signature")
    secret = os.getenv("QUICKNODE_WEBHOOK_SECRET")
    dry_run = _is_truthy_env(os.getenv("QUICKNODE_DRY_RUN"))

    if not verify_quicknode_signature(raw_body, signature, secret):
        raise HTTPException(status_code=401, detail="Invalid QuickNode signature")

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from exc

    log_event(
        "webhook_received",
        {
            "source": "quicknode",
            "dry_run": dry_run,
            "payload": payload,
        },
    )
    result = handle_new_contract(payload)
    return {"status": "ok", "result": result}
