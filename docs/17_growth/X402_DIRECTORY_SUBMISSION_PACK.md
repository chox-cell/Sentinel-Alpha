# x402 Directory Submission Pack

## 2) Purpose

Prepare **truthful** submission copy for **x402 community-maintained directories**. This document is **preparation only**: it does **not** submit forms, scrape directories, deploy, publish packages, change `.env`, or imply official x402 integration, partnership, or endorsement.

## 3) Source signal

Maintainer/community response on the x402 ecosystem page PR (paraphrased posture for internal use):

- The **x402 ecosystem page** on the official repo path is being **sunset** because maintaining it is no longer scalable.
- Maintainers are **closing** ecosystem-page PRs and redirecting projects to **community-maintained** x402 directories, including:
  - **x402scan.com**
  - **Agentic.Market**
  - **Pay.sh**
  - **app.ampersend.ai/discover**
- This is a **directory redirection signal**, not a rejection of BeezShield specifically.
- This is **not** acceptance, integration, partnership, or endorsement.

## 3a) x402scan probe / GET compatibility (directory validation)

- **x402scan** (and similar tools) may validate a submitted URL with **GET** and expect **HTTP 402** plus a JSON **x402 challenge** body.
- **Observed manual attempt (2026):** registering `https://api.beezshield.com/contracts/risk-score` failed with **Error: Expected 402 response** because **GET** returned **405 Method Not Allowed** (`Allow: POST`) while **POST** with JSON + `X-SENTINEL-LANE: basic` correctly returned **402** and a challenge (`payment_method: x402`, `network: eip155:8453`, etc.).
- **Repository API behavior:** **GET `/contracts/risk-score`** returns **402** and the same challenge **shape** as an unpaid **POST** path (discovery only: **no** risk scoring, **no** required `contract_address`, **no** DB writes). **POST** behavior is unchanged for paid flows.
- **Listing claim discipline:** **Do not** claim x402scan (or any directory) **listing success** from this document. The **x402scan.com** row in §7 remains **`not submitted`** until a **verified** manual registration and listing URL are recorded in `OUTREACH_TRACKER.md`. **Listing is not claimed** until **x402scan** (or the directory UI) visibly accepts the submission and a listing URL exists.

## 3b) x402scan second attempt — schema/header compatibility hypothesis (no listing claim)

- **Observed after GET-compat deploy (2026):** public **GET** `https://api.beezshield.com/contracts/risk-score` returns **HTTP 402** with JSON including legacy fields (`x402_version`, `pay_to`, `amount_usdc`, etc.).
- **x402scan outcome:** manual **“This URL only”** registration **still failed** with **`Error: Expected 402 response`** despite **GET 402**.
- **Working hypothesis:** the directory validator may expect a **modern** wire shape (**`x402Version`**, **`accepts[]`**) and/or a **`PAYMENT-REQUIRED`** response header carrying a **compact / base64** payment-requirements payload (patterns described in Coinbase / x402-foundation-era documentation alongside HTTP 402). This repository adds those fields **as API compatibility only** — **not** an official x402 protocol certification.
- **Repository behavior:** **`GET`** and **`POST` (missing payment)** on `/contracts/risk-score` expose **legacy challenge keys** unchanged and add **`x402Version`**, **`accepts`** ( **`scheme`: `exact`**; **`network`**: **`eip155:8453`** to match `.well-known` + legacy **`network`**; **`maxAmountRequired`** in USDC **6-decimal atomic units**, e.g. `0.02` → **`20000`** ), plus **`PAYMENT-REQUIRED`** (**standard base64** over compact JSON `{"x402Version","accepts"}`) and **`Access-Control-Expose-Headers: PAYMENT-REQUIRED`** for browser-style clients behind CORS gateways.
- **Posture unchanged:** **`status`** for x402scan in §7 remains **`not submitted` / validation failed** until **verified** listing; **do not claim** submission success.

## 3c) x402scan third attempt — HEAD / OPTIONS probe hypothesis (no listing claim)

