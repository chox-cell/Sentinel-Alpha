# GitHub Issue Template (Builder Outreach)

## Title

Optional pre-execution risk gate for your bot (`@beezshield/sentinel`)

## Body

Hi team - quick note from BeezShield.

Sentinel Alpha is a pre-execution risk decision API/SDK for autonomous bot flows:
- call once before interacting with a contract
- receive `allow/review/block` style decision output
- enforce your own policy path in code

Quick try:

```bash
npm install @beezshield/sentinel
```

AgentKit-style example (not official provider):
- `examples/agentkit-sentinel`

If useful, we can open a small PR against your repo to add a non-invasive pre-execution gate.

Notes:
- official AgentKit provider wiring is coming next
- no safety overclaims
- x402 settlement is explicit (not automatic in SDK)
