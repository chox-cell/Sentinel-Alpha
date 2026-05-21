# Trust Receipt pilot checkout v0

**Purpose:** Semi-automated first-revenue pilot checkout — **website + manual ops only**. No Stripe, escrow smart contracts, API runtime changes, or false automation claims.

**Surface:** `apps/website/pilot/trust-receipt.html` · `FIRST_REVENUE_PLAYBOOK.md`

---

## 1) Checkout flow (buyer)

| Step | Buyer action | BeezShield action |
| --- | --- | --- |
| 1 | Choose tier: **$25** Draft Review · **$50** Operator Pilot · **$250** Integration Sprint | Display tier amount in USDC |
| 2 | Send **USDC on Base** only to **manual pilot payment address** (public x402 treasury) | **No** escrow; **no** auto-capture |
| 3 | Submit intake: contact, `payment_tx_hash`, redacted `proposed_action_summary`, `chain`, optional `result_ref_optional`, `notes` | Store intake; **do not** mint receipt yet |
| 4 | Wait for **manual payment verification** | Operator confirms tx → mints JSON + Markdown Trust Receipt v0 |

**Not automated:** payment detection, receipt generation, email delivery, or revenue recognition on submit.

---

## 2) Pricing tiers

| `selected_tier` (USDC) | Name | Deliverable |
| --- | --- | --- |
| **25** | Draft Review | Lighter boundary review artifact |
| **50** | Operator Pilot | Standard Trust Receipt v0 JSON + Markdown |
| **250** | Integration Sprint | Receipt + integration guidance per SOW |

Amount sent on-chain must match selected tier (USDC, 6 decimals).

---

## 3) Payment (manual pilot address)

| Field | Value |
| --- | --- |
| Network | **Base** only |
| Asset | **USDC** only |
| Address | `0x3cf9C2E55485fF8DAFfb59c84a0fa7c03bDbAeaf` |
| Label | **Manual pilot payment address** (same treasury as public x402 config / `identity-manifest.json`) |

**Warning:** Send **only USDC on Base**. Other tokens or chains are not credited automatically.

**Forbidden copy:** escrow (not escrow — funds are not held in release contract), “funds held in trust”, “instant delivery on payment”, “automated fulfillment”.

---

## 4) Payment verification (operator manual)

1. Receive checkout JSON (email or copied from pilot page).
2. Validate `payment_tx_hash` format (`0x` + 64 hex).
3. On Base, confirm USDC `Transfer` to manual pilot payment address for **≥ tier amount**.
4. Only after confirmation: set internal `payment_confirmed` (not public claim); assign `pilot_run_id`.
5. Run Sentinel + mint receipt per `TRUST_RECEIPT_PILOT_PACK.md`.

**No revenue claim** in marketing, ledger, or public metrics until **payment confirmed** on-chain (manual tx verification complete).

---

## 5) Checkout intake JSON (`trust-receipt-checkout-v0`)

| Field | Required | Notes |
| --- | --- | --- |
| `contact` | yes | Email or agreed handle |
| `selected_tier` | yes | `25` \| `50` \| `250` |
| `payment_tx_hash` | yes | Buyer’s USDC payment tx on Base |
| `proposed_action_summary` | yes | One redacted action description |
| `chain` | yes | e.g. `base` |
| `result_ref_optional` | no | Post-execution hash/ref if available |
| `notes` | no | Staging / timeline |

---

## 6) Claim boundaries

**Allowed**

- “Checkout v0: copy payment address, pay USDC on Base, submit tx hash for manual verification.”
- “Receipt delivered after operator confirms payment.”

**Forbidden (until verified internally)**

- Revenue confirmed / first revenue achieved (until tx verified + recorded)
- Escrow or custodial holding of buyer funds
- Automated or instant fulfillment on payment
- Official AgentKit / Coinbase / x402 partnership or endorsement

---

## 7) Refund / cure rule (pilot)

If BeezShield does not deliver Trust Receipt v0 **JSON + Markdown** matching `TRUST_RECEIPT_V0_SPEC.md` within **5 business days** of **confirmed** pilot payment, buyer may request a **one-time pilot fee refund** (tier amount). Remedy limited to pilot fee; no consequential damages. Refunds are **manual** — not smart-contract escrow.

---

## 8) Related docs

- `TRUST_RECEIPT_PILOT_INTAKE_SCHEMA.md` — broader intake fields
- `TRUST_RECEIPT_V0_SPEC.md` — receipt shape
- `fixtures/trust_receipt_buyer_pilot_sample.redacted.json` — sample deliverable
