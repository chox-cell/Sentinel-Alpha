# Trust Receipt pilot intake — static JSON schema (v0)

**Purpose:** Minimal lead/pilot intake shape for **direct buyer/operator** first-revenue workflow. **Not** a live API. Operators collect via email, form copy, or manual JSON file.

**Schema id:** `trust-receipt-pilot-intake-v0`

## Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `contact` | string | yes | Buyer email or agreed contact handle (no secrets in public samples) |
| `project_name` | string | yes | Buyer project or team name |
| `agent_or_tool_description` | string | yes | One-line description of agent, framework, or tool context |
| `proposed_action_summary` | string | yes | Human-readable summary of the single redacted action to evaluate |
| `chain` | string | yes | Target chain id (e.g. `base`, `ethereum`) |
| `contract_or_tool_ref_redacted` | string | yes | Hash, alias, or redacted identifier — **not** raw contract address or calldata |
| `has_post_action_result_ref` | boolean | yes | Whether buyer can supply a post-execution hash/ref for binding |
| `preferred_payment_method` | string | yes | e.g. `usdc_base_manual`, `invoice`, `other` — **no** on-page payment automation in v0 |
| `notes` | string | no | Staging constraints, timeline, tier preference |

## Example (redacted)

```json
{
  "schema": "trust-receipt-pilot-intake-v0",
  "contact": "builder@example.com",
  "project_name": "Example Agent Ops",
  "agent_or_tool_description": "Coinbase AgentKit-style sandbox agent on Base",
  "proposed_action_summary": "Contract risk precheck before one swap step",
  "chain": "base",
  "contract_or_tool_ref_redacted": "contract_id_hash:b569321de72d0af89c2fb48a484de3fc9343f31600ae1f3e13d633cb48cbf816",
  "has_post_action_result_ref": true,
  "preferred_payment_method": "usdc_base_manual",
  "notes": "Prefer $50 operator pilot tier; staging only."
}
```

## Operator rules

1. Reject intake that includes private keys, `.env` values, full tx blobs, or raw `0x` addresses in `contract_or_tool_ref_redacted`.
2. Map accepted intake to internal `pilot_run_id` before minting Trust Receipt v0.
3. Deliverable: `trust_receipt_buyer_pilot_sample.redacted.json` shape + companion Markdown receipt (see `FIRST_REVENUE_PLAYBOOK.md`).

## Claim boundaries

- Intake submission **does not** imply revenue recognized, paid customer, or partnership.
- Payment is **manual** until a separate payment rail is explicitly launched.
