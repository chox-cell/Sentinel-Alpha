# CONTROLLED REAL PAYMENT TEST v0.8

Objective:
- Execute one controlled real x402 payment verification exercise on Base.

Constraints:
- Do not change `/contracts/risk-score`.
- Do not change successful response schema keys.
- Do not enable real payments by default.

Preflight:
- Run `python scripts/print_real_payment_readiness.py`
- Confirm:
  - `payment_mode`
  - `x402_enabled`
  - `onchain_verify_enabled`
  - `base_rpc_configured`
  - `treasury_configured`
  - `wallet_address_configured`
  - `pricing_tiers`
  - `readiness_verdict`

Safety:
- Never print secret values.
- Keep defaults:
  - `PAYMENT_MODE=demo`
  - `X402_ENABLED=false`
  - `X402_ONCHAIN_VERIFY=false`
