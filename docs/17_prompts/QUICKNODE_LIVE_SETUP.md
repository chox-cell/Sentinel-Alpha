# QUICKNODE LIVE SETUP v0.1

Goal:
- Prepare Sentinel Alpha for real QuickNode webhook traffic using environment checks and public URL readiness, without changing risk-score schema.

Required env:
- `QUICKNODE_DRY_RUN`
- `QUICKNODE_WEBHOOK_URL`
- `QUICKNODE_WEBHOOK_SECRET`
- `QUICKNODE_CHAIN`

Internal check endpoint:
- `GET /internal/quicknode-live-check`

Output contract:
- `ready_for_live: bool`
- `checks`:
  - `webhook_url_configured`
  - `webhook_secret_configured`
  - `dry_run`
  - `chain`

Ready rule:
- true only when url configured, secret configured, and dry_run is false.

Constraints:
- Keep `/contracts/risk-score` unchanged.
- Keep public response schema unchanged.
- Do not expose secret values.
