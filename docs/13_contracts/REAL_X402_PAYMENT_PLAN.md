# Real x402 Payment Plan v0.1

## Purpose
Prepare Sentinel Alpha for future real x402/Coinbase payment enablement without turning on real payments in this phase.

## Current mode
- Default payment mode remains `demo`.
- Payment method is fixed as `x402`.

## Configuration status API
- `services/x402/payment_config.py`
- `get_payment_status() -> dict`
- internal endpoint: `GET /internal/x402/status`

## Environment inputs
- `PAYMENT_MODE` (default `demo`)
- `CDP_PROJECT_ID` (optional)
- `CDP_API_KEY_NAME` (optional)
- `CDP_API_KEY_PRIVATE_KEY` (optional)
- `SENTINEL_TREASURY_WALLET` (optional)
- `X402_NETWORK` (default `base`)

## Safety rule
- `real_payments_enabled` is true only when:
  - mode is `real`
  - CDP project configured
  - CDP API key name+private key configured
  - treasury wallet configured

## Security
- Status responses expose booleans only, never secret values.
- `/contracts/risk-score` schema remains unchanged.
