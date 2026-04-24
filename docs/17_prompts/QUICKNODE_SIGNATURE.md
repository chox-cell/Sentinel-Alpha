# QUICKNODE SIGNATURE VERIFICATION v0.2

Goal:
- Reject forged webhook payloads at `/webhooks/quicknode` while preserving current webhook and risk-score schemas.

Implementation:
- `services/scout_cell/signature.py`
- `apps/webhooks/quicknode.py`

Function:
- `verify_quicknode_signature(raw_body: bytes, signature: str | None, secret: str | None, nonce: str | None = None, timestamp: str | None = None) -> bool`

Rules:
- Use HMAC-SHA256.
- Signature header: `x-qn-signature`.
- Optional QuickNode headers:
  - `x-qn-nonce`
  - `x-qn-timestamp`
- Secret env var: `QUICKNODE_WEBHOOK_SECRET`.
- Dry-run env var: `QUICKNODE_DRY_RUN`.
- Webhook URL env var: `QUICKNODE_WEBHOOK_URL`.
- If secret is empty/None, treat as dev mode and allow (`True`).
- If secret exists and signature is invalid, return HTTP `401`.
- Compatibility payload candidates:
  - `raw_body`
  - `timestamp + nonce + raw_body`
  - `nonce + timestamp + raw_body`
  - `timestamp + raw_body`
- Use timing-safe comparison and debug-safe mismatch logs (no secrets).

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public risk response schema unchanged.
