# ABI/Source Provider Pivot Review v11.6

## 2) Purpose

Review the ABI/source provider path after **unresolved** Sourcify endpoint validation (see `docs/16_launch/SOURCIFY_ENDPOINT_VALIDATION_STATUS.md`). This document is **planning and posture only**: it does **not** perform provider calls, enable runtime providers, change `.env`, deploy, publish packages, or store raw provider bodies.

## 3) Current Sourcify evidence

- **v10.8A** local controlled attempt: **5** rows, all **`network_error`**, no usable metadata.
- **v11.2** VPS preflight: **`reachable: true`**, **HTTP 404** on the checked path, **connectivity evidence only** (no usable metadata).
- **v11.4** endpoint validation: **`tls_error`**, no usable metadata from the **full_match** metadata candidate for **T01**.
- **v11.5** status: endpoint validation **unresolved**; **full 5-target trial remains blocked**.

## 4) Current interpretation

- **Sourcify** remains a **candidate** path but is **unresolved** (no successful sanitized metadata shape observed in recorded evidence).
- **No usable metadata** has been received on any recorded Sourcify validation or trial attempt.
- **Full 5-target trial remains blocked** until endpoint validation succeeds and separate founder gates are met.
- **Provider remains disabled** in default configuration.
- **No** public claims of ABI/source coverage, verified-source completeness, or third-party verification guarantees are supported by current evidence.

## 5) Options

### Option A — Retry Sourcify endpoint validation later

- **One target** only.
- **One endpoint** only per attempt.
- Requires the exact founder phrase:

  **"green light retry VPS Sourcify endpoint validation only"**

- This is **not** a trial rerun.

### Option B — Prepare Blockscout endpoint validation path

- **Docs/test-only** preparation first (plan, gates, schema alignment).
- **Next preparation step:** `docs/16_launch/BLOCKSCOUT_BASE_ENDPOINT_SOURCE_PACK.md` (v11.8; candidate URL sourcing before validation).
- **One endpoint** candidate when validation is eventually approved.
- **One target** only for the first validation attempt.
- **No API keys** by default (unless a later explicitly approved path requires them).
- **No raw body** stored in evidence artifacts.
- **Not** a trial rerun until separately gated.
- Requires a future exact founder phrase:

  **"green light VPS Blockscout endpoint validation only"**

### Option C — Hold all live provider work

- Continue **local-only** fixtures and **fake backend** contract tests.
- **Safest** posture until evidence and approval posture improve.
- **No** live provider metadata attempt.

## 6) Recommendation

- **Do not run** the full Sourcify five-target trial now.
- **Do not run** five-target lookup now.
- **Prepare** the Blockscout endpoint validation plan as the **next docs/test** step, **unless** the founder explicitly chooses **Option A** (Sourcify retry phrase above). Prepared plan: `docs/16_launch/BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md` (v11.7; documentation only; **not** a validation run).
- **Keep the provider disabled** until a sanctioned validation or trial path clears recorded gates.

## 7) Decision criteria (unchanged discipline)

- Endpoint validation must produce a **usable sanitized metadata shape** before any **full** trial.
- **One target** only before any dataset-wide lookup.
- **Provider disabled** before and after any approved validation window.
- **`.env` unchanged** by documentation tasks; env hash discipline applies to live runs.
- **No raw response body** in committed evidence by default.
- **No paid calls** within the scoped free/public posture.
- **No claim inflation** relative to recorded evidence.

## 8) Public claim controls

**Allowed**

- Sourcify validation is **unresolved** in recorded evidence.
- Provider **pivot review** is **prepared** (this document).
- **Blockscout** may be **prepared** as a **candidate** path (planning only until separately approved).
- **Provider remains disabled** by default.

**Forbidden** (avoid implying)

- trial completed
- live ABI coverage
- full verified-source coverage
- guaranteed source verification
- detects honeypots
- guaranteed protection
- production provider active

## 9) Cross-references

- `docs/16_launch/SOURCIFY_ENDPOINT_VALIDATION_STATUS.md`
- `docs/16_launch/SOURCIFY_ENDPOINT_CORRECTION_PLAN.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md`
- `docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md`
- `docs/16_launch/BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md` (v11.7; prepared next path after unresolved Sourcify validation; **not run** from this pivot doc)
- `docs/16_launch/BLOCKSCOUT_BASE_ENDPOINT_SOURCE_PACK.md` (v11.8; Base endpoint source pack; selection pending)

This file does not run trials, activate providers, or perform network calls.
