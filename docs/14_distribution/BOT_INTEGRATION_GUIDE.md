# Bot Integration Guide v1.2

## Positioning

Sentinel Alpha is an execution fidelity layer for bots and agents. Integrate it before order execution to turn on-chain risk signals into machine actions.

## Integration Flow

1. Build request payload with `contract_address`, `chain`, and optional `context`.
2. Call `POST /contracts/risk-score`.
3. Provide payment header:
   - Demo: `PAYMENT-SIGNATURE: demo`
   - x402: `X402-PAYMENT: tx:0x<64_hex_chars>`
4. Use response fields (`score`, `confidence`, `action`, `emergency_signal`, `attestation`) to gate execution.

## Network and Payment

- Supported chain for this launch: `base`
- x402 network: `eip155:8453`
- Asset: USDC

Pricing tiers:
- `basic`: `0.02`
- `executive`: `0.05`
- `premium`: `0.10`
- `priority`: `0.15`

## SDKs

- Python: `sdk/python/client.py`
- TypeScript stub: `sdk/typescript/client.ts`

## Launch Safety

Run a controlled real payment test before production launch to verify billing and on-chain verification paths for your environment.
