# Builder outreach execution tracker (v4.3)

Track the first **20** builder targets. Replace placeholder rows **T01–T20** with researched entries; keep statuses honest—do not mark **integrated** until there is a verified integration.

**Allowed status values:** `not contacted` · `contacted` · `replied` · `interested` · `rejected` · `integrated`

## How to use

1. Fill **Target name**, **Link**, **Reason**, and **Message channel** after research.
2. Set **Relevance score** (1–5) using `FIRST_20_BUILDER_TARGETS.md`.
3. Update **Status** and dates as outreach progresses.
4. **Notes** are for facts only (no invented outcomes).

## Tracker

| ID | Target name | Type | Link | Relevance (1–5) | Reason | Message channel | Status | Date contacted | Follow-up date | Notes |
|----|-------------|------|------|-----------------|--------|-----------------|--------|----------------|----------------|-------|
| T01 | — unassigned — | builder | TBD | 3 | Placeholder slot | TBD | not contacted | | | Assign first verified target. |
| T02 | — unassigned — | repo | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T03 | — unassigned — | community | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T04 | — unassigned — | company | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T05 | — unassigned — | builder | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T06 | — unassigned — | repo | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T07 | — unassigned — | builder | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T08 | — unassigned — | community | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T09 | — unassigned — | builder | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T10 | — unassigned — | repo | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T11 | — unassigned — | company | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T12 | — unassigned — | builder | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T13 | — unassigned — | repo | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T14 | — unassigned — | builder | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T15 | — unassigned — | community | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T16 | — unassigned — | builder | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T17 | — unassigned — | repo | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T18 | — unassigned — | builder | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T19 | — unassigned — | company | TBD | 3 | Placeholder slot | TBD | not contacted | | | |
| T20 | — unassigned — | builder | TBD | 3 | Placeholder slot | TBD | not contacted | | | Assign twentieth verified target. |

## Product mention (copy-safe)

- **npm SDK:** `@beezshield/sentinel` — install: `npm install @beezshield/sentinel`
- **AgentKit-style example:** available in-repo; **official provider coming next** (not a live Coinbase AgentKit provider).
- Does not guarantee safety outcomes; builders supply x402 settlement explicitly (the SDK does not auto-settle).

## Manual outreach log (actual sends)

- target: x402 Foundation / x402
- source_url: https://github.com/x402-foundation/x402
- channel: GitHub Issue
- issue_url: https://github.com/x402-foundation/x402/issues/2198
- sent_at: 2026-05-05
- status: contacted
- response_status: pending
- next_follow_up_date: 2026-05-12
- community_responder: giskard09 (community / adjacent builder; not confirmed AgentKit maintainer)
- community_project_mentioned: Mycelium Trails
- community_demo_url: https://argentum.rgiskard.xyz/trails/demo
- community_signal: pre/post loop interest (Sentinel pre-check -> AgentKit action -> Mycelium Trails post-action record)
- note: message used evidence-only wording and no safety guarantee claims; Mycelium Trails appears complementary post-execution accountability, not competing; no official AgentKit acceptance, no integration claim, and no partnership claim.

