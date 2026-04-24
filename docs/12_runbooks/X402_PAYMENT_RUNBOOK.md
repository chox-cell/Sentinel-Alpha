# X402 Payment Runbook v0.2

## Goal
Enable safe x402 payment enforcement paths without enabling live settlement.

## Modes
- Demo mode:
  - `PAYMENT_MODE=demo`
  - request must include `PAYMENT-SIGNATURE=demo` (or configured demo signature)
  - billing status: `demo`
- Real guarded mode:
  - `PAYMENT_MODE=real`
  - `X402_ENABLED=true`
  - if `X402-PAYMENT` is missing, API returns `402` with challenge payload:
    - `x402_version: "0.2"`
    - `payment_method: "x402"`
    - `network` from `X402_NETWORK`
    - `pay_to` from `X402_REVENUE_ADDRESS` or `SENTINEL_TREASURY_WALLET`
    - `amount_usdc` by lane
    - `asset: "USDC"`
    - `resource: "/contracts/risk-score"`
    - `instructions: "Submit X402-PAYMENT header to access this resource."`
  - if `X402-PAYMENT` is present, billing status is `pending_real_validation`
- Real disabled:
  - `PAYMENT_MODE=real`
  - `X402_ENABLED=false`
  - request is rejected with `402` and detail `{"error":"x402_disabled"}`

## Pricing lanes
- `basic`: `PRICE_BASIC`
- `executive`: `PRICE_EXECUTIVE`
- `premium`: `PRICE_PREMIUM`
- `priority`: `PRICE_PRIORITY`

## Internal checks
- `GET /internal/x402/status`
- `GET /internal/x402/pricing`
- `GET /internal/x402/challenge?lane=basic`

## Security notes
- Never log or return private keys or secret values.
- v0.2 does not perform Coinbase settlement.
