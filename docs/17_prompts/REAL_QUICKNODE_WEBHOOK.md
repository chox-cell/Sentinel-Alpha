# REAL QUICKNODE WEBHOOK DRY RUN v0.1

Goal:
- Safely prepare first live QuickNode webhook traffic with signature verification and dry-run observability.

Endpoints:
- `POST /webhooks/quicknode`
- `GET /webhooks/quicknode/health`

Health output:
- `ok`
- `service`
- `signature_verification` (`enabled` or `dev-disabled`)

Logging requirement:
- Include `source: "quicknode"` and `dry_run` in webhook log payload.

Dry run rule:
- If `QUICKNODE_DRY_RUN=true`, process webhook normally.
- Keep billing demo behavior unchanged.

Environment variables:
- `QUICKNODE_WEBHOOK_SECRET`: HMAC verification secret.
- `QUICKNODE_DRY_RUN`: boolean dry-run flag for logging/ops mode.
- `QUICKNODE_WEBHOOK_URL`: externally reachable URL configured in QuickNode.

Constraints:
- Do not change `/contracts/risk-score`.
- Do not change public risk response schema.
