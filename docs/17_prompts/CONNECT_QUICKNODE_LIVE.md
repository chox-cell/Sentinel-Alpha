# CONNECT QUICKNODE LIVE v0.1

Goal:
- Verify live QuickNode connectivity safely using local/public test scripts and readiness checks.

Scripts:
- `scripts/check_quicknode_live_ready.py`
- `scripts/test_quicknode_webhook_local.py`
- `scripts/test_quicknode_webhook_public.py`

Behavior:
- readiness script calls `/internal/quicknode-live-check`
- exits with code `1` if `ready_for_live` is false
- local/public test scripts post sample webhook payloads
- public script reads `QUICKNODE_WEBHOOK_URL` from `.env`
- scripts avoid printing secrets

Constraints:
- Do not change `/contracts/risk-score`
- Do not change public response schema
