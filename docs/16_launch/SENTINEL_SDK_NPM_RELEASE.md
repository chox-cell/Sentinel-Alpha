# Sentinel SDK npm Release Verification (v3.8.2)

## Release status
- Package: `@beezshield/sentinel`
- Version: `0.1.0`
- npm status: **published**
- Verification timestamp (UTC): `2026-05-04 12:10:46Z`

## npm registry verification
Commands used:
- `npm view @beezshield/sentinel version`
- `npm view @beezshield/sentinel name version description homepage`

Observed:
- `version = 0.1.0`
- `name = @beezshield/sentinel`
- `description = Official BeezShield Sentinel Alpha TypeScript SDK for pre-execution smart-contract risk decisions`
- `homepage = https://beezshield.com`

## install verification (fresh temp project)
Commands used:
- `npm init -y`
- `npm install @beezshield/sentinel`
- `node -e "import('@beezshield/sentinel').then(m => console.log(Object.keys(m)))"`

Install/import succeeded and visible exports included:
- `createSentinelClient`
- `scoreContract`
- `decideBeforeExecution`
- `isX402Challenge`
- `normalizeSentinelDecision`
- `SentinelPaymentRequiredError`
- `SentinelValidationError`
- additional typed errors/helpers

## product-truth notes
- AgentKit provider integration is **not live** in this SDK (coming next).
- x402 settlement is **not automatic**; callers must provide settlement headers when available.
- This document records verification only; it does not perform another publish.

## release process guardrail
- Any next npm release requires a semantic version bump (for example `0.1.1` or higher) before publishing.
