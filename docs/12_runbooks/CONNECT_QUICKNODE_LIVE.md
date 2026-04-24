# Connect QuickNode Live v0.1

## Purpose
Provide a safe operational checklist to connect QuickNode live traffic to Sentinel Alpha through ngrok/public URL.

## Preconditions
- Sentinel Alpha API running locally (`http://127.0.0.1:8000`)
- `.env` configured:
  - `QUICKNODE_WEBHOOK_URL`
  - `QUICKNODE_WEBHOOK_SECRET`
  - `QUICKNODE_DRY_RUN`
  - `QUICKNODE_CHAIN`

## Steps
1. Validate readiness:
   - `python scripts/check_quicknode_live_ready.py`
2. Test local webhook path:
   - `python scripts/test_quicknode_webhook_local.py`
3. Test public/ngrok webhook URL:
   - `python scripts/test_quicknode_webhook_public.py`
4. Confirm webhook health:
   - `GET /webhooks/quicknode/health`

## Safety constraints
- Keep `/contracts/risk-score` unchanged.
- Keep public risk response schema unchanged.
- Keep payment mode as demo during dry-run and initial live checks.
- Do not print or expose secret values.
