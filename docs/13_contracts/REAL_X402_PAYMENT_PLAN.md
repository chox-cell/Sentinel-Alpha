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
- internal endpoint: `GET /internal/x402/pricing`
- internal endpoint: `GET /internal/x402/challenge?lane=basic`
- internal endpoint: `GET /internal/x402/verification/status`

## Environment inputs
- `PAYMENT_MODE` (default `demo`)
- `X402_ENABLED` (default `false`)
- `CDP_PROJECT_ID` (optional)
- `CDP_API_KEY_NAME` (optional)
- `CDP_API_KEY_PRIVATE_KEY` (optional)
- Alias pair supported:
  - `CDP_API_KEY_ID`
  - `CDP_API_KEY_SECRET`
- `SENTINEL_TREASURY_WALLET` (optional)
- `X402_NETWORK` (default `base`)
- `X402_ONCHAIN_VERIFY` (default `false`)
- `BASE_RPC_URL` (optional)
- Pricing env:
  - `PRICE_BASIC` (default `0.02`)
  - `PRICE_EXECUTIVE` (default `0.05`)
  - `PRICE_PREMIUM` (default `0.10`)
  - `PRICE_PRIORITY` (default `0.15`)
  - `X402_DEFAULT_PRICE_USDC` (default `0.05`)

## Safety rule
- `real_payments_enabled` is true only when:
  - mode is `real`
  - CDP project configured
  - CDP API key configured (canonical or alias pair)
  - treasury wallet configured
  - pricing tiers valid

Pricing validity rule:
- all prices > 0
- `basic <= executive <= premium <= priority`

## Security
- Status responses expose booleans only, never secret values.
- `/contracts/risk-score` schema remains unchanged.

## Real Payment Middleware v0.1
- `services/x402/payment.py`
- `services/x402/coinbase.py`
- `require_x402_payment(headers: dict, lane: str = "basic") -> dict`

Behavior:
- Demo mode (`PAYMENT_MODE=demo`):
  - accepts `PAYMENT-SIGNATURE=demo` (or configured demo signature)
  - returns billing status `demo`
- Real mode disabled (`PAYMENT_MODE=real`, `X402_ENABLED=false`):
  - rejects with `402`
- Real mode guarded (`PAYMENT_MODE=real`, `X402_ENABLED=true`):
  - requires `X402-PAYMENT` header
  - performs placeholder validation in v0.1 only
  - returns billing status `pending_real_validation`

Lane pricing mapping:
- `basic` -> `PRICE_BASIC`
- `executive` -> `PRICE_EXECUTIVE`
- `premium` -> `PRICE_PREMIUM`
- `priority` -> `PRICE_PRIORITY`

Settlement:
- No live Coinbase settlement is executed in v0.1.

## Real Payment Challenge v0.2
- `services/x402/payment.py`
- `build_x402_challenge(lane: str = "basic") -> dict`

When `PAYMENT_MODE=real` and `X402_ENABLED=true`:
- missing `X402-PAYMENT` returns `HTTP 402` with challenge payload

Challenge payload:
- `x402_version: "0.2"`
- `payment_method: "x402"`
- `network` from `X402_NETWORK`
- `pay_to` from `X402_REVENUE_ADDRESS` or `SENTINEL_TREASURY_WALLET`
- `amount_usdc` from lane pricing
- `asset: "USDC"`
- `resource: "/contracts/risk-score"`
- `instructions: "Submit X402-PAYMENT header to access this resource."`

When `PAYMENT_MODE=real` and `X402_ENABLED=false`:
- return `HTTP 402` with `{"error":"x402_disabled"}`

## Real Payment Verification v0.4
- `services/x402/coinbase.py`
- `parse_x402_payment_header(header: str) -> dict`
- `verify_real_payment(payment_header: str, lane: str = "basic") -> dict`

Accepted format:
- `X402-PAYMENT: tx:0xTRANSACTION_HASH`
- tx hash must start with `0x` and be length 66

v0.4 verification behavior:
- parse tx hash
- validate tx hash shape only
- if valid shape, return:
  - `verified: false`
  - `status: tx_format_valid_unverified`
  - `reason: onchain_verification_not_enabled`
- if invalid header, return `verified: false` with invalid reason

Runtime behavior:
- `PAYMENT_MODE=real`, `X402_ENABLED=true`, missing header: `402` challenge
- `PAYMENT_MODE=real`, `X402_ENABLED=true`, invalid header: `402` + `{"error":"invalid_x402_payment"}`
- `PAYMENT_MODE=real`, `X402_ENABLED=true`, valid tx format: request allowed with billing status `tx_format_valid_unverified`

## On-chain USDC Verification Adapter v0.7
- `services/x402/onchain_verifier.py`
- constants:
  - `BASE_USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"`
  - `USDC_DECIMALS = 6`
- functions:
  - `usdc_to_units(amount: float) -> int`
  - `get_onchain_verification_status() -> dict`
  - `verify_usdc_transfer_tx(tx_hash: str, expected_amount: float, treasury_wallet: str) -> dict`

Adapter safety:
- if `X402_ONCHAIN_VERIFY=false`: `verified=false`, `status=onchain_verification_disabled`
- if enabled but no `BASE_RPC_URL`: `verified=false`, `status=rpc_not_configured`
- no external RPC calls unless both on-chain verify is enabled and RPC is configured

Validation:
- tx hash must be `0x` + 64 hex chars
- treasury wallet must be valid `0x` address
- expected amount must be greater than zero
