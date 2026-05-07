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
