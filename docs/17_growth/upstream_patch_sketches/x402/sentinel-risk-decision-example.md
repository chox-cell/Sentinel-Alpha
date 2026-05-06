# Sentinel Risk Decision Example for x402 (Optional)

This is an optional example only for a docs-style upstream patch sketch.
It is not submitted upstream.

Target issue URL: https://github.com/x402-foundation/x402/issues/2198

## Pattern

Use x402-gated API flow + pre-execution risk decision before sensitive contract actions.

1. Handle payment challenge path in builder logic.
2. Call Sentinel decision endpoint (`/contracts/risk-score`) via `@beezshield/sentinel`.
3. Route result to allow/review/block.

## Safety wording

- optional example only
- no live simulation claim
- no guaranteed protection claim
- regression evidence only, not a security guarantee
- not submitted upstream
