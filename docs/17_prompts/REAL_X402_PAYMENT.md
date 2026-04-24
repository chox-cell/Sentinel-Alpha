# REAL X402 PAYMENT + ENV LOCK v0.1

Goal:
- Add safe planning/status scaffolding for real x402 payments without enabling real settlement by default.

Implementation:
- `services/x402/payment_config.py`
- `GET /internal/x402/status`

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
