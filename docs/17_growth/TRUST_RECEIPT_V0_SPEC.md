# BeezShield Trust Receipt v0 — specification

**Status:** documentation + redacted sample fixture only (paid-pilot artifact). **Not** a live public API guarantee, security certification, or execution-quality proof.

## 1) Purpose

Trust Receipt v0 is a **buyer-grade, redacted packet** summarizing one **AgentKit-style + Sentinel** pre-execution gate for a **small paid pilot**. It lets a buyer verify *what was checked*, *what was excluded*, and *how policy classified the proposed action* — without exposing secrets, env values, wallet material, or raw transaction internals.

## 2) Scope (v0)

| In scope | Out of scope |
| --- | --- |
| One redacted run summary per pilot | Warehouse analytics, SLA, or revenue guarantees |
| Hashed / categorical fields only | Raw contract addresses, calldata, private keys |
| Sentinel `allow` / `review` / `block` + `risk_score` | Honeypot/MEV prevention claims |
| x402 **payment lane** label (e.g. `basic`) | Full payment signatures or treasury secrets |
| Optional **hash/ref** to AgentKit outcome | Full tx trace, logs, or mempool detail |

## 3) Packet fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `receipt_version` | string | yes | Constant: `trust-receipt-v0` |
| `receipt_id` | string | yes | Opaque pilot delivery id (UUID or deterministic pilot id) |
| `pilot_only` | boolean | yes | `true` for v0 paid-pilot artifacts |
| `secrets_excluded` | boolean | yes | Must be `true`; documents redaction policy applied |
| `proposed_action` | string | yes | Human-readable action class (e.g. `contract_risk_precheck_before_agentkit_step`) |
| `normalized_args_hash` | string (hex) | yes | SHA-256 over canonical JSON of **non-secret** args (chain, action kind, hashed identifiers — no raw secrets) |
| `sentinel_decision` | enum | yes | `allow` \| `review` \| `block` |
| `risk_score` | number | yes | Sentinel score at decision time (0–100 scale in pilot) |
| `policy_version` | string | yes | e.g. `sentinel-policy-v0` |
| `decision_timestamp` | string (ISO-8601 UTC) | yes | When Sentinel decision was recorded |
| `checked_signals` | string[] | yes | Signal **categories** evaluated (names only) |
| `not_checked` | string[] | yes | Explicit non-claims / limits of the run |
| `agentkit_result_hash_or_tx_ref` | string | yes | **Hash or opaque ref only** — not raw tx body, calldata, or wallet addresses |
| `payment_lane` | string | yes | x402 lane used for the pilot call (e.g. `basic`) |
| `release_refund_cure_rule` | string | yes | Pilot commercial cure text (delivery/refund boundary) |
| `disclaimer` | string | yes | Must state: not a security guarantee; not execution-quality proof |
| `linking_refs` | object | no | Optional cross-surface refs (`action_ref`, `sentinel_decision_ref`, `payment_decision_link_ref`) — hashes only |
| `sample_only` | boolean | no | `true` on public fixtures |

### 3.1) `normalized_args_hash` canonicalization

Hash input MUST be JSON with **sorted keys**, UTF-8, no whitespace:

```json
{
  "action_kind": "contract_risk_precheck",
  "chain": "base",
  "contract_identifier_hash": "<sha256 of lowercased address or opaque id>",
  "pilot_run_id": "<opaque pilot id>"
}
```

Never include: API keys, bearer tokens, `X402-PAYMENT` payloads, private keys, seed phrases, `.env` values, or full request bodies.

### 3.2) `agentkit_result_hash_or_tx_ref`

Allowed forms:

- `exec_ref:<sha256>` — hash of redacted execution summary JSON
- `tx_ref:<tx_hash_prefix_only>` — **only** if buyer already has chain context; never include calldata, from/to wallet labels, or internal revert data in the receipt packet

Forbidden in v0 packets: log blobs, RPC debug traces, signed tx hex.

## 4) API shape (pilot v0 — proposed)

v0 **delivers JSON files** to paid-pilot buyers. Endpoints below are the **target contract** for a later implementation; they are **not** claimed as live on `api.beezshield.com` until separately verified.

### 4.1) Issue (operator / post-run)

```http
POST /pilot/trust-receipt/v0/issue
Content-Type: application/json
Authorization: <pilot operator credential — not documented here>
```

**Request (redacted inputs only):**

```json
{
  "pilot_run_id": "pilot-2026-05-19-demo-001",
  "proposed_action": "contract_risk_precheck_before_agentkit_step",
  "normalized_args": {
    "action_kind": "contract_risk_precheck",
    "chain": "base",
    "contract_identifier_hash": "b569321de72d0af89c2fb48a484de3fc9343f31600ae1f3e13d633cb48cbf816"
  },
  "sentinel_response_ref": "<internal — not returned to buyer>",
  "agentkit_result_ref": "<hash-only ref>",
  "payment_lane": "basic"
}
```

**Response `201`:** full Trust Receipt v0 packet (same schema as fixture).

### 4.2) Fetch (buyer)

```http
GET /pilot/trust-receipt/v0/{receipt_id}
```

**Response `200`:** Trust Receipt v0 JSON. **404** if unknown or expired pilot id.

### 4.3) Public sample (documentation)

```http
GET /pilot/trust-receipt/v0/sample
```

Returns the redacted fixture at `docs/17_growth/fixtures/trust_receipt_v0.redacted.sample.json` shape — **not** a real buyer run.

## 5) Privacy and redaction rules

- `secrets_excluded` MUST be `true` on every issued receipt.
- No `.env`, treasury private keys, or facilitator credentials.
- No raw `contract_address`; use `contract_identifier_hash` inside args hash only.
- No payment signatures, JWTs, or session cookies.
- `checked_signals` / `not_checked` are **labels**, not raw provider JSON.

## 6) Claim discipline

**Allowed**

- “Trust Receipt v0 summarizes one redacted Sentinel + AgentKit-style pilot run.”
- “Receipt is policy assistance metadata, not proof of safe execution.”

**Forbidden**

- Security guarantee, audit certification, or “safe to execute” claim
- Official AgentKit / Coinbase partnership or integration
- Honeypot detected, MEV prevented, or execution-quality proof
- Listing Agentic.Market or x402scan as endorsement

## 7) Related artifacts

| Artifact | Path |
| --- | --- |
| Redacted sample JSON | `docs/17_growth/fixtures/trust_receipt_v0.redacted.sample.json` |
| Paid pilot pack | `docs/17_growth/TRUST_RECEIPT_PILOT_PACK.md` |
| AgentKit demo output (separate) | `examples/agentkit-sentinel-provider/examples/sample-output.json` |
| Decision receipt boundary | `docs/16_launch/SENTINEL_DECISION_RECEIPT.md` |
