# Sourcify Endpoint Validation Status v11.5

## 2) Purpose

Summarize current Sourcify connectivity and endpoint validation evidence recorded in-repo. This note is **documentation and consolidation only**: it does **not** perform a new network run, enable any provider, change `.env`, or store raw provider bodies.

## 3) Evidence so far

### v10.8A local controlled attempt

- Five requests attempted.
- Five rows returned `network_error`.
- No usable metadata was received.
- Provider remained disabled.

### v11.2 VPS connectivity preflight

- One request only.
- `reachable: true`.
- HTTP **404** on the checked path.
- No usable metadata was received.
- Recorded as **connectivity evidence only** (not ABI/source metadata proof).

### v11.4 endpoint validation

- One request only.
- **T01** only.
- **full_match** endpoint candidate (see `reports/provider_trials/sourcify_endpoint_validation.v11.4.json`).
- `reachable: false`.
- `error_type: tls_error`.
- `usable_metadata_received: false`.
- `verified_source_status: unknown`.
- `abi_available: unknown`.

## 4) Current interpretation

- Sourcify domain reachability was observed from the VPS in v11.2 (HTTP response received).
- The **metadata endpoint path** has **not** yet returned usable metadata in recorded evidence.
- v11.4 did **not** validate endpoint usability (TLS failure; no successful HTTP/metadata parse).
- No recorded result proves ABI availability.
- No recorded result proves source verification.
- The **full five-target provider trial remains blocked**.
- **Full 5-target trial remains blocked** (same gate; explicit wording for runbook alignment).

## 5) Current block conditions

- `usable_metadata_received` remains **false** across recorded validation attempts.
- `verified_source_status` remains **unknown** where no successful metadata shape was observed.
- `abi_available` remains **unknown** where no successful metadata shape was observed.
- Provider remains **disabled**.
- **No production provider active** for this evidence path.
- **No dataset-wide lookup** approved or performed as part of these steps.

## 6) Allowed next steps

- **Optional** canonical VPS endpoint validation **retry** only if the founder explicitly approves the exact phrase:

  **"green light retry VPS Sourcify endpoint validation only"**

- **Full trial rerun** only if endpoint validation **succeeds** (usable metadata observed per runbook/schema discipline) **and** the founder explicitly says:

  **"green light rerun Sourcify trial from VPS"**

## 7) Public claim controls

**Allowed**

- Sourcify connectivity and endpoint validation attempts are **recorded**.
- **No usable metadata received yet** in consolidated evidence.
- Provider **remains disabled**.
- **Full trial remains blocked** until the gates above are met.

**Forbidden** (avoid implying)

- trial completed
- live ABI coverage
- full verified-source coverage
- guaranteed source verification
- detects honeypots
- guaranteed protection
- production provider active

## 8) Cross-references

- `docs/16_launch/ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md` (v11.6 provider path review; docs/test only)
- `docs/16_launch/SOURCIFY_ENDPOINT_CORRECTION_PLAN.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_VPS_CONNECTIVITY_PREFLIGHT.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md`
- `reports/provider_trials/sourcify_endpoint_validation.v11.4.json`
- `reports/provider_trials/sourcify_vps_preflight.v11.2.json`

This file does not deploy, publish packages, run trials, perform dataset-wide lookups, or mutate runtime configuration.
