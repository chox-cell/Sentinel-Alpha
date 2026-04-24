# QuickNode Signature Verification v0.1

## Purpose
Protect `/webhooks/quicknode` from fake payloads using HMAC-SHA256 before enabling live QuickNode traffic.

## Module
- `services/scout_cell/signature.py`

## Function
- `verify_quicknode_signature(raw_body: bytes, signature: str | None, secret: str | None) -> bool`

## Rules
- Uses HMAC-SHA256 over the raw request body.
- Reads signature from header: `x-qn-signature`.
- Reads secret from environment: `QUICKNODE_WEBHOOK_SECRET`.
- Supports dry-run ops flag: `QUICKNODE_DRY_RUN`.
- Supports deployment URL registration var: `QUICKNODE_WEBHOOK_URL`.
- If secret is empty or missing, verification is disabled and returns `True` (dev mode).

## Webhook integration
- `apps/webhooks/quicknode.py` reads `await req.body()`.
- Verifies signature before JSON parse and processing.
- Returns HTTP `401` when verification fails.
- Successful shape remains: `{"status":"ok","result":...}`.
