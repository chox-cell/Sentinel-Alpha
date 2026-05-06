# Sentinel AgentKit Provider Prototype (v8.0)

## Purpose

Define a local Action Provider-style prototype for Sentinel risk checks in AgentKit-oriented flows.

## What is live

- `@beezshield/sentinel` npm SDK is live.
- AgentKit-style example exists in-repo.
- Sentinel `/contracts/risk-score` API is live.

## What is not live

- Official Coinbase AgentKit provider is not live.
- This prototype is not submitted upstream.
- This prototype is not runtime-integrated in Coinbase AgentKit.
- Local demo script is example-only policy assistance, not wallet execution/signing.

## allow/review/block mapping

The prototype action function calls Sentinel `decideBeforeExecution(...)` and maps output to:

- `allow`
- `review`
- `block`

It returns a structured response with `notSecurityGuarantee: true`.
An illustrative local sample output fixture is included under
`examples/agentkit-sentinel-provider/examples/sample-output.json`.
This fixture is sample-only and not live scan proof.

## Upstream path later

If maintainers request it, this prototype can be converted into a tiny docs/example PR.
Current tracking issue URL: https://github.com/coinbase/agentkit/issues/1168

## Safety constraints

- no official provider claim
- no wallet execution/signing in prototype
- no live simulation claim
- no honeypot detection claim
- no guaranteed protection claim
- no provider key or CDP key requirement for demo sketch usage
