# API integration copy blocks (public-safe)

Use for outreach, docs, and directory forms. **Pre-execution decision layer** — not guaranteed protection.

## Agent builders

**Short DM:** Sentinel Alpha returns allow/review/block before your agent touches a contract. `POST /contracts/risk-score` on Base, x402 basic **0.02 USDC**. Registered on x402scan (directory only).

**Long email:** See `REVENUE_FUNNEL.md` long email template.

**Technical snippet:**

```bash
curl -s -X POST https://api.beezshield.com/contracts/risk-score | jq .
# Paid:
curl -s -X POST https://api.beezshield.com/contracts/risk-score \
  -H "Content-Type: application/json" \
  -H "X-SENTINEL-LANE: basic" \
  -H "X402-PAYMENT: tx:<YOUR_TX_HASH>" \
  -d '{"contract_address":"0x...","chain":"base"}'
```

## Wallet automation teams

**Short DM:** Hook a pre-execution risk gate into your send pipeline on Base. x402-gated API; builders handle settlement explicitly.

**Long email:** BeezShield helps wallet automation teams pause or review transactions when contract risk scores exceed policy. Integrate via `@beezshield/sentinel` or direct HTTP. Not a custody or guarantee product.

**Technical snippet:** `GET https://api.beezshield.com/public/status` for integration posture (no secrets).

## x402 ecosystem

**Short DM:** Payable x402 resource on Base — risk-score API registered on x402scan (listing only, not endorsement).

**Long email:** Sentinel Alpha exposes pure v1 **402** discovery on unpaid POST. Directory registration on x402scan is live; we do not claim official protocol certification.

**Technical snippet:** Unpaid POST body: `x402Version`, `error`, `accepts` only (v1 body-first; no `PAYMENT-REQUIRED` header on v1).

## Base builders

**Short DM:** Machine Trust Infrastructure on Base — USDC lane pricing, ERC-8004 identity public, npm SDK live.

**Long email:** Base-native contract risk scoring for agents. Basic lane **0.02 USDC**. Explore https://beezshield.com/pricing.html for lanes.

**Technical snippet:** `"chain": "base"` in request body; network slug `base` in discovery `accepts`.

## Security-conscious founders

**Short DM:** Policy assistance before autonomous execution — conservative signals, explicit payment, no security guarantee wording.

**Long email:** BeezShield provides **risk signals** to support human or agent policy. Outcomes are not guaranteed. Suitable for teams that want a **guardian layer**, not a trading bot.

**Technical snippet:** Read `decision` + `risk_metrics` from paid 200 response; enforce `shouldExecute` in your agent runtime.

## Claim-safe footer (all channels)

> BeezShield builds pre-execution risk decision tools for agents. Directory registration on x402scan is discoverability only. Not a security guarantee, not an x402 partnership, not an endorsement.
