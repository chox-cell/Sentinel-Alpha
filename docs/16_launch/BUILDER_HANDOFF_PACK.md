# Builder Handoff Pack v3.3

## Funnel: Website -> cURL -> SDK -> AgentKit
1. Website scan UI demonstrates end-to-end decision flow.
2. Builder copies generated cURL request and runs local validation.
3. Builder moves to SDK snippets (TypeScript/Python) for production wiring.
4. AgentKit is noted as upcoming integration for richer orchestration workflows.

## How a Builder Integrates Sentinel Alpha
- Start with `POST https://api.beezshield.com/contracts/risk-score`
- Add required headers:
  - `Content-Type: application/json`
  - `X-SENTINEL-LANE`
  - `X402-PAYMENT`
- Send payload with `contract_address` and `chain: base`
- Parse `score`, `confidence`, `action`, `emergency_signal`, `attestation` into execution policy logic.

## Pricing Lanes (USDC)
- basic: 0.02
- executive: 0.05
- premium: 0.10
- priority: 0.15

## ERC-8004 Proof
- Agent ID: `45967`
- URL: `https://8004scan.io/agents/base/45967`

## Public Links
- Website: `https://beezshield.com`
- API: `https://api.beezshield.com/contracts/risk-score`
- GitHub: `https://github.com/chox-cell/Sentinel-Alpha`