- target: Coinbase AgentKit
- source_url: https://github.com/coinbase/agentkit
- channel: GitHub Issue
- issue_url: https://github.com/coinbase/agentkit/issues/1168
- sent_at: 2026-05-05
- status: contacted
- response_status: pending
- next_follow_up_date: 2026-05-12
- comment_type: local demo follow-up
- follow_up_sent_at: 2026-05-06
- follow_up_channel: GitHub Issue Comment
- demo_commit: 7c2190f
- demo_path: examples/agentkit-sentinel-provider
- demo_script: npm run demo
- community_composability_alignment:
  - responder_username: giskard09
  - responder_role: community / adjacent builder
  - responder_project: Mycelium Trails / argentum-core
  - responder_not_confirmed_agentkit_maintainer: true
  - responder_not_confirmed_x402_maintainer: true
  - external_repo: https://github.com/giskard09/argentum-core
  - external_doc_path: feat/mycelium-trails/docs/MYCELIUM_TRAILS_REFERENCE.md
  - external_draft_url: https://github.com/giskard09/argentum-core/blob/feat/mycelium-trails/docs/MYCELIUM_TRAILS_REFERENCE.md
  - signal_type: mutual documentation alignment / community composability signal
  - observed_alignment:
    - sentinel_decision_ref accepted as optional back-reference
    - audit independence preserved between pre-decision and post-action records
    - external Mycelium Trails reference draft complements COMPOSABILITY_REFERENCE_DRAFT.md
    - end-to-end pattern confirmed as complete from both sides (Sentinel pre-check -> x402 payment authorization -> AgentKit action -> Mycelium Trails post-action record)
    - same documentation boundaries confirmed on their side
  - boundaries:
    - documentation-only alignment
    - not partnership
    - not official integration
    - not official AgentKit response
    - not official x402 response
    - not a security guarantee
  - mycelium_contribution_signal:
    - responder_username: giskard09
    - responder_role: community / adjacent builder
    - responder_project: Mycelium Trails / argentum-core
    - responder_not_confirmed_agentkit_maintainer: true
    - responder_not_confirmed_x402_maintainer: true
    - responder_not_confirmed_stripe_maintainer: true
    - external_doc_path: feat/mycelium-trails/docs/MYCELIUM_TRAILS_REFERENCE.md
    - related_external_issue: https://github.com/stripe/ai/issues/356
    - related_contributors_mentioned:
      - aeoess
      - jagmarques
    - anchors_mentioned:
      - Arbitrum One
      - Base mainnet
    - observed_summary:
      - layered framing holds with distinct layer questions and no coupling requirement
      - TrailRecords occupy the post-action slot in their reference framing
      - action_ref links APS receipt, asqav wire format, and on-chain record in their fixture
      - three fixture trails reported as anchored on Arbitrum One and Base mainnet with public verifiability context
      - explicit offer to contribute the Mycelium section to the Agent Trust Loop reference doc
      - boundaries repeated: no partnership claim, no official integration claim, composability pattern only
    - concrete_mycelium_section_content_received:
      - section_target_doc: docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md
      - section_title: Mycelium Trails-style Post-Action Section — External Community Contribution
      - trailrecord_fields_shared:
        - trail_id
        - agent_id
        - action_ref
        - payment_hash
        - service
        - operation
        - success
        - anchors.arbitrum.chain_id/block/tx_hash
        - anchors.base.chain_id/block/tx_hash
        - timestamp
      - action_ref_algorithm: SHA-256(agent_id:action_type:scope:timestamp)
      - verification_endpoint_shape: GET https://argentum.rgiskard.xyz/trails/verify?payment_hash=<hex>
      - verification_surface_note: public endpoint with anchors on Arbitrum One and Base mainnet; treated as external/community verification surface
    - classification: Mycelium Trails community documentation contribution signal (documentation-only)
    - review_feedback_and_verification_offer:
      - reviewer: giskard09
      - feedback: Mycelium layer responsibility, schema, action_ref algorithm, anchor fields, and independence framing were reviewed as accurate
      - fixture_request: Trust Loop Report fixture requested as useful
      - verification_offer: willing to verify Mycelium-side fields against the live verify endpoint shape once fixture exists
      - collaboration_type: documentation-only community collaboration signal
    - mycelium_field_validation_signal:
      - reviewer: giskard09
      - validation_scope: Trust Loop Report fixture post_action_trail section
      - validated_fields:
        - trail_id
        - agent_id
        - action_ref
        - payment_hash
        - service
        - operation
        - success
        - anchors.arbitrum.chain_id/block/tx_hash
        - anchors.base.chain_id/block/tx_hash
        - verification_endpoint_shape
      - sample_note: payment_hash null is correct for documentation-only sample
      - live_flow_note: payment_hash is cross-surface key linking payment authorization context to post_action_trail
      - outcome_note: independently verifiable loop without trusting either side
      - signal_classification: external/community field validation signal only
    - boundaries:
      - not partnership
      - not official integration
      - not official AgentKit response
      - not official x402 response
      - not Stripe endorsement
      - not a security guarantee
