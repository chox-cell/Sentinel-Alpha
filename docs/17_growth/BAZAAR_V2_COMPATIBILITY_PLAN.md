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

## Agentic.Market status

- **Not listed** until https://agentic.market/validate passes and search shows a public listing URL.
- Prior validator run (2026-05-19): failed on v1 endpoint — expected; use **v2** URL for re-validation:
  `https://api.beezshield.com/contracts/risk-score-v2`
- **No** partnership, endorsement, or security guarantee claims.

## Claim discipline

- Allowed: separate v2/Bazaar compatibility endpoint exists for indexer validation.
- Allowed: x402scan registration fact remains on v1 resource only.
- Forbidden: claiming Agentic.Market listed without verified URL; official x402 partnership; guaranteed protection.