- **Observed in production diagnostics (2026, post–schema/header compat):** **GET** `https://api.beezshield.com/contracts/risk-score` returns **402** with **`PAYMENT-REQUIRED`**, legacy fields, **`x402Version`**, and **`accepts[]`** as intended; **x402scan** listing flow **still failed** with **`Error: Expected 402 response`**.
- **Additional signals:** **`HEAD`** and **`OPTIONS`** on the same path returned **405 Method Not Allowed** (e.g. `Allow:` listing **GET** only for HEAD), implying some validators may use **HEAD** and/or **browser preflight** **OPTIONS** instead of—or before—**GET**.
- **Repository behavior:** **`HEAD /contracts/risk-score`** returns **402** with the same **`PAYMENT-REQUIRED`** / **`Access-Control-Expose-Headers: PAYMENT-REQUIRED`** as **GET**, **no response body**, discovery-only (**no** scoring, **no** `contract_address`, **no** DB writes). **`OPTIONS`** returns **204** with **`Access-Control-Allow-Methods`** **`GET,HEAD,POST,OPTIONS`**, **`Access-Control-Allow-Headers`** including **`Content-Type`**, **`X-SENTINEL-LANE`**, **`X402-PAYMENT`**, **`PAYMENT-REQUIRED`**, and **`Access-Control-Expose-Headers: PAYMENT-REQUIRED`** — compatibility only for discovery/preflight, **not** a global CORS policy for other routes.
- **Posture unchanged:** **§7 x402scan** remains **`not submitted` / validation failed** until verified listing URL; **no listing success claimed** until the directory visibly accepts the row.

## 3d) x402scan fourth diagnosis — exact EVM `accepts[]` alignment (no listing claim)

- **Observed (2026, post–HEAD/OPTIONS compat):** **GET** / **HEAD** return **402** with **`PAYMENT-REQUIRED`**; **OPTIONS** returns **204** with CORS-shaped headers; **`accepts[]`** includes **`x402Version`**, **`scheme: exact`**, **`eip155:8453`**, atomic **`maxAmountRequired`**, **`payTo`**, etc. **x402scan** submission **still fails** with **`Error: Expected 402 response`**.
- **Working hypothesis:** remaining mismatch is **exact-EVM payment requirements** detail: **`accepts[0].asset`** should be the **Base mainnet USDC ERC-20 contract address** (same value as returned in live **`accepts[0].asset`**) rather than the symbol-only placeholder, plus fields such as **`amount`**, **`maxTimeoutSeconds`**, and structured **`extra`** (name/version), while **legacy** top-level **`asset: "USDC"`** stays for human readers.
- **Repository behavior (compatibility only):** **`accepts[0]`** and the **`PAYMENT-REQUIRED`** JSON use **`scheme: "exact"`**, **`network: "eip155:8453"`**, **`asset`** = Base USDC contract, **`amount`** and **`maxAmountRequired`** = same **6-decimal USDC** atomic string, **`maxTimeoutSeconds: 60`**, **`extra: { "name": "USDC", "version": "2" }`**, unchanged **`payTo`** per env. **Not** a protocol certification or listing claim.
- **Posture unchanged:** **§7 x402scan** **`not submitted`** / validation failed until verified listing; **no success claim**.

## 3e) x402scan fifth diagnosis — OpenAPI / multi-verb discovery (PATCH/PUT/DELETE) (no listing claim)

- **Evidence (2026, VPS access logs during x402scan attempt):** scanners hit **`/openapi.json`** (**200**); probed **`/contracts/risk-score`** with **GET** (and query variants) **402**, **POST** unpaid **402**, **HEAD** **402**, **OPTIONS** **204**, and **PATCH** / **PUT** / **DELETE** (**405** Method Not Allowed prior to fix).
- **Hypothesis:** validators enumerate **HTTP methods** (from OpenAPI or brute force) and expect **402 Payment Required** on the **same resource path** for discovery-shaped verbs, not only **GET**/ **POST**/ **HEAD**.
- **Repository behavior:** **PATCH**, **PUT**, and **DELETE** on **`/contracts/risk-score`** return the **same** basic-lane **402** JSON challenge and **`PAYMENT-REQUIRED`** / expose headers as **GET**, with **`include_in_schema=False`** so **OpenAPI** does **not** describe them as scoring APIs (**POST** remains the documented risk endpoint). Discovery-only (**no** scoring, **no** required body, **no** DB writes). **OPTIONS** **`Access-Control-Allow-Methods`** updated to acknowledge these verbs for preflight alignment.
- **Posture unchanged:** **§7** **`not submitted`** / validation failed; **no listing success claim**.

## 3f) x402scan sixth diagnosis — unpaid POST 422 vs prepayment gate (no listing claim)

