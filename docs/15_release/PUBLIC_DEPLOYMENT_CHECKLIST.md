# Public Deployment Checklist v2.2

Use this checklist to deploy Sentinel Alpha to a VPS/domain for public agent traffic.

## Infrastructure

- [ ] DNS configured for production domain.
- [ ] TLS certificate installed and auto-renewal enabled.
- [ ] Nginx config applied from `infra/deploy/nginx/sentinel-alpha.conf`.
- [ ] systemd service installed from `infra/deploy/systemd/sentinel-alpha.service`.

## Environment

- [ ] `.env` configured with `APP_ENV=production`.
- [ ] `PUBLIC_BASE_URL` set to public HTTPS API URL.
- [ ] `PAYMENT_MODE=real`, `X402_ENABLED=true`.
- [ ] `X402_ONCHAIN_VERIFY=true`, `X402_MOCK_ONCHAIN_VERIFY=false`.
- [ ] `BASE_RPC_URL` configured.
- [ ] `QUICKNODE_SIGNATURE_REQUIRED=true`.
- [ ] `RATE_LIMIT_ENABLED=true`.
- [ ] Agent wallet configured.
- [ ] Treasury wallet configured.

## Verification

- [ ] `python3 scripts/production_env_check.py` shows production-ready booleans.
- [ ] `python3 scripts/public_smoke_test.py` passes all endpoint checks.
- [ ] `/contracts/risk-score` without payment returns `402`.

## Safety

- [ ] No secrets are logged or committed.
- [ ] `.env` remains private.
