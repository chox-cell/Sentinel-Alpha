# Minimum Verifiable Trust Loop (Sample)

This is a local sample-only, documentation-only fixture for the trust loop:

ATCP-style tool pre-flight placeholder
-> Sentinel Decision Receipt
-> Payment Decision Link
-> AgentKit-style execution placeholder
-> Mycelium Trails-style post-action record

Reference:
`docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md`

## Flow summary

- **Tool pre-flight**: placeholder receipt context (`trace_id`, `receipt_id`) for tool-boundary policy shape.
- **Sentinel pre-check**: decision receipt-like fields including `sentinel_decision_ref` and `action_ref`.
- **Payment authorization context**: `payment_decision_link_ref`, `payment_protocol`, `payment_status`, optional `payment_hash`.
- **Execution**: explicit placeholder (`not_executed`) with `wallet_execution: false` and `transaction_signed: false`.
- **Post-action trail**: Mycelium Trails-style fields with Arbitrum/Base anchor placeholders.

## Field meanings

- `action_ref`: shared cross-surface linking key for action context.
- `sentinel_decision_ref`: optional pre-decision reference identifier for Sentinel-side boundary context.
- `payment_decision_link_ref`: boundary link from decision context to optional payment authorization context.
- `payment_hash`: payment/settlement surface reference when available (null in this sample).
- `trace_id` / `receipt_id`: optional tool-boundary references from pre-flight context.

## Boundaries

- sample only
- no live calls
- no wallet execution/signing
- no DB writes
- no official integration/partnership claim
- no automatic x402 settlement
- not a security guarantee