- **Evidence (2026):** scanners reached the endpoint with **GET**/ **HEAD**/ **OPTIONS** and **PATCH**/ **PUT**/ **DELETE** behaving as **402**/ **204**, while OpenAPI correctly lists **`get`** / **`head`** / **`options`** / **`post`**. Logs still showed at least one **`POST /contracts/risk-score` → 422 Unprocessable Entity** probe.
- **Hypothesis:** the probe omitted **`X402-PAYMENT`** (or otherwise presented as unpaid) but sent **empty**, **missing**, **non-JSON**, or **schema-incomplete JSON** bodies; FastAPI/Pydantic **body validation ran before payment challenge logic**, yielding **422** instead of **402**.
- **Repository behavior:** **`POST /contracts/risk-score`** checks **payment/demo gate first** (**`PAYMENT-SIGNATURE`** in demo mode, **`X402-PAYMENT`** in real **`PAYMENT_MODE=real`** with **`X402_ENABLED`**). Unpaid probes return **402** with historical **`detail`‑wrapped** discovery challenge plus **`PAYMENT-REQUIRED`** without consuming the payload. **Paid** callers with **`X402-PAYMENT`** then receive normal **JSON parse + validation** (**422** on invalid payloads) before execution. Paid execution unchanged. **Compatibility only**.
- **Posture unchanged:** **§7** **`not submitted`** / validation failed; **no listing success claim**.

## 3g) x402scan seventh diagnosis — public OpenAPI exposed internal resources (no listing claim)

- **Evidence (2026):** **x402scan** repeatedly fetched **`GET /openapi.json`** (**200**), then probed paths discovered from that schema — including **`/internal/x402/status`**, **`/internal/x402/lanes`**, **`/internal/x402/challenge`**, **`/internal/x402/onchain/status`**, **`/internal/identity/erc8004/status`**, **`/health`**, and **`/webhooks/*`** — which return **200** or **405**, not **402**. **`/contracts/risk-score`** itself returned **402** on discovery probes.
- **Hypothesis:** validators treat **OpenAPI-listed paths** as resources to validate for **402 Payment Required**, not only the submitted marketplace URL; exposing **non-paid internal/diagnostic** routes causes **“Expected 402 response”** failures.
- **Repository behavior (compatibility only):** default **`/openapi.json`** hides **`/internal/*`**, **`/health`**, and **`/webhooks/*`** via **`include_in_schema=False`** while **runtime endpoints remain callable**. **`/contracts/risk-score`** stays documented (**`get`**, **`head`**, **`options`**, **`post`**); **PATCH** / **PUT** / **DELETE** remain **`include_in_schema=False`**. **Not** a listing or protocol certification claim.
- **Posture unchanged:** **§7** **`not submitted`** / validation failed; **no listing success claim**.

## 3h) x402scan eighth diagnosis — v1 schema (`network: base`, top-level `error`) (no listing claim)

- **Evidence (2026):** Inspected **x402scan** source/tests: v1 validators expect **`x402Version: 1`**, top-level **`error`** (e.g. **`"X-PAYMENT header is required"`**), **`accepts[]`**, and **`accepts[0].network: "base"`** (not **`eip155:8453`**). **POST** examples use **top-level** fields, not only nested **`detail`**. UI **“Expected 402 response”** is a generic fallback.
- **Repository behavior (compatibility only):** **`accepts[0].network`** → **`base`**; legacy top-level **`network`** stays **`eip155:8453`**; discovery bodies add **`error: "X-PAYMENT header is required"`**; **GET** returns flat v1 body; **POST** unpaid merges **top-level** v1 fields plus **`detail`** duplicate; **`PAYMENT-REQUIRED`** base64 includes **`error`** + **`accepts`** with **`network: base`**; **`extra.name`** → **`USD Coin`**. HTTP/OpenAPI/POST-prepayment behavior from §3e–§3g unchanged. **Not** a listing claim.
- **Posture unchanged:** **§7** **`not submitted`** / validation failed; **no listing success claim**.

## 3i) x402scan ninth diagnosis — multiple OpenAPI operations on one path (no listing claim)

