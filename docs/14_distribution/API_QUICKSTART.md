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

## cURL Example

```bash
curl -X POST "http://localhost:8000/contracts/risk-score" \
  -H "Content-Type: application/json" \
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
