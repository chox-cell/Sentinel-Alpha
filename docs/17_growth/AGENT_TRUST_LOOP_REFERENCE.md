# Agent Trust Loop Reference Pattern

## 1) Purpose

Reference architecture only.
No partnership claim and no integration claim.

This document positions complementary trust layers around autonomous agent actions without asserting shipped joint integrations.

## 2) Layer map

- ATCP-style tool pre-flight: can this agent call this tool/API?
- Sentinel Alpha / BeezShield: should this agent touch this contract or asset?
- x402 / Lightning: is the request/payment authorized?
- AgentKit-style execution layer: execute if policy permits.
- Mycelium Trails-style post-action proof: what happened, and can it be verified?

## 3) Reference flow

ATCP tool pre-flight
-> Sentinel contract/asset pre-check
-> x402 payment authorization
-> AgentKit action
-> Mycelium Trails post-action record

## 4) Field alignment

- action_ref: cross-surface linking key
- sentinel_decision_ref: optional pre-decision payload/hash reference, produced from a local Sentinel Decision Receipt boundary object
- payment_decision_link_ref: optional bridge reference linking pre-decision context to payment authorization context
- payment_hash: payment/settlement reference
- claims: runtime/post-action context
- trace_id or receipt_id: optional tool-boundary receipt reference

## 5) Independence

Each layer should remain independently verifiable.

- Tool boundary policy checks, contract/asset risk checks, payment authorization, execution, and post-action receipts should not collapse into one self-attesting layer.
- Independent evidence paths reduce circular trust assumptions and improve audit review quality.
- Cross-references (`action_ref`, `sentinel_decision_ref`, `payment_hash`, and optional `trace_id`/`receipt_id`) should link records without removing layer independence.

## 6) Non-goals

- no partnership claim
- no official integration claim
- no official AgentKit provider claim
- no official x402 integration claim
- no Mycelium integration claim
- no ATCP integration claim
- no security guarantee
- no live simulation claim

## 7) Current status

- Sentinel prototype exists locally.
- Sentinel Decision Receipt boundary exists locally for deterministic `sentinel_decision_ref` / `action_ref` references.
- Sentinel Decision Receipt Store boundary exists as disabled-by-default local history preparation (sanitized-only, not persisted by default).
- Mycelium Trails external draft exists.
- ATCP signal is community discussion only.
- No official integration exists.

## 8) External discussion references

- Mycelium Trails external draft URL:
  https://github.com/giskard09/argentum-core/blob/feat/mycelium-trails/docs/MYCELIUM_TRAILS_REFERENCE.md
- ATCP signal source is treated as community discussion context for architecture mapping, not as shipped integration evidence.

## 9) Mycelium Trails-style Post-Action Section — External Community Contribution

### Attribution

- Contributed by `giskard09` as community / adjacent builder.
- This is an external/community section, not a Sentinel dependency.
- Documentation-only composability contribution, not an official integration or partnership.
- This is not official integration or partnership.

### Layer responsibility

- Records what execution produced.
- Does not validate authorization.
- Does not enforce policy.
- Does not block execution.

### TrailRecord schema excerpt

```json
{
  "trail_id": "<uuid>",
  "agent_id": "<string>",
  "action_ref": "<sha256-hex>",
  "payment_hash": "<sha256-hex>",
  "service": "<string>",
  "operation": "<string>",
  "success": true,
  "anchors": {
    "arbitrum": { "chain_id": 42161, "block": "<int>", "tx_hash": "<hex>" },
    "base": { "chain_id": 8453, "block": "<int>", "tx_hash": "<hex>" }
  },
  "timestamp": "<iso8601>"
}
```

### action_ref algorithm

- `SHA-256(agent_id:action_type:scope:timestamp)`
- Deterministic if same inputs are used.
- Used as shared cross-surface key.

### Verification endpoint shape (external surface)

- `GET https://argentum.rgiskard.xyz/trails/verify?payment_hash=<hex>`
- Returns `anchors.arbitrum` and `anchors.base` with `block` + `tx_hash`.
- Public, no API key.
- Treated as an external verification surface, not a Sentinel dependency.

### Field alignment with Sentinel

- `action_ref`: shared cross-surface key.
- `sentinel_decision_ref`: optional pre-decision reference; Mycelium may reference boundary fields but does not validate Sentinel authorization logic.
- `payment_hash`: settlement/payment surface reference.
- `claims`: runtime/post-action context if available.

### Disclaimers

- no partnership claim
- no official integration claim
- no Stripe/Coinbase/x402-foundation affiliation claim
- no security guarantee
- not audited; community-built infrastructure
- composability pattern only
