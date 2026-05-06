# PR Draft Pack: Coinbase AgentKit (Issue #1168)

## 1) Purpose

Prepare an optional tiny PR draft for AgentKit ecosystem maintainers. This is local planning only.

## 2) Target issue URL

- https://github.com/coinbase/agentkit/issues/1168

## 3) Proposed tiny change

- Add an optional agent-action guard example that calls Sentinel before contract execution.
- Keep this as a lightweight docs/example addition.

## 4) Example code snippet using @beezshield/sentinel

```ts
import { createSentinelClient } from "@beezshield/sentinel";

const sentinel = createSentinelClient({ lane: "basic" });

export async function guardContractAction(contractAddress: string) {
  const decision = await sentinel.decideBeforeExecution({
    contract_address: contractAddress,
    chain: "base",
  });

  // allow / review / block routing
  return decision.recommendation;
}
```

## 5) README/docs snippet

Optional example: run a pre-execution risk decision step before autonomous contract actions, then route to allow / review / block behavior.
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

- `README.md` (optional integration note)
- `examples/` (optional guard helper snippet)

## 9) Status

Not submitted yet.
