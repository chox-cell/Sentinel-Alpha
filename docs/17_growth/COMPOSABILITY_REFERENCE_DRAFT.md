# Composability Reference Draft: Pre-Decision, Payment Authorization, Execution, and Post-Action Proof

## 1) Purpose

Reference architecture only.
No partnership claim and no integration claim.

## 2) Layer responsibilities

- Sentinel Alpha: pre-execution risk decision / allow-review-block policy assistance
- x402: machine-payable API / payment authorization context
- AgentKit-style execution layer: action execution after policy permits
- Mycelium Trails-style post-action layer: signed accountability record after execution

## 3) Temporal boundary

- before execution: should this agent act?
- during request/payment: is access/payment authorized?
- execution: perform action
- after execution: what happened and can it be verified?

## 4) Audit independence

Pre-decision and post-action proof should remain independent layers:

- Sentinel pre-decision evaluates whether an action should proceed.
- Post-action trail records what happened after execution.
- Independent layers reduce circular self-attestation risk and improve auditability.

## 5) Example flow

Sentinel pre-check -> x402 payment authorization -> AgentKit action -> post-action trail record

## 6) Sentinel-side example

- contract_address
- action: allow/review/block
- reason
- confidence
- notSecurityGuarantee: true
- sample output reference:
  `examples/agentkit-sentinel-provider/examples/sample-output.json`

## 7) Placeholder trail-side schema

Community-suggested / external trail-side example:

- agent_id
- action
- payment_hash
- claims
- timestamp
- signature

This is schema context only and does not claim Mycelium integration is live.

## 8) Non-goals

- no partnership claim
- no official integration claim
- no official AgentKit provider claim
- no official x402 integration claim
- no Mycelium integration claim
- no security guarantee
- no live simulation claim

## 9) Open collaboration note

This draft can be refined if the external trail-side builder wants to contribute schema/example details.
