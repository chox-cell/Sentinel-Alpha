# ABI/Source Provider Activation Plan v1

## 1) Purpose

Plan for future ABI/source provider activation.
Not active now.

This is a planning and gate artifact only. It does not activate providers, does not require keys, and does not change runtime defaults.

## 2) Current status

- ABI/source adapter boundary exists.
- Local fixture mode exists.
- No live provider configured by default.
- No API key required by default.
- No external provider call is made by baseline runtime.

## 3) Why ABI/source first

- improves contract classification
- improves function hinting
- improves ERC20/NFT/router/pool heuristics
- improves confidence reasoning
- lower risk than simulation/mempool provider activation

## 4) Candidate providers (candidates only)

- Basescan
- Etherscan
- Blockscout
- Sourcify

Current posture:

- no provider selected yet
- no provider integrated live
- no paid plan approved

## 5) Activation requirements

- explicit founder approval
- provider selected
- cost reviewed
- `.env.example` placeholders only
- real keys stay only in `.env` or secret manager, never repo
- timeout tests
- rate-limit tests
- invalid response tests
- provider-down fallback tests
- confidence reduction when provider unavailable
- no top-level schema break
- one-flag disable
- rollback plan

## 6) Required config flags (future placeholders only)

- `SENTINEL_ABI_SOURCE_PROVIDER_ENABLED=false`
- `SENTINEL_ABI_SOURCE_PROVIDER_NAME=`
- `SENTINEL_ABI_SOURCE_PROVIDER_TIMEOUT_MS=`
- `BASESCAN_API_KEY=`
- `ETHERSCAN_API_KEY=`
- `SOURCIFY_ENABLED=false`

These are future placeholders, not required now.

## 7) Runtime behavior when disabled

- `source_provider_status`: `disabled` / `not_configured`
- `abi_available`: `unknown`
- `verified_source_status`: `unknown`
- `fallback_mode`: `true`
- `confidence_impact` reflects unavailable source context

## 8) Privacy/security

- never log API keys
- never store raw auth headers
- never store secrets
- cache only sanitized ABI/source metadata
- no private keys/seed phrases/payment signatures

## 9) Public claim controls

Allowed:

- "ABI/source provider boundary exists"
- "local fixture ABI context is supported"
- "live provider activation is planned behind explicit gates"

Forbidden:

- "live ABI coverage"
- "full verified-source coverage"
- "guaranteed source verification"
- "detects honeypots"
- "guaranteed protection"

## 10) Rollback plan

- disable one flag
- return to local fixture / unknown state
- confidence reduction
- preserve API compatibility

## 11) Decision record template

- provider_name
- provider_url
- free_or_paid
- monthly_budget
- enabled_flag
- fallback_behavior
- tests_required
- approved_by
- approved_at
- rollback_owner

## 12) v9.7 fake backend contract tests

- Before any real provider activation, ABI/source boundary behavior must pass fake backend contract tests.
- Fake backend scenarios validate success and failure behavior without live providers, API keys, network calls, or paid plans.
- Required fake backend scenarios:
  - `success_verified_source`
  - `success_abi_only`
  - `timeout`
  - `rate_limited`
  - `invalid_response`
  - `provider_down`
  - `unsupported_chain`
- Failure modes must force fallback mode and confidence reduction behavior.
- This does not enable live provider integration.
- No API keys required for fake backend contract tests.

## 13) v9.8 disabled wiring skeleton

- A disabled-by-default ABI/source provider wiring skeleton exists for future activation readiness.
- Skeleton status/config wiring can report `disabled`, `not_configured`, `unsupported_provider`, or `adapter_ready`.
- Live provider calls remain disabled in skeleton mode.
- No API keys are required by default.
- Future activation still requires explicit founder approval and a completed decision record.
