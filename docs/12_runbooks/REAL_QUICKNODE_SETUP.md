# Real QuickNode Setup Runbook v0.1

## Purpose
Safely connect QuickNode live webhook traffic to Sentinel Alpha using env-locked configuration checks.

## Required environment
- `APP_ENV=dev` (or target environment)
- `QUICKNODE_DRY_RUN=true` for first live tests
- `QUICKNODE_WEBHOOK_URL=<public webhook url>`
- `QUICKNODE_WEBHOOK_SECRET=<shared secret>`
- `PAYMENT_MODE=demo`
- `PHI_LEARNING_RATE=0.01`

## Health verification
Call:
- `GET /webhooks/quicknode/health`

Expect:
- `ok: true`
- `service: quicknode-webhook`
- `signature_verification: enabled` when secret configured
- `quicknode_env_status` with:
  - `webhook_url_configured`
  - `webhook_secret_configured`
  - `dry_run`
  - `signature_mode`

No secret values are returned by health.

## Dry run rollout
1. Configure `QUICKNODE_DRY_RUN=true`
2. Configure secret + URL
3. Send test QuickNode payloads
4. Confirm `source=quicknode` and `dry_run=true` in webhook logs
5. Keep `PAYMENT_MODE=demo` during dry run
