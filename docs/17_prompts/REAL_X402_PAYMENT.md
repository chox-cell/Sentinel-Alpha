# REAL X402 PAYMENT + ENV LOCK v0.7

Goal:
- Add safe planning/status scaffolding for real x402 payments without enabling real settlement by default.

Implementation:
- `services/x402/payment_config.py`
- `services/x402/payment.py`
- `services/x402/coinbase.py`
- `GET /internal/x402/status`
- `GET /internal/x402/pricing`
- `GET /internal/x402/challenge`
- `GET /internal/x402/verification/status`
- `GET /internal/x402/replay/status`
- `GET /internal/x402/settlements/status`
- `GET /internal/x402/onchain/status`

Function:
- `get_payment_status() -> dict`

Output:
- `payment_mode`
- `payment_method`
- `cdp_project_configured`
- `cdp_api_key_configured`
- `wallet_address_configured`
- `network`
- `pricing_tiers` (`basic`, `executive`, `premium`, `priority`, `default`)
- `pricing_valid`
- `real_payments_enabled`

Env alias compatibility:
- canonical: `CDP_API_KEY_NAME` + `CDP_API_KEY_PRIVATE_KEY`
- alias: `CDP_API_KEY_ID` + `CDP_API_KEY_SECRET`

Constraints:
- Do not change `/contracts/risk-score`.
- Do not change public response schema.
- Do not expose secrets in status output.

Middleware behavior v0.1:
- Add `require_x402_payment(headers: dict, lane: str = "basic") -> dict`
- `PAYMENT_MODE=demo` accepts `PAYMENT-SIGNATURE=demo`, billing status `demo`
- `PAYMENT_MODE=real` and `X402_ENABLED=false` rejects with `402`
- `PAYMENT_MODE=real` and `X402_ENABLED=true` requires `X402-PAYMENT` and returns `pending_real_validation`
- Lane pricing:
  - `basic` -> `PRICE_BASIC`
  - `executive` -> `PRICE_EXECUTIVE`
  - `premium` -> `PRICE_PREMIUM`
  - `priority` -> `PRICE_PRIORITY`

Challenge behavior v0.2:
- Add `build_x402_challenge(lane: str = "basic") -> dict`
- In real mode with `X402_ENABLED=true` and missing `X402-PAYMENT`, return `HTTP 402` with structured challenge detail
- In real mode with `X402_ENABLED=false`, return `HTTP 402` with `{"error":"x402_disabled"}`
- Challenge includes:
  - `x402_version: "0.2"`
  - `payment_method: "x402"`
  - `network`
  - `pay_to`
  - `amount_usdc`
  - `asset: "USDC"`
  - `resource: "/contracts/risk-score"`
  - `instructions`

Billing propagation v0.3:
- Payment middleware result from `require_x402_payment(...)` must override successful `/contracts/risk-score` response `billing`
- Demo success billing:
  - `method: x402`
  - `status: demo`
  - `amount` matches lane price
- Real guarded success billing (`X402-PAYMENT` present):
  - `method: x402`
  - `status: tx_format_valid_unverified`
  - `amount` matches lane price
- Missing real payment must continue returning `402` challenge payload

Real payment verification v0.4:
- `parse_x402_payment_header(header: str) -> dict`
- `verify_real_payment(payment_header: str, lane: str = "basic") -> dict`
- Accepted payment format: `tx:0x<64_hex_chars>`
- If tx hash format is valid, return:
  - `verified: false`
  - `status: tx_format_valid_unverified`
  - `reason: onchain_verification_not_enabled`
- If payment header is invalid, return `verified: false` and reject request with `402` + `{"error":"invalid_x402_payment"}`
- `X402_ONCHAIN_VERIFY=false` by default

x402 replay protection v0.5:
- Create `services/x402/replay_guard.py`
- Add:
  - `get_payment_fingerprint(payment_header: str) -> str`
  - `is_payment_replay(payment_header: str) -> bool`
  - `record_payment_fingerprint(payment_header: str, trace_id: str | None = None) -> dict`
- Store fingerprints in `logs/x402_payments.jsonl`
- Never store raw full payment header
- In `PAYMENT_MODE=real` + `X402_ENABLED=true`:
  - replayed payment header returns `402` + `{"error":"x402_replay_detected"}`
  - accepted payment records fingerprint after tx-format verification succeeds

x402 settlement logging v0.6:
- Create `services/x402/settlement_ledger.py`
- Add:
  - `write_settlement_record(record: dict) -> dict`
  - `read_settlement_records(limit: int = 50) -> list[dict]`
  - `get_settlement_status() -> dict`
- Store in `logs/x402_settlements.jsonl`
- Record includes:
  - `trace_id`
  - `tx_hash`
  - `payment_fingerprint`
  - `lane`
  - `amount`
  - `network`
  - `treasury_wallet`
  - `verification_status`
  - `created_at`
- Never store raw full `X402-PAYMENT` header

x402 on-chain USDC verification adapter v0.7:
- Create `services/x402/onchain_verifier.py`
- Constants:
  - `BASE_USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"`
  - `USDC_DECIMALS = 6`
- Add:
  - `usdc_to_units(amount: float) -> int`
  - `get_onchain_verification_status() -> dict`
  - `verify_usdc_transfer_tx(tx_hash: str, expected_amount: float, treasury_wallet: str) -> dict`
- Behavior:
  - `X402_ONCHAIN_VERIFY=false` -> `verified=false`, `status=onchain_verification_disabled`
  - `X402_ONCHAIN_VERIFY=true` and no `BASE_RPC_URL` -> `verified=false`, `status=rpc_not_configured`
  - no external calls unless both on-chain verify is enabled and RPC is configured
- In `services/x402/coinbase.py`:
  - when on-chain verify enabled, call adapter for tx proof
  - if verified true, billing status is `verified`
  - if not verified, return `402` with `{"error":"x402_payment_not_verified","status":"..."}`
- `.env`:
  - `X402_ONCHAIN_VERIFY=false`
  - `BASE_RPC_URL=`
