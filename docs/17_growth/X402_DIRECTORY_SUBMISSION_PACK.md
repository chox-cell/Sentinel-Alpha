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
| `notes` | Validators often **GET** the URL and expect **402** — see §3a. First attempt failed (GET **405**); second attempt (**GET 402** + challenge body, then **`x402Version`/`accepts`/`PAYMENT-REQUIRED`** per §3b) **still rejected** — **`status` stays `not submitted`** until a verified listing exists; **never claim listing success prematurely**. |

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
