# Sentinel + x402 + AgentKit + Mycelium Trails — Composability Reference Draft

## 1) Purpose

Reference architecture only.
No partnership claim and no integration claim.

## 2) External reference

External community draft URL:
https://github.com/giskard09/argentum-core/blob/feat/mycelium-trails/docs/MYCELIUM_TRAILS_REFERENCE.md

This is an external community draft, not dependency wiring for Sentinel runtime.

## 3) Naming note

- Canonical product name is Sentinel Alpha / BeezShield.
- “Sentinel” is acceptable as short architecture name.
- Do not use AgentShield as our product name.

## 4) Layer responsibilities

- ATCP-style tool pre-flight layer (community signal context): tool/API boundary policy checks before contract-level risk checks
- Sentinel Alpha / BeezShield: pre-execution risk decision / allow-review-block policy assistance
- x402 / Lightning: machine-payable API / payment authorization context
- AgentKit-style execution layer: action execution after policy permits
- Mycelium Trails-style post-action layer: signed accountability record after execution

## 5) Temporal boundary

- before execution: should this agent act?
- during request/payment: is access/payment authorized?
- execution: perform action
- after execution: what happened and can it be verified?

## 6) Audit independence

Pre-decision and post-action proof should remain independent layers.
Sentinel should not be both the pre-decision engine and the post-action accountability writer.

- Sentinel pre-decision evaluates whether an action should proceed.
- Post-action trail records what happened after execution.
- Independent layers reduce circular self-attestation risk and improve auditability.

## 7) Reference flow

ATCP tool pre-flight -> Sentinel pre-check -> x402 payment authorization -> AgentKit action -> Mycelium Trails post-action record

## 8) Sentinel-side decision shape

- contract_address (runtime input)
- chain
- action: allow/review/block
- reason
- confidence
- explanation
- notSecurityGuarantee: true
- local Decision Receipt boundary object (docs/16_launch/SENTINEL_DECISION_RECEIPT.md)
- optional sentinel_decision_ref

Reference sample output:
`examples/agentkit-sentinel-provider/examples/sample-output.json`

## 9) Trail-side schema alignment

Community-suggested / external trail-side example fields:

- trail_id
- agent_id
- service
- operation
- action_ref
- payment_hash
- timestamp
- signature_ref
- claims
- success

Field notes:

- action_ref: cross-surface linking key
- payment_hash: payment/settlement reference
- sentinel_decision_ref: optional pre-decision payload/hash reference from the local deterministic Decision Receipt boundary object
- claims: runtime context observed after execution
- trace_id or receipt_id: optional tool-boundary receipt reference

This is schema context only and does not claim Mycelium integration.

## 10) Non-goals

- no partnership claim
- no official integration claim
- no official AgentKit provider claim
- no official x402 integration claim
- no Mycelium integration claim
- no ATCP integration claim
- no security guarantee
- no live simulation claim
- no wallet execution claim
- no signing claim

## 11) Open collaboration note

This draft can be refined if the external trail-side builder wants to contribute schema/example details.
Any cross-reference remains documentation-only unless future explicit agreement happens.
