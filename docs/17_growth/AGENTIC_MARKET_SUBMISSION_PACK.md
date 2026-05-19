# Agentic.Market submission pack

**Preparation only.** This document does **not** auto-submit forms, scrape Agentic.Market, deploy, publish npm, or change API/runtime behavior. Manual submission by the owner is required.

## Status

| Field | Value |
| --- | --- |
| **Status** | **validator_passed_not_listed** (validator pass on production v2; search **0 results**; not listed) |
| **Bazaar v2 endpoint** | https://api.beezshield.com/contracts/risk-score-v2 |
| **Target** | [Agentic.Market](https://agentic.market) |
| **Submission owner** | Chox |
| **Product name** | BeezShield Sentinel Alpha |
| **Category** | agent security / risk / machine trust / x402 API |
| **Public website** | https://beezshield.com/ |
| **API endpoint** | https://api.beezshield.com/contracts/risk-score |
| **x402scan proof page** | https://beezshield.com/registry/x402scan.html |
| **x402scan listing status** | **registered** (directory listing only — not partnership or endorsement) |
| **Pricing** | Basic lane **0.02 USDC** on Base |
| **Network** | Base |
| **Asset** | USDC |
| **Package** | `@beezshield/sentinel` (`0.1.0` on npm; see https://www.npmjs.com/package/@beezshield/sentinel) |

## Submission state machine

| State | Meaning | When to set |
| --- | --- | --- |
| `prepared_not_submitted` | Copy + checklist ready; no form sent | Superseded |
| `submitted_pending` | Seller validator run; awaiting Bazaar | Superseded by v2 attempt |
| `validator_passed_not_listed` | Validator green; search has no listing | **Current** — production pass `62c0b1f`; see `BAZAAR_V2_COMPATIBILITY_PLAN.md` |
| `listed_verified` | Public listing URL captured and checked | **Only** with verified Agentic.Market URL |
| `rejected_needs_fix` | Validation failed or not deployed | Superseded (pre-`62c0b1f`) |

**Rules:** Never use `listed_verified` without a verified listing URL. No fake listing claim. x402scan remains **registered** (directory only) independent of Agentic.Market state.

## One-liner

> BeezShield Sentinel Alpha is a pre-execution risk decision API for autonomous agents, payable with x402 on Base.

## Short copy

> **BeezShield Sentinel Alpha** is **Machine Trust Infrastructure**: a **pre-execution decision layer** for autonomous agents before onchain contract interaction. The **x402-gated risk-score API** at `POST /contracts/risk-score` runs on **Base** with **USDC** lane pricing (basic **0.02 USDC**). The project is **registered on x402scan** as a **payable x402 resource** (directory discoverability only). npm: **`@beezshield/sentinel`**. BeezShield builds **guardians, not traders**.

## Long copy

> Autonomous agents should **not execute blind**. **BeezShield Sentinel Alpha** evaluates **contract risk before execution** and returns machine-readable **allow / review / block** posture for builder policy enforcement.
>
> **API:** `POST https://api.beezshield.com/contracts/risk-score` on **Base** (basic lane **0.02 USDC**; additional lanes documented on https://beezshield.com/pricing.html).
>
> **x402 paid access:** unpaid probes receive an **x402 discovery challenge**; builders supply payment/settlement explicitly. The SDK surfaces challenges — it does **not** perform automatic settlement.
>
> **x402scan directory proof:** BeezShield is **registered on x402scan** as a payable resource. Public record: https://beezshield.com/registry/x402scan.html · live resource https://api.beezshield.com/contracts/risk-score.
>
> **Website & SDK:** https://beezshield.com/ · `@beezshield/sentinel` · AgentKit-style example in-repo (not an official Coinbase AgentKit provider).
>
> **Boundaries:** This is **not** a **security guarantee**, **not** **certified protection**, and **not** an **official x402 integration**, **x402 partnership**, or **x402scan endorsement**. Directory registration on x402scan is **marketplace discoverability only**.

## Technical copy

| Field | Value |
| --- | --- |
| **Method** | `POST` |
| **URL** | `https://api.beezshield.com/contracts/risk-score` |
| **Chain** | `base` |
| **Payment** | x402-gated (v1 discovery body on unpaid POST; builders pass `X402-PAYMENT` or demo signature per environment) |
| **Basic lane header** | `X-SENTINEL-LANE: basic` |
| **Basic price** | 0.02 USDC (6-decimal atomic `20000` in discovery `accepts`) |
| **Example discovery** | `curl -s -X POST https://api.beezshield.com/contracts/risk-score` |
| **Example body (paid)** | `{"contract_address":"0x1111111111111111111111111111111111111111","chain":"base"}` |
| **OpenAPI** | `https://api.beezshield.com/openapi.json` (public filter; paid path documented as POST) |
| **Machine docs** | https://beezshield.com/llms.txt · https://beezshield.com/.well-known/x402.json |
| **ERC-8004** | https://8004scan.io/agents/base/45967 |

## Claim-safe boundaries

**Allowed**

- Prepared submission copy for Agentic.Market
- BeezShield Sentinel Alpha is **registered as a payable x402 resource on x402scan** (directory listing only)
- x402-gated API posture; pre-execution policy assistance; Machine Trust Infrastructure framing
- Base / USDC / 0.02 USDC basic lane (as documented)

**Forbidden (do not use in Agentic.Market listings or outreach)**

- official x402 integration
- x402 partnership
- x402scan endorsement
- security guarantee
- certified protection
- automatic x402 settlement live
- guaranteed protection / honeypot detection / MEV prevention claims

## Agentic.Market discovery model (2026-05-19)

- **No traditional listing form** with product name / long description fields was found on https://agentic.market.
- Seller path: **Validate Endpoint** → https://agentic.market/validate — checks x402 + **Bazaar** indexing.
- FAQ: services indexed on the **Bazaar** appear in Agentic.Market search automatically.
- Manual attempt screenshot: `docs/17_growth/evidence/agentic-market-validate-2026-05-19.png`
- Validator result (GET probe): **Implementation Invalid** (v2 resource + PAYMENT-REQUIRED header + `extensions.bazaar` expected). **Do not break x402scan v1 body-first** without a deliberate compatibility plan.

## Manual submission checklist

1. Open https://agentic.market/validate (not a copy/paste listing form — Bazaar indexer path).
2. Copy **one-liner** or **short copy** into title/summary fields; use **long copy** for description/body if character limits allow.
3. Paste **API endpoint:** `https://api.beezshield.com/contracts/risk-score`.
4. Paste **website:** `https://beezshield.com/`.
5. Paste **x402scan proof:** `https://beezshield.com/registry/x402scan.html` (state **registered** directory listing only).
6. Set **category/tags** to agent security, risk, machine trust, x402 API (as form allows).
7. Link **npm:** `https://www.npmjs.com/package/@beezshield/sentinel`.
8. Confirm **pricing** fields show Base USDC **0.02** basic lane if requested — do not change live pricing in this step.
9. Review preview for **forbidden claims** (§ Claim-safe boundaries) before submit.
10. Submit manually; capture confirmation screenshot or listing URL.
11. **Do not** mark status `submitted` or `listed` in tracker until a **verified** listing URL exists.

## Post-submit tracker update instructions

After manual submission (or if rejected):

1. Update `docs/17_growth/OUTREACH_TRACKER.md` **Agentic.Market** table row:
   - `prepared_not_submitted` → `submitted_pending` when form sent; → `listed_verified` only with verified public listing URL; → `rejected_needs_fix` on failure.
   - Set `submission_result` to confirmation text, listing URL, or rejection reason.
2. Add a dated block `## Agentic.Market directory submission — attempt (v12.x)` with evidence links (no partnership/integration claims).
3. Update `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` §7 Agentic.Market row `status` to match verified outcome.
4. Update `docs/18_investor/CLAIMS_LEDGER.md` only with **verified** listing facts — never upgrade to partnership/endorsement language.
5. If listed, optionally cross-link from `https://beezshield.com/registry/x402scan.html` or homepage **only** with directory-listing-safe copy.
