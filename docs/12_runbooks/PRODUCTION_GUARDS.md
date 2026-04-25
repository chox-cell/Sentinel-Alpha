# Production Guards v1.6

## Goal
Enable optional production hardening controls before external traffic while keeping default behavior unchanged.

## Rate Limit Guard (`/contracts/risk-score`)

Environment:
- `RATE_LIMIT_ENABLED=false` (default)
- `RATE_LIMIT_PER_MINUTE=60` (default)

Behavior:
- Applies only when enabled.
- Keyed by client IP for v1.6.
- When exceeded, `/contracts/risk-score` returns `429` with `{"error":"rate_limit_exceeded"}` in detail.

Internal status:
- `GET /internal/rate-limit/status`

## QuickNode Signature Strict Mode

Environment:
- `QUICKNODE_SIGNATURE_REQUIRED=false` (default)

Behavior:
- When `true`, `/webhooks/quicknode` rejects missing or invalid signature with `401`.
- Requires valid signature against configured `QUICKNODE_WEBHOOK_SECRET`.

Internal status:
- `GET /internal/security/status`

## Security Notes

- Status endpoints expose booleans and numeric config only.
- No secret values are returned.
