# PR Draft Pack: x402 Foundation (Issue #2198)

## 1) Purpose

Prepare an optional tiny PR draft for x402 maintainers. This is local planning only.

## 2) Target issue URL

- https://github.com/x402-foundation/x402/issues/2198

## 3) Proposed tiny change

- Add an optional "pre-execution risk decision" example section for builders running contract actions.
- Keep it docs/example-only and non-blocking.

## 4) Example code snippet using @beezshield/sentinel

```ts
import { createSentinelClient } from "@beezshield/sentinel";

const sentinel = createSentinelClient({ lane: "basic" });

const decision = await sentinel.decideBeforeExecution({
  contract_address: "0x1111111111111111111111111111111111111111",
  chain: "base",
});

// optional example policy routing:
// allow / review / block
if (decision.recommendation === "allow") {
  // proceed
} else if (decision.recommendation === "review") {
  // manual review path
} else {
  // block path
}
```

## 5) README/docs snippet

Optional example: before executing a high-risk contract action, call Sentinel for a pre-execution risk decision and route to allow / review / block policy handling.
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

- `README.md` (new optional integration subsection)
- `examples/` docs or sample note (if maintainers want example placement)

## 9) Status

Not submitted yet.
