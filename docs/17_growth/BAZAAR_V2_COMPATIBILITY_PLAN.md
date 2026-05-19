# Bazaar / x402 v2 compatibility plan

## Why v1 and v2 coexist

| Surface | Path | Protocol posture | Purpose |
| --- | --- | --- | --- |
| **x402scan (verified)** | `POST /contracts/risk-score` | **x402 v1** body-first — no `PAYMENT-REQUIRED` on v1 `402` | Current registered directory resource; must not change |
| **Agentic.Market / Bazaar** | `POST /contracts/risk-score-v2` | **x402 v2** — `PAYMENT-REQUIRED` header + `extensions.bazaar` | Separate discovery resource for Bazaar indexer validation |

x402scan registration remains tied to **`/contracts/risk-score`**. The v2 path is additive only.

## v2 discovery shape (summary)

- `x402Version`: **2**
- Top-level **`resource`** with `url`, `type`, `method`, `description`
- **`accepts[]`**: Base USDC exact scheme, `amount` / `payTo` / `maxTimeoutSeconds`
- **`extensions.bazaar`**: title, claim-safe description, input/output hints, JSON schema
- Unpaid **POST** returns **402** with **`PAYMENT-REQUIRED`** header and matching JSON body

## OpenAPI

| Document | Contents |
| --- | --- |
| `/openapi.json` | **POST `/contracts/risk-score` only** (x402scan filter unchanged) |
| `/openapi.bazaar.json` | **POST `/contracts/risk-score-v2` only** + `x-payment-info` |

## Agentic.Market validation record (2026-05-19)

| Field | Value |
| --- | --- |
| **Validator URL** | https://agentic.market/validate?url=https%3A%2F%2Fapi.beezshield.com%2Fcontracts%2Frisk-score-v2&method=POST |
| **Method** | POST |
| **Production probe** | `POST https://api.beezshield.com/contracts/risk-score-v2` → **HTTP 404** (v2 route not deployed to production yet) |
| **Validator UI result** | **No x402 Setup Detected** — endpoint reachable but did not return **402** (expected **402**, got **404**) |
| **Screenshot** | `docs/17_growth/evidence/agentic-market-validate-v2-2026-05-19.png` |
| **Search** | https://agentic.market/?q=beezshield → **0 results** |
| **Tracker status** | `rejected_needs_fix` (deploy v2, then re-validate) |
| **In-repo** | `tests/test_bazaar_v2_payment_required.py` passes locally — not an Agentic.Market pass claim |

Prior validator run (same day, v1 URL): **Implementation Invalid** on `…/risk-score` — expected; x402scan remains on v1.

## Agentic.Market status

- **Not listed** — no verified Agentic.Market listing URL.
- **Validator not passed** on production v2 URL until deploy returns unpaid **POST → 402** with v2 + Bazaar shape.
- **No** partnership, endorsement, certification, or security guarantee claims.

## Claim discipline

- Allowed: separate v2/Bazaar compatibility endpoint exists for indexer validation.
- Allowed: x402scan registration fact remains on v1 resource only.
- Forbidden: claiming Agentic.Market listed without verified URL; official x402 partnership; guaranteed protection.
