# QuickNode Live Checklist v0.1

## Purpose
Safely move from dry-run webhook ingestion to live QuickNode traffic while keeping API schema and payment mode stable.

## Required environment
- `QUICKNODE_WEBHOOK_URL` set to public HTTPS endpoint
- `QUICKNODE_WEBHOOK_SECRET` set to shared signing secret
- `QUICKNODE_DRY_RUN=false` for live mode
- `QUICKNODE_CHAIN=base`
- `PAYMENT_MODE=demo` (no real payment enablement yet)

## Internal readiness check
Call:
- `GET /internal/quicknode-live-check`

Expected response shape:
```json
{
  "ready_for_live": true,
  "checks": {
    "webhook_url_configured": true,
    "webhook_secret_configured": true,
    "dry_run": false,
    "chain": "base"
  }
}
```

Readiness rule:
- `ready_for_live=true` only when:
  - URL configured
  - secret configured
  - dry_run is false

## Safety notes
- Health and live-check endpoints never expose secret values.
- `/contracts/risk-score` schema remains unchanged.
