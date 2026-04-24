# Controlled Real Payment Test v0.8

## Goal
Run one controlled real-payment verification exercise on Base without changing default behavior or enabling real payments globally.

## Safety defaults
- `PAYMENT_MODE` default remains `demo`
- `X402_ENABLED` default remains `false`
- `X402_ONCHAIN_VERIFY` default remains `false`
- No irreversible settlement behavior is enabled by default

## Pre-check
Run:
- `python scripts/print_real_payment_readiness.py`

The script reports:
- `env_source` (`.env`)
- `payment_mode`
- `x402_enabled`
- `onchain_verify_enabled`
- `base_rpc_configured`
- `treasury_configured`
- `wallet_address_configured`
- `pricing_tiers`
- `readiness_verdict`

It does not print secret values.
It loads repo-root `.env` with override behavior, so `.env` is the source of truth even if shell vars differ.

The API process uses the same rule: `apps/api/main.py` loads repo-root `.env` with `override=True` before other app imports, so runtime matches the readiness script. Check alignment with `GET /internal/env/source` (fields: `env_source`, `override`, `app_env`, `payment_mode`, `x402_enabled`) and compare `payment_mode` to `GET /internal/x402/status`.

## Controlled test steps
1. Set scoped environment for a single test session.
2. Enable:
   - `PAYMENT_MODE=real`
   - `X402_ENABLED=true`
   - `X402_ONCHAIN_VERIFY=true`
3. Configure non-empty:
   - `BASE_RPC_URL`
   - treasury wallet (`X402_REVENUE_ADDRESS` or `SENTINEL_TREASURY_WALLET`)
4. Submit one tx-shaped payment header:
   - `X402-PAYMENT: tx:0x...`
5. Observe:
   - billing status response
   - replay guard behavior on repeat attempt
   - settlement and replay internal status endpoints

## Rollback
- Restore env to safe defaults:
  - `PAYMENT_MODE=demo`
  - `X402_ENABLED=false`
  - `X402_ONCHAIN_VERIFY=false`
