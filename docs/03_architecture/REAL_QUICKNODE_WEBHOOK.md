# Real QuickNode Webhook Dry Run v0.1

## Purpose
Prepare Sentinel Alpha to receive first live QuickNode traffic safely with signature checks, dry-run observability, and unchanged public risk response schema.

## Endpoints
- `POST /webhooks/quicknode`
- `GET /webhooks/quicknode/health`

Health response:
```json
{
  "ok": true,
  "service": "quicknode-webhook",
  "signature_verification": "enabled | dev-disabled"
}
```

## Runtime behavior
- Signature verification uses `x-qn-signature` and `QUICKNODE_WEBHOOK_SECRET`.
- If `QUICKNODE_DRY_RUN=true`, webhook still processes normally.
- Billing remains demo because risk response billing mode is unchanged.
- Webhook logs include:
  - `source: "quicknode"`
  - `dry_run: <bool>`

## Environment variables
- `QUICKNODE_WEBHOOK_SECRET`
  - HMAC secret for signature verification.
  - Empty/missing means verification is dev-disabled.
- `QUICKNODE_DRY_RUN`
  - Boolean flag (`true/false`, `1/0`, `yes/no`, `on/off`) for dry-run logging mode.
- `QUICKNODE_WEBHOOK_URL`
  - Public webhook URL registered with QuickNode for incoming events.

## Constraints
- No changes to `/contracts/risk-score`.
- No changes to public risk response schema.
