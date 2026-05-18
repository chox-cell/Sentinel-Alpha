# Revenue funnel — BeezShield Sentinel Alpha (internal)

**Purpose:** Convert x402scan discovery into paid API usage without overclaiming. **Not** a revenue guarantee or buyer pipeline forecast.

## Funnel stages

| Stage | Surface | Goal |
| --- | --- | --- |
| 1. Discovery | x402scan, Agentic.Market (pending), Pay.sh, Ampersend | Builder finds payable risk API |
| 2. Proof | https://beezshield.com/registry/x402scan.html | Directory registration fact + boundaries |
| 3. Website | https://beezshield.com/ | Trust, quick-start curl, npm SDK |
| 4. API probe | `POST /contracts/risk-score` (unpaid) | **402** x402 v1 challenge (body-first) |
| 5. Payment | Builder supplies `X402-PAYMENT` / demo signature | Lane-priced USDC on Base |
| 6. Value | Risk score + decision JSON | Pre-execution policy input |
| 7. Retention | SDK integration, lane upgrades, repeat scans | Habit + operational embedding |

**Public status:** `GET /public/status` · **Counters:** `GET /public/metrics` (process-lifetime; not billing truth).

## Current bottlenecks

- **Agentic.Market** not submitted (`prepared_not_submitted`).
- **Pay.sh** and **Ampersend Discover** not submitted.
- **No warehouse analytics** — metrics are in-process counters only until durable telemetry is justified.
- **Manual x402 settlement** — builders must wire payment; SDK does not auto-settle.
- **Single hero API** — expansion to more resources is roadmap, not live claim.

## First 10 buyer personas

1. **Autonomous trading / execution bot team** — needs allow/review/block before swap/contract calls.
2. **Agent framework maintainer** — wants x402-gated tool route for risk checks.
3. **Wallet automation shop** — pre-tx policy hook on Base.
4. **Security-conscious DeFi founder** — conservative signals for user-facing agents.
5. **x402 experiment builder** — testing payable APIs on Base USDC lanes.
6. **ERC-8004 agent operator** — identity + paid API composability story.
7. **MEV-aware execution desk** — boundary metadata (not live MEV prevention claim).
8. **Internal platform eng at crypto startup** — gate risky contract interactions.
9. **Agent marketplace listing owner** — cross-list after Agentic.Market live.
10. **Consulting / audit firm** — reproducible risk JSON for client agents.

## Outreach copy (claim-safe)

**Short DM**

> BeezShield Sentinel Alpha is a pre-execution risk API on Base — x402-gated, registered on x402scan as a payable resource (directory listing only). Unpaid `POST /contracts/risk-score` returns the x402 challenge; basic lane 0.02 USDC. Pre-execution policy assistance, not a security guarantee.

**Long email**

> Hi — we built **BeezShield Sentinel Alpha**, a **pre-execution decision layer** for agents that interact with onchain contracts. Before execution, your stack can call `POST https://api.beezshield.com/contracts/risk-score` on **Base** (x402, **0.02 USDC** basic lane). Unpaid calls return a standard **402** discovery body for x402 clients. We're **registered on x402scan** (discoverability only — not a partnership or endorsement). Docs: https://beezshield.com/ · proof: https://beezshield.com/registry/x402scan.html · npm `@beezshield/sentinel`. Happy to share integration notes if useful.

## Weekly metrics (measure honestly)

| Metric | Source | Notes |
| --- | --- | --- |
| x402scan listing clicks / referrals | Directory analytics if available | May be null early |
| Unpaid **402** probes | `/public/metrics` `unpaid_discovery_402_count` | Process lifetime until durable telemetry |
| Paid requests | `/public/metrics` `paid_request_count` | Same scope |
| Settlement log rows | Internal `logs/x402_settlements.jsonl` | Not exposed on public metrics |
| Agentic.Market state | `OUTREACH_TRACKER.md` | No `listed_verified` without URL |
| Website → API smoke | `scripts/public_smoke_test.py` | Config requires `PUBLIC_BASE_URL` |
| Support / integration threads | Manual tracker | Qualitative |

## Do not claim

- Official x402 integration, x402 partnership, or x402scan endorsement
- Security guarantee, certified protection, or honeypot/MEV prevention live
- Revenue, ARR, buyer count, or partnership with Agentic.Market until verified
- Automatic x402 settlement in the SDK
- x402scan registration as protocol certification
