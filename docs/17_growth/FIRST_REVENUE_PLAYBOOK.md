# First revenue playbook — Trust Receipt paid pilot (minimal)

**Goal:** First revenue from **direct buyer/operator** pilots. **Do not** build broad product features — intake schema, sample deliverable, outbound copy, and manual fulfillment only.

**Related:** `TRUST_RECEIPT_CHECKOUT_V0.md` · `TRUST_RECEIPT_PILOT_INTAKE_SCHEMA.md` · `TRUST_RECEIPT_PILOT_PACK.md` · `TRUST_RECEIPT_V0_SPEC.md` · `apps/website/pilot/trust-receipt.html`

---

## 0) Checkout v0 (semi-automated)

**Pay for Pilot** on the website (`#payForPilot`):

1. Choose tier (**$25** / **$50** / **$250**).
2. Send **USDC on Base** to the **manual pilot payment address** (`0x3cf9C2E55485fF8DAFfb59c84a0fa7c03bDbAeaf` — public x402 treasury).
3. Submit contact + **`payment_tx_hash`** + redacted action intake (copy checkout JSON).
4. BeezShield **manually verifies** payment → delivers JSON + Markdown receipt.

**Not included:** Stripe, escrow, smart-contract checkout, automated fulfillment, or revenue claims before tx confirmation. See `TRUST_RECEIPT_CHECKOUT_V0.md`.

---

## 1) Offer

**Trust Receipt paid pilot** — one redacted autonomous action:

1. Buyer submits intake (one action, redacted refs, optional post-execution ref).
2. BeezShield runs Sentinel pre-check + binds post-action ref when provided.
3. Buyer receives **JSON Trust Receipt v0** + **Markdown receipt** (human-readable summary).

**Not included in v0:** on-site payment automation, SLA security guarantee, official AgentKit/x402 partnership claims.

---

## 2) Price tiers

| Tier | Price (USDC, one-time) | Best for |
| --- | --- | --- |
| **Draft review** | **$25** | Single-action boundary review; lighter deliverable |
| **Operator pilot** (default CTA) | **$50** | Standard Trust Receipt v0 JSON + Markdown for one AgentKit-style run |
| **Integration sprint** | **$250** | Deeper integration notes + custom client wiring guidance (still one primary receipt run unless SOW states otherwise) |

Payment: **checkout v0** — USDC on Base to manual pilot payment address + tx hash intake; operator verifies before minting receipt. **Not** escrow; **not** automated delivery.

---

## 3) ICPs (ideal customer profiles)

1. **Agent operator on Base** — runs one contract interaction via AgentKit-style stack; wants pre-check + receipt artifact.
2. **Autonomous trading / bot team** — needs allow/review/block paper trail for one staging action.
3. **Agent framework maintainer** — evaluating x402 + Sentinel + receipt binder for a demo path.
4. **Wallet automation shop** — policy hook before user-facing agent step.
5. **Security-conscious DeFi founder** — falsifiable receipt for investor or internal review.

**Disqualify:** requests for guarantee wording, raw key/calldata submission, or “official Coinbase partnership” framing.

---

## 4) Outbound message (claim-safe)

**Subject:** Trust Receipt pilot — one redacted action, JSON + Markdown

> Hi — we run **paid Trust Receipt pilots** for teams testing **pre-execution Sentinel risk** on a single **redacted** agent action (Base / AgentKit-style workflows).
>
> **$50 operator pilot:** you send one redacted proposed action (+ optional post-execution ref); we return **Trust Receipt v0 JSON + Markdown** with checked/not-checked boundaries. **Not** a security guarantee or official AgentKit/x402 endorsement. Payment is manual USDC on Base after scope confirm.
>
> Pilot page: https://beezshield.com/pilot/trust-receipt.html  
> API discovery: https://beezshield.com/registry/x402scan.html

---

## 5) Qualification rules

| Rule | Pass | Fail |
| --- | --- | --- |
| Single scoped action | One `proposed_action_summary` | Open-ended audit / unlimited contracts |
| Redaction | `contract_or_tool_ref_redacted` hash/alias only | Raw addresses, calldata, keys, `.env` |
| Chain stated | `chain` field set | “any chain” without scope |
| Payment realism | Accepts manual USDC / invoice | Demands automated checkout day one |
| Claims | Accepts disclaimer boundaries | Requires “safe to execute” or partnership copy |

---

## 6) Claim boundaries

**Allowed**

- “We offer paid Trust Receipt pilots for one redacted action.”
- “Deliverable is JSON + Markdown receipt per `TRUST_RECEIPT_V0_SPEC.md`.”
- “Pre-execution policy assistance; explicit not-checked list.”

**Forbidden (until independently verified)**

- First revenue achieved / revenue confirmed (until payment settled and recorded)
- Paid customer / pilot sold (until SOW + payment)
- Official partnership, integration, or endorsement (AgentKit, Coinbase, x402, Mycelium, AURA)
- Security guarantee, execution-quality proof, honeypot/MEV prevention claims

---

## 7) Conversion metric table

| Metric | Definition | Source | Notes |
| --- | --- | --- | --- |
| Pilot page views | Unique loads of pilot HTML | Hosting analytics if available | May be null early |
| Intake started | Form interaction or email reply | Manual / form events | Not billing truth |
| Qualified lead | Passes §5 rules | Operator tag | |
| SOW sent | Scope + tier agreed | CRM / email | |
| Checkout JSON submitted | Buyer copies `trust-receipt-checkout-v0` | Pilot page / email | Includes `payment_tx_hash`; not revenue yet |
| Payment confirmed | Operator verifies USDC tx on Base | Treasury log | **Only then** consider revenue internal flag |
| Receipt delivered | JSON + Markdown sent | `pilot_run_id` folder | |
| Repeat pilot | Second paid intake | Operator | Expansion signal |
| API attach rate | Buyer later calls x402 API | `/public/metrics` | Secondary; not required for first receipt |

**Do not** publish “revenue confirmed” or “first revenue” in public copy until payment is settled and ledger-updated.

---

## 8) Fulfillment checklist

1. Validate intake against `TRUST_RECEIPT_CHECKOUT_V0.md` / `TRUST_RECEIPT_PILOT_INTAKE_SCHEMA.md`.
2. Confirm tier ($25 / $50 / $250) and **manual verification** of `payment_tx_hash` on Base.
3. Run Sentinel; mint receipt per `TRUST_RECEIPT_PILOT_PACK.md` §4.
4. Deliver JSON + Markdown; store internal copy only.
5. Update operator tracker — **no** public buyer PII paths.
