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
- QuickNode Event Reducer v0.2 converts large payloads into canonical candidate packets before evaluation.
- Candidate Classification v0.1 prioritizes high-value candidates before evaluation.
- QuickNode Payload Inspector v0.1 summarizes unknown large payload structures safely.
- Candidate fan-out is capped at 50 per webhook.
- Webhook logs include:
  - `source: "quicknode"`
  - `dry_run: <bool>`
  - `payload_size_bytes`
  - `candidate_count`
  - `evaluated_count`
  - `skipped_count`
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

## Candidate classification (v0.1)
- `first_liquidity` => evaluate (priority 100)
- `new_token_candidate` => evaluate (priority 90)
- transfer topic => `token_transfer`, skip by default unless force evaluate
- approval topic => `approval`, skip
- unknown => skip
- Webhook summary now reports:
  - `candidates`
  - `evaluated`
  - `skipped`
  - `results`

### matchingReceipts support (v0.2)
- Supports top-level `matchingReceipts`.
- Supports `matchingReceipts[i].logs`.
- Uses `receipt.contractAddress` (when present) as `new_token_candidate`.
- Uses each `log.address` as `contract_event` / `first_liquidity` candidate.
- Extracts transaction hash from log first, then receipt fallback.
- Extracts block number from log first, then receipt fallback.
- Priority sort: `first_liquidity` > `new_token_candidate` > high `log_count` > `contract_event`.

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
