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
- QuickNode Event Reducer v0.1 converts large payloads into canonical candidate packets before evaluation.
- QuickNode Payload Inspector v0.1 summarizes unknown large payload structures safely.
- Candidate fan-out is capped at 50 per webhook.
- Webhook logs include:
  - `source: "quicknode"`
  - `dry_run: <bool>`
  - `payload_size_bytes`
  - `candidate_count`
  - `block_number`
- For large payloads (>100000 bytes) with zero candidates:
  - logs `quicknode_payload_inspected` with inspection summary only.

## Event reducer output
Each reduced candidate uses:
- `contract_address`
- `chain`
- `event_type`
- `transaction_hash`
- `block_number`
- `log_count`
- `context`

## Payload inspector summary
Inspection summary includes only structure metadata:
- `top_level_type`
- `top_level_keys`
- `data_type`
- `data_keys`
- `possible_list_paths`
- `receipt_count_guess`
- `log_count_guess`
- `sample_paths_only`

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