- note: message used evidence-only wording and no safety guarantee claims; demo is local-only, not official provider, no wallet execution/signing, and not a security guarantee.

- target: elizaOS / eliza
- source_url: https://github.com/elizaOS/eliza
- channel: GitHub Issue
- issue_url: https://github.com/elizaOS/eliza/issues/7396
- sent_at: 2026-05-05
- status: contacted
- response_status: closed (completed)
- next_follow_up_date: hold
- note: message used evidence-only wording and no safety guarantee claims; issue closed as completed by lalalune with labels bug, security; no written acceptance/rejection observed; visibility signal only, not integration or partnership.

## x402 ecosystem directory redirection (v12.x)

Maintainer signal on x402 ecosystem page PR (ecosystem page sunset; PR closed; community directories suggested):

- signal_type: directory redirection received
- integration_claim: false
- partnership_claim: false
- endorsement_claim: false
- rejection_of_beezshield_specifically: false
- notes: not a BeezShield-specific rejection; not acceptance/integration/partnership; prepare manual submissions per `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md`

### x402 community directory submission targets (not submitted)

| Directory | URL | status | submission_owner | copy_variant | notes |
| --- | --- | --- | --- | --- | --- |
| x402scan | https://x402scan.com | not submitted | Chox | short | See submission pack §7 |
| Agentic.Market | https://agentic.market | not submitted | Chox | long | See submission pack §7 |
| Pay.sh | https://pay.sh | not submitted | Chox | short | See submission pack §7 |
| ampersend discover | https://app.ampersend.ai/discover | not submitted | Chox | long | See submission pack §7 |

## x402scan directory registration attempt (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (“This URL only”)
- registration_status: **attempted_validation_failed** (no listing claimed)
- observed_before_fix:
  - GET → **405** Method Not Allowed (`Allow: POST`)
  - POST (JSON body + `X-SENTINEL-LANE: basic`) → **402** + x402 challenge JSON (`payment_method: x402`, `network: eip155:8453`, `pay_to`, `amount_usdc`, `resource`, `lane`, …)
  - validator_message: **Error: Expected 402 response** (consistent with GET-based probe expecting 402)
- compatibility_note: GET must return **402** challenge for discovery validators; POST behavior unchanged — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` §3a
- integration_claim: false
- partnership_claim: false
- listing_success_claim: false
- notes: update **§7 x402scan row** to `submitted` **only** after manual verification and captured listing URL; do not mark success prematurely

## giskard09 / Mycelium Trails — x402 directory cross-reference signal (v12.x)

Paraphrased **community** reply on the closed x402 ecosystem PR thread (no implied maintainer authority):

- responder: giskard09 (community / adjacent builder; role as stated in prior tracker notes)
- signal: **pre/post split** described as clean — Sentinel at **decision boundary**, Mycelium at **execution record**; **independent layers**, **same discovery surfaces**; may **show up together** without coupling specs
- stated intent: will **submit Mycelium** to the **same** community directories listed in the redirection table above
- future copy: **openness to cross-reference** in each other’s directory copy **once both submissions are live** (listings exist)
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false
- coupled_runtime_stack_claim: false
- directory_submissions_status: **community directory rows above remain `not submitted` here** until a real manual submission is recorded and verified
- status: **community alignment signal** / **no partnership** / **no integration**
- notes: positive **alignment signal** only; not partnership, not approval, not shared runtime stack; cross-reference is **optional** and **after** both listings are live — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` §10
