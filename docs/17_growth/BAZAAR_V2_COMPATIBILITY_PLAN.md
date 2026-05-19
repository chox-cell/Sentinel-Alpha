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

## Production verification (commit `b57330a`, 2026-05-19)

| Check | Result |
| --- | --- |
| **Git** | `b57330a` on `origin/main` (pushed) |
| **POST v2 unpaid** | **HTTP 402** — `x402Version: 2`, `resource`, `accepts`, `extensions.bazaar` |
| **PAYMENT-REQUIRED** | Present; base64 decodes to **identical** JSON as 402 body |
| **Bazaar info fields** | `toolName`, `method`, `output.example` present on production |
| **OpenAPI split** | `/openapi.json` → POST `/contracts/risk-score` only; `/openapi.bazaar.json` → POST `/contracts/risk-score-v2` only |
| **v1 unchanged** | POST `/contracts/risk-score` → **402**, `x402Version: 1`, keys `x402Version`/`error`/`accepts` only; **no** `PAYMENT-REQUIRED` |

## Agentic.Market validator (post-deploy, 2026-05-19)

| Field | Value |
| --- | --- |
| **Validator URL** | https://agentic.market/validate?url=https%3A%2F%2Fapi.beezshield.com%2Fcontracts%2Frisk-score-v2&method=POST |
| **Validator UI (b57330a)** | **Implementation Invalid** — **SDK Parse Error:** failed to extract method/toolName from discovery info |
| **Screenshot (pre-fix)** | `docs/17_growth/evidence/agentic-market-validate-v2-b57330a-2026-05-19.png` |
| **In-repo fix** | `info.input` HTTP shape (`type`/`method`/`bodyType`/`body`) — re-validate on production after deploy |
| **Search** | https://agentic.market/?q=beezshield → **0 results** (no listing URL) |
| **Tracker status** | `rejected_needs_fix` until Agentic.Market validator passes; then `validator_passed_not_listed` if search still empty |

Earlier same-day attempt (pre-deploy): **404** / **No x402 Setup Detected** — `docs/17_growth/evidence/agentic-market-validate-v2-2026-05-19.png`.

Prior v1 URL probe: **Implementation Invalid** — expected; x402scan remains on v1.

## Agentic.Market status

- **Not listed** — no verified Agentic.Market listing URL.
- **Production v2 live** for x402 transport checks; **validator not passed** (SDK discovery parse).
- **No** partnership, endorsement, certification, or security guarantee claims.

## Claim discipline

- Allowed: separate v2/Bazaar compatibility endpoint exists for indexer validation.
- Allowed: x402scan registration fact remains on v1 resource only.
- Forbidden: claiming Agentic.Market listed without verified URL; official x402 partnership; guaranteed protection.
