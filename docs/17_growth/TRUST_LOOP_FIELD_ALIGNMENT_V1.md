# Trust Loop Field Alignment v1

## 1) Purpose

Documentation-only field map for the Agent Trust Loop.
No partnership claim and no integration claim.

## 2) Field alignment table

| field | owner_layer | purpose | example_source | safe_to_store | raw_secret_allowed | persistence_default | integration_status |
|---|---|---|---|---|---|---|---|
| `trace_id` | ATCP-style tool pre-flight | Tool-boundary trace correlation for pre-flight checks | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `receipt_id` | ATCP-style tool pre-flight | Tool-boundary receipt correlation key | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `action_ref` | Sentinel Alpha / BeezShield | Shared cross-surface action linking key | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `sentinel_decision_ref` | Sentinel Alpha / BeezShield | Pre-decision boundary reference identifier | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `payment_decision_link_ref` | x402 / Lightning payment context | Decision-to-payment boundary link reference | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `payment_hash` | x402 / Lightning payment context | Optional payment/settlement surface reference (sample may use null; live flow uses it as cross-surface payment-to-trail key) | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes (hash/reference only) | no | not_persisted | not_integrated |
| `contract_address_hash` | Sentinel Alpha / BeezShield | Contract identifier in hashed form for privacy | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `decision_action` | Sentinel Alpha / BeezShield | Allow/review/block policy-assistance result | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `confidence` | Sentinel Alpha / BeezShield | Confidence indicator for decision interpretation | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `notSecurityGuarantee` | Sentinel Alpha / BeezShield | Explicit non-guarantee boundary marker | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `trail_id` | Mycelium Trails-style post-action record | Post-action record identifier | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `agent_id` | Mycelium Trails-style post-action record | Agent-scoped post-action record key | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `service` | Mycelium Trails-style post-action record | Service context for recorded operation | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `operation` | Mycelium Trails-style post-action record | Operation type/context in post-action record | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `success` | Mycelium Trails-style post-action record | Post-action success marker | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `anchors.arbitrum.tx_hash` | Mycelium Trails-style post-action record | Arbitrum anchor transaction reference | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `anchors.base.tx_hash` | Mycelium Trails-style post-action record | Base anchor transaction reference | `reports/trust_loop/minimum_verifiable_loop.sample.json` | yes | no | not_persisted | not_integrated |
| `claims` | AgentKit-style execution / post-action context | Optional runtime or post-action contextual claims payload | `docs/17_growth/COMPOSABILITY_REFERENCE_DRAFT.md` | yes (sanitized only) | no | not_persisted | not_integrated |

## 3) Owner layers

- ATCP-style tool pre-flight
- Sentinel Alpha / BeezShield
- x402 / Lightning payment context
- AgentKit-style execution
- Mycelium Trails-style post-action record

## 4) Privacy rules

- no private keys
- no seed phrases
- no raw auth headers
- no bearer tokens
- no payment signatures
- no raw contract addresses in Sentinel receipts
- hash identifiers where possible

## 5) Current status

- sample fixture exists
- documentation-only
- no live integration
- no partnership claim
- no official endorsement

## 6) Future use

- field alignment can guide future PRs/examples if explicitly requested by upstream maintainers
- not a runtime contract yet
