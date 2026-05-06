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
