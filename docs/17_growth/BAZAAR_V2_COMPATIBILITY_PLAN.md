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

## Production verification (`62c0b1f`, 2026-05-19)

| Check | Result |
| --- | --- |
| **Deploy commit** | `62c0b1f` — HTTP `extensions.bazaar.info.input` shape |
| **POST v2 unpaid** | **HTTP 402** — `x402Version: 2`, `resource`, `accepts`, `extensions.bazaar` |
| **PAYMENT-REQUIRED** | Present; decodes to **identical** JSON as 402 body |
| **Bazaar info** | `toolName: beezshield_risk_score`; `input.type: http`, `input.method: POST`, `bodyType: json`, `body` example; `output.example` with `risk_score` / `decision` / `reasons` |
| **OpenAPI split** | `/openapi.json` → POST `/contracts/risk-score` only; `/openapi.bazaar.json` → POST `/contracts/risk-score-v2` only |
| **v1 unchanged** | POST `/contracts/risk-score` → **402**, `x402Version: 1`, body-first only; **no** `PAYMENT-REQUIRED` |

## Agentic.Market validator (`62c0b1f` production, 2026-05-19)

| Field | Value |
| --- | --- |
| **Validator URL** | https://agentic.market/validate?url=https%3A%2F%2Fapi.beezshield.com%2Fcontracts%2Frisk-score-v2&method=POST |
| **Validator UI** | **Implementation Looks Correct** — all checks pass; SDK would index; needs first verify+settle for Bazaar |
| **Screenshot** | `docs/17_growth/evidence/agentic-market-validate-v2-http-shape-pass-2026-05-19.png` |
| **Search** | https://agentic.market/?q=beezshield → **0 results** (no public listing URL) |
| **Tracker status** | **`validator_passed_not_listed`** |

Prior attempts: pre-deploy **404** (`agentic-market-validate-v2-2026-05-19.png`); SDK parse error before `62c0b1f` (`agentic-market-validate-v2-b57330a-2026-05-19.png`). v1 URL probe **Implementation Invalid** — expected; x402scan remains on v1.

## Agentic.Market status

- **Validator passed** on production v2 POST URL (not a listing claim).
- **Not listed** — no verified Agentic.Market listing URL; search **0 results**.
- **Indexing:** first real verify+settle payment required per validator UI — not claimed complete.
- **No** partnership, endorsement, certification, or security guarantee claims.

## Claim discipline

- Allowed: separate v2/Bazaar compatibility endpoint exists for indexer validation.
- Allowed: x402scan registration fact remains on v1 resource only.
- Forbidden: claiming Agentic.Market listed without verified URL; official x402 partnership; guaranteed protection.
