# QUICKNODE SIGNATURE VERIFICATION v0.1

Goal:
- Reject forged webhook payloads at `/webhooks/quicknode` while preserving current webhook and risk-score schemas.

Implementation:
- `services/scout_cell/signature.py`
- `apps/webhooks/quicknode.py`

Function:
- `verify_quicknode_signature(raw_body: bytes, signature: str | None, secret: str | None) -> bool`

Rules:
- Use HMAC-SHA256.
- Signature header: `x-qn-signature`.
- Secret env var: `QUICKNODE_WEBHOOK_SECRET`.
- If secret is empty/None, treat as dev mode and allow (`True`).
- If secret exists and signature is invalid, return HTTP `401`.

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public risk response schema unchanged.
