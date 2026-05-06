# Sentinel Pre/Post Agent Action Loop (v8.1)

## 1) Purpose

This is a local reference architecture only:
Sentinel pre-check + AgentKit execution + post-execution trail.
It is not an official AgentKit integration and not a Mycelium Trails integration.

## 2) Boundary split

- Sentinel asks: should this agent act?
- Execution layer asks: perform the action.
- Trail layer asks: what happened and can it be verified?

## 3) Reference flow

1. agent prepares action
2. Sentinel risk-check returns allow/review/block
3. if allowed by policy, execution layer proceeds
4. post-action trail records `agent_id` / `action` / `payment_hash` / `claims` / `timestamp` / `signature`
5. verifier can inspect pre-decision context and post-action proof

## 4) Non-goals

- no official AgentKit integration
- no Mycelium Trails integration
- no partnership
- no wallet execution
- no signing
- no security guarantee
- no live simulation claim

## 5) Context notes

- AgentKit issue URL: https://github.com/coinbase/agentkit/issues/1168
- Community signal observed from giskard09 in issue discussion.
- Mycelium Trails demo URL was externally mentioned by responder:
  https://argentum.rgiskard.xyz/trails/demo
- Mention is context only and not an integrated dependency claim.
- Composability reference draft:
  `docs/17_growth/COMPOSABILITY_REFERENCE_DRAFT.md`
- The composability draft is documentation-only and does not imply partnership/integration.
