# REAL X402 PAYMENT + ENV LOCK v0.1

Goal:
- Add safe planning/status scaffolding for real x402 payments without enabling real settlement by default.

Implementation:
- `services/x402/payment_config.py`
- `services/x402/payment.py`
- `services/x402/coinbase.py`
- `GET /internal/x402/status`
- `GET /internal/x402/pricing`

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
