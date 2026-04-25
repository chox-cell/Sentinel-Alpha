# X402 Payment Runbook v0.9.1

## Goal
Enable safe x402 payment enforcement paths without enabling live settlement.

## Modes
- Demo mode:
  - `PAYMENT_MODE=demo`
  - request must include `PAYMENT-SIGNATURE=demo` (or configured demo signature)
  - billing status: `demo`
  - successful `/contracts/risk-score` response billing is overridden from payment middleware result
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
  - supported header format: `X402-PAYMENT: tx:0x<64_hex_chars>`
  - invalid payment header returns `402` with `{"error":"invalid_x402_payment"}`
  - valid tx-format header returns billing status `tx_format_valid_unverified`
  - verification result reason: `onchain_verification_not_enabled`
  - if `X402_ONCHAIN_VERIFY=true`, tx proof is verified on Base via JSON-RPC `eth_getTransactionReceipt` (`BASE_RPC_URL`, timeout ≤ 8s): receipt success, USDC contract log, ERC-20 `Transfer` to treasury, amount ≥ lane price in USDC units
  - if on-chain verification fails, request returns `402` with `{"error":"x402_payment_not_verified","status":"..."}` (e.g. `receipt_not_found`, `tx_failed`, `no_matching_usdc_transfer`, `amount_too_low`, `rpc_error`)
  - if on-chain verification succeeds, billing status becomes `verified`
  - replayed tx proof returns `402` with `{"error":"x402_replay_detected"}`
  - accepted tx proof appends settlement ledger entry in `logs/x402_settlements.jsonl`
  - successful `/contracts/risk-score` response billing is overridden from payment middleware result
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
- `GET /internal/x402/verification/status`
- `GET /internal/x402/replay/status`
- `GET /internal/x402/settlements/status`
- `GET /internal/x402/onchain/status`

## Security notes
- Never log or return private keys or secret values.
- v0.9 does not perform irreversible settlement actions beyond receipt checks.
- `X402_ONCHAIN_VERIFY` defaults to `false`; set `true` plus `BASE_RPC_URL` for Base USDC receipt verification (v0.9).
- `X402_MOCK_ONCHAIN_VERIFY` defaults to `false`; when set `true` together with `X402_ONCHAIN_VERIFY=true`, valid tx-shaped proof is accepted in safe local mock mode and billing can reach `verified` without real RPC.
- Never log or return `BASE_RPC_URL` in API or status payloads.
- `BASE_RPC_URL` is optional and used only when `X402_ONCHAIN_VERIFY=true`.
- Replay fingerprints are stored in `logs/x402_payments.jsonl` and never include raw payment headers.
- Settlement records are append-only in `logs/x402_settlements.jsonl` and never include raw payment headers.
- Successful response schema keys are unchanged; only `billing` values are updated by payment mode.
