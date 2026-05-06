# PR Draft Pack: elizaOS/eliza (Issue #7396)

## 1) Purpose

Prepare an optional tiny PR draft for elizaOS maintainers. This is local planning only.

## 2) Target issue URL

- https://github.com/elizaOS/eliza/issues/7396

## 3) Proposed tiny change

- Add an optional middleware-style snippet for pre-execution risk decision checks.
- Keep it as a docs/example improvement, not a runtime requirement.

## 4) Example code snippet using @beezshield/sentinel

```ts
import { createSentinelClient } from "@beezshield/sentinel";

const sentinel = createSentinelClient({ lane: "basic" });

export async function preExecutionGuard(contractAddress: string) {
  const decision = await sentinel.decideBeforeExecution({
    contract_address: contractAddress,
    chain: "base",
  });

  // allow / review / block
  return {
    route: decision.recommendation,
    score: decision.score,
  };
}
```

## 5) README/docs snippet

Optional example: add a pre-execution risk decision gate before agent-triggered contract calls and route behavior to allow / review / block.
Install with `npm install @beezshield/sentinel`.

## 6) Safety wording

- AgentKit-style example available.
- official provider coming next.
- local fixture evaluation is 8 fixtures / 8 passed / 0 review; regression evidence only, not a security guarantee.

## 7) Non-goals

- no claim of shipped upstream adoption
- no claim of shipped provider integration
- no claim of certainty for trap detection outcomes
- no claim of MEV blocking outcomes
- no claim of guaranteed safety outcomes

## 8) Exact files that would be changed in upstream if approved

- `README.md` (optional integration pattern paragraph)
- `docs/` or `examples/` area (optional snippet)

## 9) Status

Not submitted yet.
