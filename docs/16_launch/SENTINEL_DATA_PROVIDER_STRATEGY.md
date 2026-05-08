# Sentinel data provider strategy (v6.0)

This strategy explains how Sentinel adds real data providers progressively while keeping pre-revenue cost discipline.

Roadmap status source of truth: `docs/00_project/SENTINEL_ALPHA_ROADMAP_TRACKER.md`.

## 1) Data Ladder

| Level | Stage | Purpose | Cost posture |
|---|---|---|---|
| Level 0 | current local/VPS/free mode | Existing production baseline with conservative metadata boundaries | Keep <= $10/month target |
| Level 1 | ABI/source feed | Add verified source and ABI context inputs | Prefer free/public sources first |
| Level 2 | local bytecode analysis | Deepen signal extraction without paid external analyzers | Run locally on current VPS where possible |
| Level 3 | local Postgres historical database | Durable, queryable history for scans/signals/outcomes | Local Postgres first; no managed DB by default |
| Level 4 | simulation provider adapter | Enable real simulation evidence path behind adapter boundary | No paid simulation provider until demand/revenue |
| Level 5 | mempool/MEV feed | Add pending activity and MEV pressure context signals | No paid mempool feed by default |

## 2) Provider categories

- RPC providers
- ABI/source providers
- simulation providers
- mempool/feed providers
- database/storage providers

## 3) Low-cost policy

- no paid QuickNode by default
- no managed Postgres by default
- no paid simulation provider by default
- no paid mempool stream by default
- use public/free/Base-first providers until usage justifies upgrade

## 4) Upgrade triggers

Upgrade from free/local mode only when one or more triggers occur:

- paid scans exist (revenue-backed infra decisions)
- repeated scans require stronger durability/performance
- provider failures materially affect reliability or UX
- integration demand requires richer data depth
- simulation is requested by users and backed by budget

## 5) Recommended order

- v6.1 local bytecode analyzer first
- v6.2 ABI/source adapter
- v6.3 local Postgres schema
- v6.4 Source/ABI cache boundary (disabled by default)
- v6.5 simulation provider adapter
- v6.6 mempool feed adapter

## 6) Public-safe wording

- data-provider-ready
- bytecode signal analyzer
- simulation adapter boundary
- mempool readiness
- no claim of live paid provider integration unless enabled

## 7) v6.4 Source / ABI cache boundary posture

- v6.4 adds Source / ABI Cache Boundary for future lookup deduplication.
- cache is disabled by default.
- Redis is not required by default.
- DATABASE_URL is not required by default.
- managed Redis remains postponed by default.
- later cache backends can be local Redis or local Postgres only after explicit approval.
- no secrets/API keys/raw headers are cached.

## 8) v6.5 simulation provider adapter boundary posture

- v6.5 adds simulation provider adapter boundary.
- disabled by default.
- no Tenderly or paid provider key is required by default.
- no wallet/private key/signing is allowed in boundary mode.
- no live simulation claim.
- no honeypot detection claim.
- activation later requires explicit budget approval, provider selection, and dedicated tests.

## 9) v6.6 local fixture evaluation harness posture

- v6.6 adds local fixture evaluation harness over Base fixture dataset.
- evaluation is local/offline only (no network/provider dependency).
- results are regression checks, not security guarantees.
- does not prove honeypot detection.
- does not prove full bytecode coverage.

## 10) v6.7 provider decision gate posture

- v6.7 adds strict provider activation policy guardrails.
- policy is documented in `docs/16_launch/SENTINEL_PROVIDER_DECISION_GATE.md`.
- no provider is activated by this step.
- default remains no paid providers.
- activation requires explicit founder approval, cost estimates, fallback tests, and rollback readiness.

## 11) ABI/source activation plan posture (v9.6)

- ABI/source activation planning is documented in
  `docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md`.
- this is gate/planning only; no live provider activation.
- no paid providers by default remains unchanged.
- real provider activation must pass fake backend contract tests first.

## 12) ABI/source wiring skeleton posture (v9.8)

- v9.8 adds disabled-by-default provider wiring skeleton/status for ABI/source lookup.
- this is additive skeleton wiring only; live provider calls remain disabled.
- runtime defaults remain unchanged and no API key is required by default.
