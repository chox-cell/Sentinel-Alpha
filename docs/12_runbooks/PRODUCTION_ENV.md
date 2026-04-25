# Production Environment v2.1

Required production environment settings:

- `APP_ENV=production`
- `PUBLIC_BASE_URL=<https public URL>`
- `PAYMENT_MODE=real`
- `X402_ENABLED=true`
- `X402_MOCK_ONCHAIN_VERIFY=false`
- `X402_ONCHAIN_VERIFY=true`
- `BASE_RPC_URL=<configured>`
- `QUICKNODE_SIGNATURE_REQUIRED=true`
- `RATE_LIMIT_ENABLED=true`
- `RATE_LIMIT_PER_MINUTE=60` (or tighter)
- `AGENT_WALLET_ADDRESS=<configured>`
- `SENTINEL_TREASURY_WALLET=<configured>` (or `X402_REVENUE_ADDRESS`)

Validation command:

```bash
python3 scripts/production_env_check.py
```

The checker prints boolean readiness only and does not print secret values.
