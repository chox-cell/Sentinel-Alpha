# Trust Receipt v0 — paid pilot pack

**Audience:** buyer / design partner evaluating BeezShield Sentinel + AgentKit-style workflow. **Not** a public product SLA.

## 1) What the buyer receives

One **Trust Receipt v0** JSON packet per completed pilot run:

- Redacted summary of the **proposed action** and **Sentinel decision** (`allow` / `review` / `block`)
- **Risk score** and **policy version** at decision time
- **Checked** vs **not checked** signal categories (explicit limits)
- **Payment lane** used for the x402-gated Sentinel call
- **Hash-only** link to AgentKit outcome (`agentkit_result_hash_or_tx_ref`)
- **Release / refund cure rule** for pilot delivery
- **Disclaimer** — not a security guarantee; not execution-quality proof

Deliverable file name pattern: `trust-receipt-v0_<pilot_run_id>.json`

Sample shape: `docs/17_growth/fixtures/trust_receipt_v0.redacted.sample.json`

## 2) Pilot flow (one run)

```text
Buyer scopes pilot action (staging/sandbox)
  → x402-paid POST /contracts/risk-score (v1, x402scan-compatible)
  → Sentinel returns decision + risk_score
  → AgentKit-style step runs only if buyer policy permits (buyer-controlled)
  → Operator mints Trust Receipt v0 (redacted)
  → Buyer receives JSON + optional verify instructions
```

**Independence:** Sentinel pre-check and AgentKit execution remain **separate layers**. The receipt **links** them with hashes; it does not attest that execution was correct or profitable.

## 2.1) Architecture (layer composition)

```text
[AURA reputation — optional, backward-looking]
        ↓
[Sentinel risk — forward-looking allow/review/block]
        ↓
[AgentKit-style execution — buyer-controlled]
        ↓
[Mycelium Trails post-execution signed trail — external evidence]
        ↓
[BeezShield Trust Receipt v0 — binder: refs + boundaries only]
```

- **Sentinel** does not write Mycelium trails or AURA scores.
- **Trust Receipt** binds `reputation_axis` + `post_execution_trail` **refs** when present — not full protocol payloads.
- **No** official partnership or integration claim with Mycelium or AURA.

## 3) Pricing alignment (claim-safe)

| Item | Pilot range | Notes |
| --- | --- | --- |
| Trust Receipt pilot bundle | **$25–$50** one-time | Aligns with `apps/website/pilot/trust-receipt.html` |
| Per-scan API (ongoing) | **0.02 USDC** basic lane | x402 on Base; not bundled into receipt list price unless stated in SOW |

No revenue guarantee. No implied refund unless `release_refund_cure_rule` in the issued receipt matches a signed SOW.

## 4) Operator checklist (mint receipt)

1. Confirm pilot SOW id and `pilot_run_id`.
2. Run Sentinel with buyer-approved **non-secret** args only; record `sentinel_decision`, `risk_score`, `policy_version`, `decision_timestamp`.
3. Build `normalized_args_hash` per `TRUST_RECEIPT_V0_SPEC.md` §3.1.
4. Set `checked_signals` / `not_checked` from actual engine categories (no invented coverage).
5. Set `agentkit_result_hash_or_tx_ref` to hash/ref only — **no** raw tx internals.
6. Set `payment_lane` to the lane charged (e.g. `basic`).
7. Set `secrets_excluded: true` and paste standard `disclaimer`.
8. Deliver JSON; update internal tracker only — **do not** publish buyer packet paths publicly.

## 5) Buyer verification (v0)

Buyers can verify:

- Field presence and schema version `trust-receipt-v0`
- `secrets_excluded === true`
- `sentinel_decision` matches their policy log if they retained a local Sentinel response
- Optional: recompute `normalized_args_hash` from agreed canonical args

Buyers **cannot** infer from v0 alone:

- Contract safety, exploit absence, or MEV/honeypot status
- Payment settlement finality (unless separately documented)
- Official Coinbase / AgentKit endorsement

## 6) API roadmap

| Endpoint | v0 status |
| --- | --- |
| `GET /pilot/trust-receipt/v0/sample` | Documented; implement when pilot API ships |
| `GET /pilot/trust-receipt/v0/{receipt_id}` | Documented; buyer fetch |
| `POST /pilot/trust-receipt/v0/issue` | Operator-only; post-run mint |

See `TRUST_RECEIPT_V0_SPEC.md` for request/response shapes.

## 7) Boundaries (required in buyer comms)

- No partnership, endorsement, or official AgentKit integration claim
- No security guarantee or “safe to execute” claim
- No honeypot / MEV prevention claims unless explicitly in `checked_signals` with live evidence (not v0 default)
- Trust Receipt is **not** a substitute for audit, formal verification, or exchange listing diligence

## 8) References

- Spec: `TRUST_RECEIPT_V0_SPEC.md`
- Website pilot: `apps/website/pilot/trust-receipt.html`
- AgentKit-style example: `examples/agentkit-sentinel-provider/`
- Trust loop fields: `TRUST_LOOP_FIELD_ALIGNMENT_V1.md`
