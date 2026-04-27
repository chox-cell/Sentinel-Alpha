# API Quickstart v1.2

## Endpoint

- `POST /contracts/risk-score`

## Request Body

```json
{
  "contract_address": "0x1111111111111111111111111111111111111111",
  "chain": "base",
  "context": {}
}
```

## Demo Payment Header

Use `PAYMENT-SIGNATURE: demo` for demo mode testing.

## x402 Payment Header (Real Mode)

Use `X402-PAYMENT: tx:0x<64_hex_chars>` when real mode is enabled and guarded payment is required.

## Lane Header

Use `X-SENTINEL-LANE` to select pricing lane:
- `basic` (default)
- `executive`
- `premium`
- `priority`

Invalid lane returns `400` with `{"error":"invalid_lane"}`.

## cURL Example

```bash
curl -X POST "http://localhost:8000/contracts/risk-score" \
  -H "Content-Type: application/json" \
  -H "X-SENTINEL-LANE: priority" \
  -H "PAYMENT-SIGNATURE: demo" \
  -d '{"contract_address":"0x1111111111111111111111111111111111111111","chain":"base","context":{}}'
```

## Output Contract

Core output fields from Sentinel Alpha:
- `score`
- `confidence`
- `action`
- `emergency_signal`
- `attestation`
