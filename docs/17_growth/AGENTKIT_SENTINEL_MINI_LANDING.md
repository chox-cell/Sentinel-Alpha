# Sentinel Alpha for AgentKit — Prototype

Before an AgentKit-style agent touches a contract or asset, ask Sentinel for an allow/review/block risk decision.

## What exists now

- local Action Provider-style prototype
- npm SDK: `@beezshield/sentinel`
- demo script: `npm run demo`
- sample output fixture: `examples/agentkit-sentinel-provider/examples/sample-output.json`
- issue URL: https://github.com/coinbase/agentkit/issues/1168

## How it works

`contract_address` -> Sentinel risk decision -> allow/review/block -> optional policy gate

## How to run locally

```bash
cd examples/agentkit-sentinel-provider
npm install
npm run demo
```

## Sample output

Reference file:

`examples/agentkit-sentinel-provider/examples/sample-output.json`

Compact excerpt:

```json
{
  "action": "review",
  "reason": "Conservative sample: confidence is not high enough for automatic allow path.",
  "confidence": "medium",
  "explanation": ["Sample fixture output for local demo documentation."],
  "notSecurityGuarantee": true
}
```

## Boundaries

- prototype only
- not an official Coinbase AgentKit provider
- not submitted upstream
- no wallet execution
- no transaction signing
- no CDP/provider keys required
- no live simulation claim
- not a security guarantee

## Possible next step

If maintainers want it, reduce into a smaller docs/example PR.
