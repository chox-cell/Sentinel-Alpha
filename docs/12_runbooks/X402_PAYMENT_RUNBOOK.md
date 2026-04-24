# X402 Payment Runbook v0.1

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
  - request must include `X402-PAYMENT`
  - billing status: `pending_real_validation`
- Real disabled:
  - `PAYMENT_MODE=real`
  - `X402_ENABLED=false`
  - request is rejected with `402`

## Pricing lanes
- `basic`: `PRICE_BASIC`
- `executive`: `PRICE_EXECUTIVE`
- `premium`: `PRICE_PREMIUM`
- `priority`: `PRICE_PRIORITY`

## Internal checks
- `GET /internal/x402/status`
- `GET /internal/x402/pricing`

## Security notes
- Never log or return private keys or secret values.
- v0.1 does not perform Coinbase settlement.
