# Pre-Launch Checklist v1.2

Use this checklist before public launch to bot builders and agent marketplaces.

## Product and API

- [ ] `POST /contracts/risk-score` reachable in target environment.
- [ ] API returns expected machine outputs: `score`, `confidence`, `action`, `emergency_signal`, `attestation`.
- [ ] No public response schema regressions from baseline contract.

## Payment and Network

- [ ] x402 header flow validated (`X402-PAYMENT: tx:0x<64_hex_chars>` in real mode).
- [ ] Demo payment flow validated for local testing (`PAYMENT-SIGNATURE: demo`).
- [ ] Base network config validated (`eip155:8453`).
- [ ] Pricing tiers communicated: basic `0.02`, executive `0.05`, premium `0.10`, priority `0.15`.

## SDK and Docs

- [ ] Python SDK quickstart verified (`sdk/python/README.md` and example).
- [ ] TypeScript SDK stub quickstart verified (`sdk/typescript/README.md` and client).
- [ ] Public docs published:
  - `README.md`
  - `docs/14_distribution/API_QUICKSTART.md`
  - `docs/14_distribution/BOT_INTEGRATION_GUIDE.md`
  - `docs/14_distribution/SDK_QUICKSTART.md`
  - `docs/14_distribution/AGENTIC_MARKET_LISTING.md`

## Safety

- [ ] Real payment test completed before launch.
- [ ] No secrets are present in docs or manifests.