- **Evidence (2026):** After v1 schema + public OpenAPI filter, **`/openapi.json`** listed only **`/contracts/risk-score`** but exposed **four operations** (**`get`**, **`head`**, **`options`**, **`post`**). **x402scan** UI showed **“Add API (4 resources)”** and still **“Expected 402 response”**. Runtime probes were correct (**GET**/**POST** unpaid **402**, **HEAD** **402** empty body, **OPTIONS** **204**, **PATCH**/**PUT**/**DELETE** **402**).
- **Hypothesis:** validators treat **each OpenAPI operation** as a separate resource; **HEAD** (no JSON body) and **OPTIONS** (**204**) are not valid payable x402 resources even when runtime compatibility is correct.
- **Repository behavior (compatibility only):** public **`/openapi.json`** documents **only `post`** on **`/contracts/risk-score`** (**`include_in_schema=False`** on **GET**/**HEAD**/**OPTIONS** discovery handlers; **PATCH**/**PUT**/**DELETE** remain hidden). Runtime methods unchanged. **POST** description documents unpaid **402** challenge. **Not** a listing claim.
- **Posture unchanged:** **§7** **`not submitted`** / validation failed; **no listing success claim**.

## 3j) x402scan tenth diagnosis — strict flat POST body (no ``detail``) (no listing claim)

- **Evidence (2026):** **x402scan** UI shows **one resource** after single-operation OpenAPI (**§3i**), but validation fails with **“No valid x402 response found (tried empty body and OpenAPI-derived sample body)”**. **GET** returns valid flat v1 JSON; **POST** unpaid previously duplicated the challenge under **`detail`**, which may fail strict POST-body validators.
- **Repository behavior (compatibility only):** unpaid **POST** returns the **same flat** **`x402Version` / `error` / `accepts`** (+ legacy keys) as **GET**, **without** a **`detail`** wrapper. OpenAPI **POST** **`example`** documents minimal **`contract_address` + `chain`**. Paid path unchanged. **Not** a listing claim.
- **Posture unchanged:** **§7** **`not submitted`** / validation failed; **no listing success claim**.

## 3k) x402scan eleventh diagnosis — pure POST v1 body (no legacy keys) (no listing claim)

- **Evidence (2026):** **One resource** detected; unpaid **POST** returns **402** with flat v1 fields and no **`detail`**, but validation still reports **“No valid x402 response found”**. **x402scan** v1 examples include only **`x402Version`**, **`error`**, **`accepts`** — extra legacy keys on **POST** may be rejected.
- **Repository behavior (compatibility only):** unpaid **POST** response and **POST** **`PAYMENT-REQUIRED`** encode **pure** v1 JSON (**three keys only**). **GET** keeps legacy + v1 fields. Paid **POST** unchanged. **Not** a listing claim.
- **Posture unchanged:** **§7** **`not submitted`** / validation failed; **no listing success claim**.

## 4) Project identity

| Field | Value |
| --- | --- |
| **Project** | BeezShield / Sentinel Alpha |
| **Category** | Pre-execution risk decision layer for autonomous agents touching onchain contracts/assets |
| **Doctrine** | BeezShield builds guardians, not traders. |
| **Website** | https://beezshield.com |
| **Manifesto** | https://beezshield.com/manifesto.html |
| **llms.txt** | https://beezshield.com/llms.txt |
| **npm** | `@beezshield/sentinel` |
| **API** | `/contracts/risk-score` |
| **x402 posture** | x402-gated API posture (builders handle payment flow explicitly; SDK does not auto-settle) |

## 5) Short submission copy

Use for directory forms with tight character limits:

> **BeezShield / Sentinel Alpha** helps builders add **allow / review / block** checks before agent onchain actions on contracts and assets. We are a **pre-execution risk decision layer**, not a trading agent. **x402-gated API posture** on `/contracts/risk-score`; npm package **`@beezshield/sentinel`**. AgentKit-style local demo and trust-loop documentation exist in-repo. **Not a security guarantee** — policy assistance and conservative signals only. BeezShield builds **guardians, not traders**.

## 6) Long submission copy

Use when a directory allows a fuller description:

> **Sentinel Alpha** (BeezShield) is a **pre-execution risk decision layer** for **autonomous agents** that interact with **onchain contracts and assets**. Before execution, builders can route agent actions through **allow / review / block** policy assistance using `/contracts/risk-score` and the **`@beezshield/sentinel`** SDK.
>
> **x402-gated API posture:** the API supports x402-style gated access patterns; **builders supply payment/settlement explicitly** — the SDK surfaces challenges and errors and does **not** perform automatic x402 settlement.
>
> **What exists today (public-safe):** website, manifesto, llms.txt, npm SDK, x402-gated API path, **AgentKit-style local demo** (in-repo; not an official Coinbase AgentKit provider), **decision receipts**, **payment decision link** boundary objects, and **trust loop** documentation/fixtures for composability discussion.
>
> **Boundaries (do not overclaim):** not official x402 integration; not x402 partnership or endorsement; not live automatic settlement; not guaranteed protection; not honeypot detection; not MEV prevention; not prompt-injection prevention. BeezShield builds **guardians, not traders**.

## 7) Directory-specific notes

### x402scan.com

| Field | Value |
| --- | --- |
| `status` | not submitted |
| `submission_owner` | Chox |
| `copy_variant` | short |
| `evidence_links` | https://beezshield.com · https://beezshield.com/manifesto.html · https://www.npmjs.com/package/@beezshield/sentinel · `docs/17_growth/SENTINEL_ALPHA_PUBLIC_TECHNICAL_SUMMARY.md` (in-repo public-safe summary) |
| `notes` | Probe timeline §3a–§3k: **pure POST v1 body** (**§3k**, three keys only on unpaid **POST**). **`status` stays `not submitted`**; **never claim listing success prematurely**. |

### Agentic.Market

| Field | Value |
| --- | --- |
| `status` | not submitted |
| `submission_owner` | Chox |
| `copy_variant` | long |
| `evidence_links` | https://beezshield.com · https://beezshield.com/manifesto.html · https://www.npmjs.com/package/@beezshield/sentinel · `docs/17_growth/SENTINEL_ALPHA_PUBLIC_TECHNICAL_SUMMARY.md` |
| `notes` | Agent/autonomous-builder angle; emphasize pre-execution policy layer, not trading bot. |

### Pay.sh

| Field | Value |
| --- | --- |
| `status` | not submitted |
| `submission_owner` | Chox |
| `copy_variant` | short |
| `evidence_links` | https://beezshield.com · https://beezshield.com/manifesto.html · https://www.npmjs.com/package/@beezshield/sentinel · `docs/17_growth/SENTINEL_ALPHA_PUBLIC_TECHNICAL_SUMMARY.md` |
| `notes` | Payment/x402-adjacent discovery; state x402-gated posture without automatic settlement claim. |

### app.ampersend.ai/discover

| Field | Value |
| --- | --- |
| `status` | not submitted |
| `submission_owner` | Chox |
| `copy_variant` | long |
| `evidence_links` | https://beezshield.com · https://beezshield.com/manifesto.html · https://www.npmjs.com/package/@beezshield/sentinel · `docs/17_growth/SENTINEL_ALPHA_PUBLIC_TECHNICAL_SUMMARY.md` |
| `notes` | Discovery listing; use long copy if form allows trust-loop / composability context. |

## 8) Safe claim controls

**Allowed**

- x402-gated API posture
- Sentinel Alpha can be used as **pre-execution policy assistance**
- SDK/package **`@beezshield/sentinel`** available on npm
- **AgentKit-style demo** exists (local/in-repo; not official AgentKit provider)
- **Trust loop** documentation exists (reference pattern; not live integrated runtime wiring)

**Forbidden**

- official x402 integration
- x402 partnership
- x402 endorsement
- automatic x402 settlement live
- guaranteed protection
- detects honeypots
- prevents MEV
- prevents prompt injection

## 9) Manual submission checklist

1. Review each directory’s current rules and required fields.
2. Paste **short** or **long** copy from §5–§6 manually (no automation from this repo).
3. Use **public links only** (website, manifesto, npm, in-repo public summary path as needed).
4. Do **not** mark `status: submitted` in this pack or `OUTREACH_TRACKER.md` until a **real** manual submission occurred.
5. Capture **submission URL** or listing ID when the directory provides one.
6. Update `docs/17_growth/OUTREACH_TRACKER.md` **only after** manual action.

## 10) Optional future cross-reference (Mycelium Trails — community signal)

Adjacent **community** builder **giskard09** indicated on the closed x402 ecosystem PR thread that **Mycelium Trails** may be submitted to the **same** community-maintained x402 directories, and that **optional cross-reference** in each project’s directory copy could happen **after both** projects have **live** directory listings.

Documentation-only posture:

- **Mycelium Trails** is an **adjacent community project** oriented toward **post-execution accountability** (execution record / trail).
- **Sentinel Alpha / BeezShield** focuses on **pre-execution decisioning** (policy assistance at the decision boundary).
- **Cross-reference** may be added **only after** both projects have **live** directory submissions (listings visible on the directory).
- **No partnership**, **no official integration**, **no endorsement**, and **no shared runtime dependency** is claimed from this note. This is **future possible** coordination on **copy** only, not a spec coupling.

## 11) Cross-references

- `docs/17_growth/OUTREACH_TRACKER.md`
- `docs/17_growth/SENTINEL_ALPHA_PUBLIC_TECHNICAL_SUMMARY.md`
- `docs/17_growth/PRE_POST_LOOP_REFERENCE_PATTERN.md`
- `docs/18_investor/CLAIMS_LEDGER.md`

This pack does not perform submissions, claim partnership, or enable integrations.
