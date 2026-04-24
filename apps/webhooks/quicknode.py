import json
import os

from fastapi import APIRouter, HTTPException, Request
from services.scout_cell.hunter import handle_new_contract
from services.scout_cell.signature import verify_quicknode_signature
from shared.config.env import get_env_bool, get_quicknode_env_status
from shared.utils.logger import log_event

router = APIRouter()


@router.get("/webhooks/quicknode/health")
async def quicknode_webhook_health():
    status = get_quicknode_env_status()
    return {
        "ok": True,
        "service": "quicknode-webhook",
        "signature_verification": status["signature_mode"],
        "quicknode_env_status": status,
    }


@router.post("/webhooks/quicknode")
async def quicknode_webhook(req: Request):
    raw_body = await req.body()
    signature = req.headers.get("x-qn-signature")
    nonce = req.headers.get("x-qn-nonce")
    timestamp = req.headers.get("x-qn-timestamp")
    secret = os.getenv("QUICKNODE_WEBHOOK_SECRET")
    dry_run = get_env_bool("QUICKNODE_DRY_RUN", default=False)

    if not verify_quicknode_signature(raw_body, signature, secret, nonce=nonce, timestamp=timestamp):
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
            "payload_size_bytes": len(raw_body),
            "block_number": payload.get("block_number") or payload.get("blockNumber"),
        },
    )
    result = handle_new_contract(payload)
    log_event(
        "webhook_processed",
        {
            "source": "quicknode",
            "dry_run": dry_run,
            "payload_size_bytes": len(raw_body),
            "candidate_count": result.get("candidates"),
            "block_number": payload.get("block_number") or payload.get("blockNumber"),
        },
    )
    return {"status": "ok", "result": result}
