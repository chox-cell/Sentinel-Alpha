# ERC-8004 Registration Proof Pack v2.6

## Registration Summary
- Product agent: `Sentinel Alpha`
- Umbrella brand: `BeezShield`
- Identity status: `erc8004_registered`
- Registry: `8004scan`

## Registration Proof
- Agent URL: `https://8004scan.io/agents/base/45967`
- Agent ID: `45967`
- Network: `Base`
- Chain ID: `8453`

## Production API
- Public base URL: `https://api.beezshield.com`
- Endpoint: `/contracts/risk-score`
- Full endpoint: `https://api.beezshield.com/contracts/risk-score`

## Payment Support
- Method: `x402`
- Network: `eip155:8453` (`Base`)
- Tiers (USDC):
  - `basic`: `0.02`
  - `executive`: `0.05`
  - `premium`: `0.10`
  - `priority`: `0.15`

## Proof Checklist
- [x] `identity-manifest.json` set to `erc8004_registered`
- [x] Agent ID set to `45967`
- [x] 8004scan URL included in market JSON files
- [x] README includes Agent ID and 8004scan URL
- [x] No fake MCP/A2A claims introduced
- [x] No `/contracts/risk-score` schema changes
- [x] No runtime behavior changes
