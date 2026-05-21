# Trust Receipt — ReaWorks-style pilot artifact

**Status:** buyer-grade **documentation + redacted JSON fixture only**. No live API routes. No partnership, endorsement, or security-guarantee claims.

## 1) Why this artifact exists

External review (ReaWorks-style) asked for a **separate post-action object** that buyers can inspect without conflating:

- **Pre-execution:** proposed action, normalized args (hashed), Sentinel decision, policy version, timestamp, what was checked vs not checked
- **Post-execution:** AgentKit tool/transaction outcome as **hash or opaque ref only** — not raw tx internals

This packet answers that request as a **paid-pilot deliverable** aligned with `TRUST_RECEIPT_V0_SPEC.md`, scoped for design-partner review before any public mint API.

## 2) Deliverable

| Item | Path |
| --- | --- |
| Redacted JSON (this pilot) | `docs/17_growth/fixtures/trust_receipt_reaworks_pilot.redacted.json` |
| **$25 review packet** | `docs/17_growth/REAWORKS_REVIEW_PACKET_001.md` + `fixtures/trust_receipt_reaworks_review_packet_001.redacted.json` |
| Generic v0 spec | `docs/17_growth/TRUST_RECEIPT_V0_SPEC.md` |
| Website pilot surface | `apps/website/pilot/trust-receipt.html` |

**Receipt id (sample):** `reaworks-pilot-2026-05-19-001`

## 3) Field map (buyer view)

| Field | Layer | Buyer meaning |
| --- | --- | --- |
| `proposed_action` | Pre | What the agent intended before Sentinel gate |
| `normalized_args_hash` | Pre | SHA-256 of canonical non-secret args (`secrets_excluded` applies) |
| `secrets_excluded` | Pre | Must be `true` — no keys, env, wallet material in packet |
| `sentinel_decision` | Pre | `allow` \| `review` \| `block` at decision time |
| `risk_score` | Pre | Sentinel score when decision was issued |
| `policy_version` | Pre | Policy bundle id (e.g. `sentinel-policy-v0`) |
| `decision_timestamp` | Pre | ISO-8601 UTC for Sentinel decision |
| `checked_signals` | Pre | Signal **categories** evaluated (labels only) |
| `not_checked` | Pre | Explicit limits — avoids overclaiming coverage |
| `agentkit_result_hash_or_tx_ref` | Post | Hash/ref to AgentKit tool or tx outcome — **not** calldata/logs |
| `payment_lane` | Payment | x402 lane for Sentinel call (e.g. `basic` / 0.02 USDC) |
| `release_refund_cure_rule` | Commercial | Delivery/refund boundary for the pilot fee |
| `disclaimer` | Legal | Not a security guarantee; not execution-quality proof |

Optional `linking_refs` (hashes only) may connect pre-decision and payment context without merging layers.

## 4) What this proves / does not prove

### Proves (within pilot scope)

- A **defined pre-execution gate** ran: proposed action class, hashed args, Sentinel `allow`/`review`/`block`, policy version, and timestamp are recorded.
- **Redaction policy** was applied (`secrets_excluded: true`).
- **Coverage boundaries** are explicit via `checked_signals` and `not_checked`.
- A **post-action link** exists as `agentkit_result_hash_or_tx_ref` (hash/ref only) for buyer-side correlation with their own AgentKit logs.
- **Commercial cure** text for pilot delivery is stated in `release_refund_cure_rule`.

### Does not prove

- Contract safety, exploit absence, honeypot status, or MEV resistance.
- Execution quality, profitability, slippage, or “safe to execute.”
- Full AgentKit or Coinbase endorsement, partnership, or official integration.
- Payment settlement finality beyond the stated x402 lane label.
- That the risk check substitutes for audit, formal verification, or exchange listing diligence.

**Core boundary:** Sentinel pre-check is **policy assistance**. AgentKit post-action ref is **correlation metadata**, not proof the onchain step succeeded or was correct.

## 5) Paid pilot copy block ($25–$50)

**Subject:** BeezShield Trust Receipt pilot — one redacted AgentKit + Sentinel run

> We’re offering a **small paid pilot ($25–$50 one-time)** to deliver one **Trust Receipt** JSON packet for a single staging/sandbox run: proposed action + hashed args (`secrets_excluded`), Sentinel decision (`allow`/`review`/`block`), risk score, policy version, timestamp, checked vs **not checked** signals, and an AgentKit result **hash/ref only** (no raw transaction internals).
>
> The receipt is for **review and audit linking** — it is **not** a security guarantee and **does not** prove execution quality or onchain safety. If we don’t deliver the agreed JSON within **5 business days** of confirmed pilot payment, the pilot fee is refundable per the cure rule in the receipt.
>
> Ongoing API usage remains x402-gated on Base (basic lane **0.02 USDC** per scan) separate from the one-time pilot bundle.

## 6) Operator notes (minting this artifact)

1. Use buyer-approved staging scope; never embed `.env`, API keys, or wallet keys.
2. Compute `normalized_args_hash` per `TRUST_RECEIPT_V0_SPEC.md` §3.1.
3. Populate `not_checked` honestly — include execution-quality and deep-scan limits by default.
4. Set `agentkit_result_hash_or_tx_ref` to `exec_ref:<sha256>` or `tx_ref:<opaque>` only.
5. Deliver `trust_receipt_reaworks_pilot.redacted.json` shape; mark production receipts with buyer-specific `receipt_id`.

## 7) Claim discipline

- Do not claim Agentic.Market or x402scan listing from this artifact.
- Do not claim the risk check proves execution quality.
- Do not publish buyer-identifying data or raw chain payloads in public repos.

## 8) Pilot closeout (2026-05-19)

| Item | Status |
| --- | --- |
| ReaWorks review artifact | **Ready** — `REAWORKS_REVIEW_PACKET_001.md` + fixtures |
| ReaWorks | **community_feedback_only** — optional $25 paid review **cancelled_or_paused** |
| API mint routes | **Not implemented** (documentation-only) |
| Bazaar v2 / Agentic.Market | Validator **passed** on production v2 (`62c0b1f`); **not listed** in search |
| x402scan v1 | **Unchanged** — registered on `/contracts/risk-score` only |

Deliver public/community packet for feedback; paid ReaWorks review **not proceeded**. First-revenue target: **direct buyer/operator pilot**. No payment, revenue, or guarantee claims.
