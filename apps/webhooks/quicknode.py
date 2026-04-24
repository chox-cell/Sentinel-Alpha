from fastapi import APIRouter, Request
from services.scout_cell.hunter import handle_new_contract
from shared.utils.logger import log_event

router = APIRouter()

@router.post("/webhooks/quicknode")
async def quicknode_webhook(req: Request):
    payload = await req.json()
    log_event("webhook_received", payload)
    result = handle_new_contract(payload)
    return {"status": "ok", "result": result}
