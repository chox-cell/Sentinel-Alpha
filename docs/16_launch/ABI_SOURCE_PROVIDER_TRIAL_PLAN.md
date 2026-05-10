# Controlled Free ABI/Source Provider Trial Plan v1

## 2) Purpose

Plan a future controlled trial for ABI/source lookup. This document is planning and gating only. The trial is **not active now**. It does not enable providers, does not require API keys for baseline development, does not change runtime defaults, and does not perform network calls by itself.

## 3) Current status

- Provider wiring skeleton exists (`abi_source_provider_config` boundary; disabled by default).
- `.env.example` placeholders exist; keys are optional and not committed.
- No provider enabled by default (`SENTINEL_ABI_SOURCE_PROVIDER_ENABLED=false`).
- No API keys required now for development or tests.
- No live provider calls are performed in the default runtime path.

## 4) Candidate ranking

Rank candidates for the first controlled trial:

1. **Sourcify** — Preferred first: source-verification oriented; can reduce reliance on per-explorer API keys for many flows.
2. **Blockscout** — Useful when a stable Base-compatible or instance endpoint is available and policy allows read-only use.
3. **Basescan** — Strong Base alignment; requires strict API-key discipline; defer until trial process is proven.
4. **Etherscan** — Broad coverage; requires strong API-key discipline and rate/tier awareness; defer until after Sourcify/Blockscout evaluation.

Rationale summary:

- Sourcify is preferred first because it is source-verification oriented and can reduce API-key dependency compared with explorer-first flows.
- Blockscout may be useful if a stable Base-relevant endpoint exists and terms allow read-only access.
- Basescan and Etherscan require stronger API-key discipline and should come later in the ladder.

## 5) Trial scope

- At most 5 known Base-chain contract addresses (fixture-known or explicitly approved list).
- Read-only lookup only (no writes, no mutations, no submissions).
- Request timeout **≤** configured `SENTINEL_ABI_SOURCE_PROVIDER_TIMEOUT_MS` (default placeholder in `.env.example`; not increased by this plan).
- **No retries** beyond an explicit small cap (e.g., zero or one retry only if documented and approved); no exponential backoff spam.
- **No paid calls**; trial must remain within free/public terms for the chosen provider.
- **No persistence by default** (no receipt store activation, no cache persistence, no DB writes for trial outputs).
- **No user-facing guarantee claims** tied to trial results.
- Fallback to unknown on failure (provider down, rate limit, timeout, invalid payload), with conservative confidence impact.

## 6) Trial success criteria

- Obtain a successful verified-source **or** ABI response for at least one known contract in scope.
- Timeout handling behaves as expected (degraded metadata, no hang).
- Invalid response handling behaves as expected (fallback, no crash, no schema break).
- Rate-limit handling behaves as expected (fallback, no retry storm).
- Provider-down fallback behaves as expected (safe unknown path).
- No top-level response schema break for API consumers.
- Confidence impact remains **conservative** (no overconfidence when data is partial).

## 7) Trial failure criteria

Immediate stop or rollback if any occur:

- Any secret leak (keys, headers, tokens) in logs, metadata, or stored artifacts.
- `.env` mutation by automation or undocumented writes.
- Paid-provider requirement to complete the trial (trial must remain free-tier/public per plan).
- Blocking runtime dependency on provider success (service must remain usable when provider fails).
- Unsafe positive claims in public copy (see section 10 — Public claim controls).
- No fallback path on provider failure (system must not assume success).

## 8) Required approval

- **Explicit founder approval** before enabling any live-provider flag or running live calls against external endpoints.
- **Provider decision record** completed (template in section 11), including scope and limits.
- **Rollback owner** assigned (name/contact documented in the decision record).
- **Test evidence** recorded (e.g., fake backend contract tests green; trial run notes; no repo secret commits).

## 9) Rollback

- Disable with **one flag** (`SENTINEL_ABI_SOURCE_PROVIDER_ENABLED=false` and clear `SENTINEL_ABI_SOURCE_PROVIDER_NAME` / provider selection as applicable).
- Return to **disabled** or **not_configured** source-provider status in runtime metadata.
- Preserve **additive** metadata fields only; avoid breaking existing response keys.
- **No** top-level schema break; consumers should still parse prior shapes.

## 10) Public claim controls

**Allowed**

- A controlled provider trial is **planned**; execution is gated.
- ABI/source provider remains **disabled by default** in shipping defaults.
- Local fixtures and fake-backend contract tests exist for boundary validation.

**Forbidden** (do not publish or imply):

- That the product offers **comprehensive** ABI completeness across all live contracts (avoid completeness claims).
- That **all** contracts have verified source (avoid universal verified-source claims).
- That source verification is **assured** or **promised** (verification is third-party and partial).
- That the product reliably **labels malicious traps** onchain without scoped evidence (avoid trap-detection guarantees).
- That users receive **assured safety** or **promised protection** outcomes.
- MEV **blocking** or **prevention** as a Sentinel guarantee.
- **Production simulation** against external paid simulators as part of this trial (out of scope here).

## 11) Decision record template

Use this template before enabling any live trial:

| Field | Value |
| --- | --- |
| `provider_name` | e.g., `sourcify` |
| `provider_endpoint` | base URL or documented endpoint scope |
| `chain` | e.g., `base` |
| `free_or_paid` | `free` for this trial |
| `api_key_required` | `true` / `false` (trial prefers `false`) |
| `monthly_budget` | hard cap (USD); `0` if free-only |
| `max_trial_requests` | max calls for trial window |
| `enabled_flag` | exact env flag(s) and values |
| `timeout_ms` | matches configured timeout |
| `fallback_behavior` | e.g., unknown + confidence reduction |
| `approval_status` | pending / approved / rejected |
| `approved_by` | name |
| `approved_at` | ISO-8601 date |
| `rollback_owner` | name |
| `test_evidence` | links or commit refs to passing tests / notes |

Policy reminder for public copy: include **no full ABI coverage** claim (no universal ABI completeness).

Cross-references: `docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md`, `docs/16_launch/SENTINEL_PROVIDER_DECISION_GATE.md`, `docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md`, `docs/18_investor/CLAIMS_LEDGER.md`.

This plan does not activate live integration, does not assert full ABI completeness, and does not promise verified source for arbitrary contracts.
