# Outreach Target Verification Pack (v7.1)

## 1) Purpose

This pack defines target research structure for the first outreach batch.
This is research only; no outreach has been performed in this step.

## 2) Verification standard

Each target row must include:

- target_id
- project_name
- source_url
- category
- evidence_observed
- why_relevant
- proposed_message_angle
- risk_of_mismatch
- status: not contacted
- notes

## 3) Source rules

- GitHub repo, docs page, hackathon page, npm package, or official site required.
- No target without source_url.
- No status beyond not contacted unless real outreach happens.
- No integrated status without merged PR or public proof.

## 4) Evidence-safe target template

Use source-required placeholder rows. Replace only when evidence is verifiable.

| target_id | project_name | source_url | category | evidence_observed | why_relevant | proposed_message_angle | risk_of_mismatch | status | notes |
|---|---|---|---|---|---|---|---|---|---|
| T01 | Coinbase AgentKit | https://github.com/coinbase/agentkit | AgentKit/Base builders | Repository title and description indicate AgentKit wallet tooling for AI agents. | Strong alignment with AgentKit-style builders and Base-adjacent agent flows. | Share pre-execution risk decision layer + optional PR + AgentKit-style example available; official provider coming next. | May already have internal risk patterns; integration priority unknown. | not contacted | Evidence captured from public GitHub repo page. |
| T02 | Coinbase x402 | https://github.com/coinbase/x402 | x402 builders | Repository description states payments protocol built on HTTP. | Direct fit for x402-gated API conversations and payment-aware integration paths. | Position Sentinel policy assistance around `/contracts/risk-score` and explicit x402 handling in builder code. | x402 scope may focus on protocol infra rather than contract execution safety. | not contacted | Evidence captured from public GitHub repo page. |
| T03 | Zora Developer Docs | https://docs.zora.co/ | Zora/Base asset tools | Docs homepage highlights developer tools and agent-ready skills for Zora. | Relevant to asset-tool builders that may add safety checks before contract calls. | Share conservative contract/asset execution safety posture and optional PR path. | Zora docs represent ecosystem surface, not a single repository owner for outreach. | not contacted | Evidence captured from public docs page. |
| T04 | modelcontextprotocol/servers | https://github.com/modelcontextprotocol/servers | MCP tool servers on Base | Repository is a public MCP server index and contribution hub. | Useful entry point for identifying Base-related tool/server maintainers for future scoped outreach. | Offer Sentinel as policy-assist layer for execution-capable MCP workflows. | Repository is broad and multi-domain; Base-specific fit varies by subproject. | not contacted | Evidence captured from public GitHub repo page. |
| T05 | Safe Core SDK | https://github.com/safe-global/safe-core-sdk | wallet automation projects | Repository description indicates account abstraction SDK for app builders. | Wallet automation and account-abstraction flows can benefit from pre-execution policy checks. | Position review/block/allow assistance before automated contract interactions. | Project priorities may center on account infra rather than external risk decision APIs. | not contacted | Evidence captured from public GitHub repo page. |
| T06 | Coinbase OnchainKit | https://github.com/coinbase/onchainkit | AgentKit/Base builders | Repository description indicates React components and TypeScript utilities for onchain apps. | Builder audience overlaps with Base/onchain app developers evaluating execution safety layers. | Pair SDK install path with AgentKit-style example available and official provider coming next. | Toolkit focus may be UI/developer experience rather than bot automation. | not contacted | Evidence captured from public GitHub repo page. |
| T07 | elizaOS/eliza | https://github.com/elizaOS/eliza | security-minded bot builders | Repository describes autonomous agents framework and active OSS collaboration. | Agent developers may value explicit risk gating before autonomous contract calls. | Share guardians-not-traders framing with regression-evidence-only positioning. | Not Base-specific by default; relevance depends on each deployment's chain targets. | not contacted | Evidence captured from public GitHub repo page. |
| T08 | — placeholder — | REQUIRED_URL | MCP trading/tool servers on Base | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T09 | — placeholder — | REQUIRED_URL | x402 builders | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T10 | — placeholder — | REQUIRED_URL | Zora/Base asset tools | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T11 | — placeholder — | REQUIRED_URL | wallet automation projects | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T12 | — placeholder — | REQUIRED_URL | security-minded bot builders | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T13 | — placeholder — | REQUIRED_URL | AgentKit/Base builders | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T14 | — placeholder — | REQUIRED_URL | MCP trading/tool servers on Base | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T15 | — placeholder — | REQUIRED_URL | x402 builders | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T16 | — placeholder — | REQUIRED_URL | Zora/Base asset tools | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T17 | — placeholder — | REQUIRED_URL | wallet automation projects | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T18 | — placeholder — | REQUIRED_URL | security-minded bot builders | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T19 | — placeholder — | REQUIRED_URL | AgentKit/Base builders | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |
| T20 | — placeholder — | REQUIRED_URL | x402 builders | pending research | pending research | pending research | unknown until verified | not contacted | replace only with verifiable evidence |

If adding real targets later, include source URL and conservative evidence only.

## 5) Batch 1 target categories

- AgentKit/Base builders
- MCP trading/tool servers on Base
- x402 builders
- Zora/Base asset tools
- wallet automation projects
- security-minded bot builders

## 6) Message angle safety

Use:

- pre-execution risk decision layer
- optional PR
- AgentKit-style example
- official provider coming next
- local fixture evaluation as regression evidence only

Avoid:

- any protection guarantee wording
- universal honeypot certainty wording
- MEV blocking/prevention wording
- live simulation wording
- full contract-type coverage wording

Evidence line:

Current local fixture evaluation covers 8 Base fixture patterns with 8 passed / 0 review. This is regression evidence, not a security guarantee.

## 7) Tracker sync

`OUTREACH_TRACKER.md` must remain not contacted.
If adding target IDs/details later, preserve not contacted status until real outreach occurs.
