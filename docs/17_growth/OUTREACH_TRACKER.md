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
| x402scan | https://x402scan.com | **registered** | Chox | short | §3o / `X402SCAN_REGISTRATION_EVIDENCE.md` |
| Agentic.Market | https://agentic.market | validator_passed_not_listed | Chox | long | validator pass 62c0b1f · search 0 |
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

## x402scan directory registration — second attempt (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (“This URL only”)
- registration_status: **attempted_validation_failed_schema** (no listing claimed)
- observed:
  - **GET** → **402** + JSON challenge (legacy **`x402_version`** / **`payment_method`** / **`network`** / **`pay_to`** / **`amount_usdc`** / …)
  - directory UI still surfaced **Error: Expected 402 response** (hypothesis: stricter **`x402Version`** / **`accepts[]`** payload and/or **`PAYMENT-REQUIRED`** header expectations)
  - compatibility patch in-repo adds **`x402Version`**, **`accepts`** ( **`exact`** scheme ), **`maxAmountRequired`** (USDC 6 decimals), and **`PAYMENT-REQUIRED`** (standard base64 over compact `{x402Version,accepts}` JSON) plus **`Access-Control-Expose-Headers: PAYMENT-REQUIRED`** on **402** discovery responses — API-side only
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — third attempt (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (“This URL only”)
- registration_status: **attempted_validation_failed_head_options** (no listing claimed)
- observed:
  - **GET** → **402** + legacy challenge + **`x402Version`** + **`accepts[]`** + **`PAYMENT-REQUIRED`** header (compat deploy live)
  - **HEAD** → **405** (**Allow** advertised **GET** only) — likely blocked validators probing **HEAD**
  - **OPTIONS** → **405** (**Allow** **GET**) — likely blocked **preflight** probes
  - directory UI **still**: **Error: Expected 402 response**
- reason_summary: **GET** schema/header compatibility **did not resolve** listing validation; diagnostics suggest **HEAD** / **OPTIONS** **405** as next probe gap — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` §3c for repository-side **HEAD 402** + **OPTIONS 204** compatibility (no deployment claim here)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — fourth diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (“This URL only”)
- registration_status: **attempted_validation_failed_requirements_schema** (no listing claimed)
- observed:
  - **GET** /**HEAD** → **402** + **`PAYMENT-REQUIRED`** + **`accepts[]`** (post method & header compatibility)
  - **OPTIONS** → **204** (post preflight compatibility)
  - directory UI **still**: **Error: Expected 402 response**
- reason_summary: Methods and transport headers **match** documented discovery probes; rejection likely driven by **exact-EVM requirement object** shape (**`asset`** as USDC **contract** on Base, **`amount`**, **`maxTimeoutSeconds`**, **`extra`**, etc.) — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` §3d (repo-side alignment; **no deployment claim** here)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — fifth diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (server logs show OpenAPI fetch + verb matrix)
- registration_status: **attempted_validation_failed_unsupported_methods** (no listing claimed)
- observed (VPS / access logs summary):
  - **GET** `/openapi.json` → **200**
  - **GET** **`/contracts/risk-score`** (including query probes) → **402**
  - **POST** **`/contracts/risk-score`** (unpaid path) → **402**
  - **HEAD** → **402**
  - **OPTIONS** → **204**
  - **PATCH** / **PUT** / **DELETE** → **405** (before all-method compatibility patch)
- reason_summary: Scanners exercised **unsupported methods**; **405** on **PATCH**/ **PUT**/ **DELETE** suspected as residual validation blocker — repo adds **402** challenge responses on those paths for discovery parity (**§3e**); **no deployment claim**
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — sixth diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (server access logs correlate with scanners)
- registration_status: **attempted_validation_failed_post_422** (no listing claimed)
- observed:
  - Majority of discovery verbs (**GET**, **HEAD**, **PATCH**, **PUT**, **DELETE**) → **402**; **OPTIONS** → **204** once compatibility patches landed
  - At least one **POST** to **`/contracts/risk-score`** returned **422 Unprocessable Entity**, attributed to unpaid body validation preceding the payment gate (pre-fix)
- reason_summary: Unpaid **POST** must return **402** challenge before mandatory JSON/schema validation — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` **§3f** (repo ordering change; **no deployment claim**)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — seventh diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (server logs show repeated `/openapi.json` fetch + internal path probes)
- registration_status: **attempted_validation_failed_openapi_internal_resources** (no listing claimed)
- observed:
  - **GET** `/openapi.json` → **200** (listed internal/health/webhook paths)
  - **GET** `/contracts/risk-score` → **402** (paid resource discovery OK)
  - Probes on OpenAPI-discovered **non-paid** paths (e.g. **`/internal/x402/status`**, **`/internal/x402/lanes`**, **`/health`**, **`/webhooks/*`**) → **200** or **405**, not **402**
- reason_summary: x402scan reached the server and the paid resource returned **402**, but public **OpenAPI** exposed internal non-paid resources that failed the validator’s **402** expectation — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` **§3g** (public OpenAPI discovery filter; **no deployment claim**)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — eighth diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (source review + live probes)
- registration_status: **attempted_validation_failed_x402scan_v1_schema** (no listing claimed)
- observed:
  - HTTP/OpenAPI compatibility landed (**402** on paid resource, clean **`/openapi.json`**, **POST** prepayment **402**)
  - **x402scan** source indicates v1 tests expect **`accepts[0].network: "base"`**, top-level **`error`**, and top-level **`x402Version`/`accepts`** on **POST** (not only **`detail`**)
- reason_summary: Align unpaid challenge JSON and **`PAYMENT-REQUIRED`** with x402scan v1 schema while preserving legacy top-level **`network: eip155:8453`** — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` **§3h** (**no deployment claim**)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — ninth diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (UI + OpenAPI fetch)
- registration_status: **attempted_validation_failed_openapi_multiple_operations** (no listing claimed)
- observed:
  - Runtime **402**/**204** matrix compatible on **`/contracts/risk-score`**
  - **`/openapi.json`** listed **`get`**, **`head`**, **`options`**, **`post`** on the same path → UI **“Add API (4 resources)”**
  - Validation still **“Expected 402 response”**
- reason_summary: x402scan likely validates **each OpenAPI operation** as a resource; **HEAD**/**OPTIONS** are not payable x402 surfaces — reduce public OpenAPI to **POST only** — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` **§3i** (**no deployment claim**)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — tenth diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow
- registration_status: **attempted_validation_failed_post_body_shape** (no listing claimed)
- observed:
  - UI **one resource** (OpenAPI **POST** only) after **§3i**
  - Error **“No valid x402 response found (tried empty body and OpenAPI-derived sample body)”**
  - **GET** flat v1 challenge OK; **POST** unpaid had nested **`detail`** duplicate
- reason_summary: Align unpaid **POST** response to the same flat v1 body as **GET** (no **`detail`**) for empty and OpenAPI sample probes — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` **§3j** (**no deployment claim**)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — eleventh diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow
- registration_status: **attempted_validation_failed_post_extra_fields** (no listing claimed)
- observed:
  - **One resource** in UI; unpaid **POST** **402** with flat v1 + no **`detail`**
  - Still **“No valid x402 response found”** (empty + OpenAPI sample probes)
  - Suspected: legacy keys on **POST** body beyond **`x402Version` / `error` / `accepts`**
- reason_summary: Reduce unpaid **POST** challenge to pure v1 shape; **GET** keeps legacy fields — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` **§3k** (**no deployment claim**)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — twelfth diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (source + live probes)
- registration_status: **attempted_validation_failed_accepts_schema** (no listing claimed)
- observed:
  - **One resource**; pure **POST** v1 top-level body
  - Still **“No valid x402 response found”**
  - Source review: v1 examples omit **`accepts[0].amount`** and include **`outputSchema.input`**
- reason_summary: Align **`accepts[]`** to strict v1 shape — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` **§3l** (**no deployment claim**)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — thirteenth diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (source inspection + live probes)
- registration_status: **attempted_validation_failed_missing_accept_amount** (no listing claimed)
- observed:
  - Pure **POST** v1 + **`outputSchema`** landed; **`accepts[0].amount`** omitted per schema-only examples
  - **x402scan** **`check-endpoint`** reads **`accept.amount`** when building **`paymentMethods`**
  - Still **“No valid x402 response found”**
- reason_summary: Restore **`accepts[0].amount`** alongside **`maxAmountRequired`** while keeping pure **POST** body — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` **§3m** (**no deployment claim**)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## x402scan directory registration — fourteenth diagnosis (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com manual listing flow (@agentcash/discovery source review)
- registration_status: **attempted_validation_failed_v1_header_conflict** (no listing claimed)
- observed:
  - One resource; pure **POST** v1 JSON with **`amount`** + **`outputSchema`**
  - **`PAYMENT-REQUIRED`** header carried **v1** payload; discovery treats header as **v2-only**
  - Body parse skipped → no **`paymentOptions`** → **“No valid x402 response found”**
- reason_summary: Omit **`PAYMENT-REQUIRED`** on **v1** **402** responses (body-first) — see `docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md` **§3n** (**no deployment claim**)
- listing_success_claim: false
- partnership_claim: false
- endorsement_claim: false
- integration_claim: false

## Agentic.Market submission — prepared (v12.x)

- target: Agentic.Market (https://agentic.market)
- status: **prepared_not_submitted** (superseded by manual attempt below)
- owner: Chox
- source_pack: `docs/17_growth/AGENTIC_MARKET_SUBMISSION_PACK.md`
- x402scan_proof_available: true
- x402scan_proof_url: https://beezshield.com/registry/x402scan.html
- manual_submission_required: true
- notes: No traditional listing form on site; discovery is Bazaar-indexed per seller FAQ

## Agentic.Market directory submission — manual attempt (v12.x)

- recorded_date: 2026-05-19
- owner: Chox
- status: **submitted_pending** (seller validator run; **not** `listed_verified`)
- channel: https://agentic.market/validate (Seller Tools — Bazaar indexer path; no separate copy/paste listing form found)
- validator_url: https://agentic.market/validate?url=https%3A%2F%2Fapi.beezshield.com%2Fcontracts%2Frisk-score
- marketplace_search: `https://agentic.market/?q=beezshield` → **0 results** (not listed yet)
- screenshot: `docs/17_growth/evidence/agentic-market-validate-2026-05-19.png`
- submission_result: **Implementation Invalid** — 4 checks failed (GET probe). Failures include: missing v2 top-level `resource`; `x402Version` is 1 (validator expects 2); v2 `PAYMENT-REQUIRED` header (current API uses v1 body-first for x402scan); missing `extensions.bazaar`. **Do not change API in this step** — x402scan compatibility preserved.
- prepared_copy_fields_used (for future Bazaar/metadata if requested):
  - product_name: BeezShield Sentinel Alpha
  - category: Agent Security / Web3 / x402 / Onchain Risk
  - website: https://beezshield.com/
  - api_endpoint: https://api.beezshield.com/contracts/risk-score
  - proof: https://beezshield.com/registry/x402scan.html
  - x402scan_listing: registered (directory only); resource API https://api.beezshield.com/contracts/risk-score
  - npm: @beezshield/sentinel (https://www.npmjs.com/package/@beezshield/sentinel)
  - pricing: 0.02 USDC basic lane on Base USDC
  - claim_posture: directory registration only; no partnership; no guarantee
- listing_url: null
- official_integration_claim: false
- partnership_claim: false
- endorsement_claim: false
- security_guarantee_claim: false
- listing_success_claim: false
- notes: Await Bazaar indexing / v2+bazaar compatibility work before `listed_verified`. Next: re-validate with POST after indexer docs review; do not claim Agentic.Market partnership.

## Agentic.Market — Bazaar v2 validator pass (62c0b1f, 2026-05-19)

- recorded_date: 2026-05-19
- owner: Chox
- status: **validator_passed_not_listed**
- deploy_commit: `62c0b1f` (HTTP `info.input` shape on production)
- channel: https://agentic.market/validate
- validator_url: https://agentic.market/validate?url=https%3A%2F%2Fapi.beezshield.com%2Fcontracts%2Frisk-score-v2&method=POST
- target_endpoint: https://api.beezshield.com/contracts/risk-score-v2
- production_unpaid_post_status: **402** (`x402Version: 2`, `PAYMENT-REQUIRED` == body)
- production_bazaar_info: `toolName`; `input.type` **http**; `input.method` **POST**; `bodyType` **json**; `body` example; `output.example`
- validator_ui_result: **Implementation Looks Correct** — all checks pass; needs first verify+settle for Bazaar indexing
- marketplace_search: https://agentic.market/?q=beezshield → **0 results**
- listing_url: null
- screenshot: `docs/17_growth/evidence/agentic-market-validate-v2-http-shape-pass-2026-05-19.png`
- v1_unchanged: POST `/contracts/risk-score` body-first v1, no `PAYMENT-REQUIRED`
- official_integration_claim: false
- partnership_claim: false
- endorsement_claim: false
- security_guarantee_claim: false
- listing_success_claim: false
- notes: Do not use `listed_verified` without public listing URL; trigger Bazaar indexing via first paid verify+settle when ready

## Agentic.Market — Bazaar v2 production verify (b57330a, 2026-05-19)

- status: superseded
- validator_ui_result: **Implementation Invalid** — SDK Parse Error (pre-`62c0b1f`)
- screenshot: `docs/17_growth/evidence/agentic-market-validate-v2-b57330a-2026-05-19.png`

## Agentic.Market — Bazaar v2 validator attempt pre-deploy (2026-05-19)

- status: superseded
- production_unpaid_post_status: **404**
- screenshot: `docs/17_growth/evidence/agentic-market-validate-v2-2026-05-19.png`

## x402scan directory registration — success (v12.x)

- target_url: `https://api.beezshield.com/contracts/risk-score`
- channel: x402scan.com — `/resources/register`
- registration_status: **registered**
- submitted_resource: `https://api.beezshield.com/contracts/risk-score`
- owner: Chox
- evidence: **Registration Complete** / **Successfully registered 1 of 1 resources**
- visible_title: `BeezShield | Pre-execution decision engine for agents`
- visible_path: `/contracts/risk-score`
- recorded_date: 2026-05-16
- official_integration_claim: false
- partnership_claim: false
- endorsement_claim: false
- security_guarantee_claim: false
- directory_registration_claim: true
- notes: Marketplace/directory registration only (not official integration/partnership/endorsement); prior attempts §3a–§3n preserved as history above; see `docs/17_growth/X402SCAN_REGISTRATION_EVIDENCE.md`

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

## ReaWorks — Trust Receipt $25 outside review (v13.x)

| Field | Value |
| --- | --- |
| **status** | **packet_sent_pending_review_payment** |
| **recorded_date** | 2026-05-20 |
| **packet_sent_at** | 2026-05-20T12:00:00Z |
| **review_offer** | ReaWorks offered **$25** outside review of one draft Sentinel/AgentKit run |
| **files_sent** | `docs/17_growth/REAWORKS_REVIEW_PACKET_001.md` |
| | `docs/17_growth/fixtures/trust_receipt_reaworks_review_packet_001.redacted.json` |
| **receipt_id** | `reaworks-review-packet-001` |
| **payment_received** | **not confirmed** |
| **review_completed** | **not confirmed** |
| **revenue_confirmed** | **false** |
| **paid_customer_claim** | **false** |
| **partnership_claim** | **false** |
| **integration_claim** | **false** |
| **endorsement_claim** | **false** |
| **security_guarantee_claim** | **false** |
| **notes** | Packet prepared and sent for external review; awaiting **$25 payment** and written review outcome. Do not claim paid customer, partnership, integration, endorsement, or revenue until separately verified. |
