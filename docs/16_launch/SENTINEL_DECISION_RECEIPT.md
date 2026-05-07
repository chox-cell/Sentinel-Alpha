# Sentinel Decision Receipt Boundary (v9.0)

## 1) Purpose

The Decision Receipt is a local deterministic Sentinel-side reference object for risk decisions.
It exists to provide a runtime-friendly reference boundary for `sentinel_decision_ref` and related linking fields without enabling database writes, provider calls, wallet execution, or external integrations.

## 2) Receipt fields

`build_decision_receipt(response, request_context=None, config=None)` returns:

- `receipt_version` (`v1`)
- `decision_id`
- `sentinel_decision_ref`
- `action_ref`
- `chain`
- `contract_address_hash`
- `requested_action`
- `intent_hash`
- `decision_action`
- `confidence`
- `risk_score`
- `signals_summary`
- `explanation_hash`
- `policy_version`
- `created_at`
- `notSecurityGuarantee` (`true`)
- `persistence_status` (`not_persisted`)
- `external_integration_status` (`not_integrated`)
- `notes`

## 3) Trust loop support

This receipt is the Sentinel-side object that supports the trust-loop composability pattern:

- ATCP-style tool pre-flight
- Sentinel pre-check with a deterministic decision receipt
- x402 payment authorization
- AgentKit-style execution
- Mycelium Trails-style post-action record

The receipt can provide `sentinel_decision_ref` and `action_ref` as optional linking context between pre-decision and post-action records.

## 4) Reference semantics

- `sentinel_decision_ref`: SHA-256 over a sanitized canonical payload representing pre-decision context.
- `action_ref`: SHA-256 over `chain + contract_address_hash + requested_action + intent_hash` (where available).

These references are deterministic for equivalent sanitized inputs and remain local boundary artifacts.

## 5) Privacy constraints

- Raw contract addresses are hashed in receipt output (`contract_address_hash`).
- Raw secrets are never included (no raw headers, auth tokens, private keys, seed phrases, or payment signatures).
- Only minimal summary fields are carried for linking and audit context.

## 6) Persistence and integration boundaries

- Decision Receipt is not persisted by default.
- Decision Receipt is not integrated with external providers by default.
- No official integration claim.
- No partnership claim.

## 6.1) Local Decision Receipt Store boundary (v9.1)

- A disabled-by-default local Decision Receipt Store boundary is available for future local history usage.
- Default behavior remains `not_persisted` with no DB requirement, no Redis requirement, and no filesystem requirement.
- No default write is performed; write status remains `not_run` unless an explicit in-memory test backend is passed.
- Future local storage mode is limited to sanitized receipt records only.
- No raw contract addresses or raw secrets are allowed in store records.
- No raw secrets are allowed in store records.

## 6.2) x402 Payment Decision Link boundary (v9.2)

- A local deterministic payment-decision link boundary can connect `sentinel_decision_ref` / `action_ref` with optional `payment_request_id` and `payment_hash`.
- The link object is boundary-only and not persisted by default.
- No raw payment headers, signatures, bearer tokens, private keys, seed phrases, or wallet keys are included.
- No automatic x402 settlement claim.
- No official x402 integration claim.
- `payment_decision_link_ref` is deterministic (SHA-256 over sanitized canonical linking payload).
- The local AgentKit demo and sample fixture include this minimum shape for reference only:
  `sentinel_decision_ref` -> `action_ref` -> `payment_decision_link_ref`.

## 7) Safety boundaries

- Not a security guarantee.
- No live simulation claim.
- No honeypot detection claim.
- No MEV prevention claim.

## 8) Future composability direction (docs-only)

In future documentation-only reference patterns, `sentinel_decision_ref` and `action_ref` can be linked to post-action trail fields such as `action_ref`, `payment_hash`, `claims`, and optional `trace_id`/`receipt_id`.
This note is composability context only and does not assert any official live integration.

The local store boundary prepares `sentinel_decision_ref` auditability context without enabling runtime DB writes or managed service activation.
