# ABI/Source Provider Trial Result Schema v1

## 2) Purpose

Define how future ABI/source provider trial results will be recorded after an approved trial runs. Schema only. Trial not run. This file does not call providers, enable live integration, change runtime defaults, or require API keys.

## 3) Current status

- Result schema prepared (documentation).
- No provider trial executed.
- No live provider enabled by default.
- No network call performed by this document.
- No API key required to author or use this schema as a template.
- No DB write performed by publishing this schema.

## 4) Result object fields

Each trial outcome row records the following fields:

| Field | Description |
| --- | --- |
| `result_version` | Schema semver string for this artifact (e.g. `v1`). |
| `trial_id` | Dataset id (e.g. `T01`…`T05`) tying to `ABI_SOURCE_PROVIDER_TRIAL_DATASET.md`. |
| `chain` | Chain label (e.g. `base`). |
| `contract_address_hash` | Hash of canonical contract address; raw address not stored in evidence by default. |
| `category` | Dataset category (ERC20-like, NFT-like, proxy-like, router/pool-like, generic/utility). |
| `provider_name` | Provider identifier used for the lookup attempt (or `null` if not_run). |
| `provider_endpoint_hash` | Hash of endpoint base URL if an endpoint identifier is retained; else `null`. |
| `lookup_status` | Outcome enum; see allowed values below. |
| `verified_source_status` | Third-party verification signal (e.g. `unknown`, `verified`, `not_verified`) aligned with adapter vocabulary. |
| `abi_available` | Whether ABI text was obtained (`unknown`, `true`, `false`). |
| `abi_function_count` | Count of ABI functions if parsed; `null` if unknown/not applicable. |
| `abi_function_names_sample` | Small capped list of function names if sanitized; empty array if none. |
| `source_fetch_error_type` | Adapter-classified error string if failure; `null` on success or not_run. |
| `latency_ms` | Observed latency for the attempt; `null` if not_run. |
| `timeout_ms` | Configured cap used for the attempt. |
| `fallback_mode` | Boolean: whether conservative fallback path applied. |
| `confidence_impact` | Conservative note or scalar consistent with scanner adapter policy. |
| `response_sanitized` | Boolean: only sanitized excerpts were recorded. |
| `raw_response_stored` | Boolean: whether a raw provider body was stored (default false). |
| `secret_material_observed` | Boolean: whether any secret pattern appeared in handled data (must default false in clean runs). |
| `created_at` | ISO-8601 timestamp when the row was finalized. |
| `notes` | Human note; no secrets. |

## 5) Allowed `lookup_status` values

Use exactly one of:

- `not_run`
- `dry_run_not_executed` (dry-run skeleton / planning-only; **not trial evidence** on its own)
- `success`
- `timeout`
- `rate_limited`
- `invalid_response`
- `provider_down`
- `unsupported_chain`
- `unsupported_provider`
- `error`

## 6) Privacy rules

- No raw API keys in evidence rows.
- No raw auth headers.
- No raw provider response body by default; use `response_sanitized: true` and short excerpts only when needed.
- No private keys or seed phrases.
- Hash contract addresses for stored artifacts; align with existing scanner hashing policy.
- Hash provider endpoint identifiers if persisted beyond this doc (`provider_endpoint_hash`).
- Store sanitized summaries only; default `raw_response_stored: false`.

## 7) Evidence recording rules

- Before any approved trial: all dataset targets remain represented with `lookup_status: not_run` until evidence exists.
- `lookup_status: dry_run_not_executed` documents a local dry-run plan only; it is **not trial evidence** and does not mean a live lookup ran.
- Before recording real execution rows after a sanctioned trial, satisfy `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md` (founder approval and operational checklist).
- After a future approved trial: record only sanitized status and metadata per this schema.
- Never promote public product claims from a single successful row.
- Failures must preserve conservative fallback behavior in runtime (per adapter design).
- Confidence impact must remain conservative for all outcomes.

## 8) Sample result rows (pre-trial placeholders)

Five placeholder rows aligned to dataset ids `T01`–`T05`. Values show the mandatory pre-trial posture only.

```json
[
  {"trial_id": "T01", "lookup_status": "not_run", "verified_source_status": "unknown", "abi_available": "unknown", "fallback_mode": true, "raw_response_stored": false, "secret_material_observed": false},
  {"trial_id": "T02", "lookup_status": "not_run", "verified_source_status": "unknown", "abi_available": "unknown", "fallback_mode": true, "raw_response_stored": false, "secret_material_observed": false},
  {"trial_id": "T03", "lookup_status": "not_run", "verified_source_status": "unknown", "abi_available": "unknown", "fallback_mode": true, "raw_response_stored": false, "secret_material_observed": false},
  {"trial_id": "T04", "lookup_status": "not_run", "verified_source_status": "unknown", "abi_available": "unknown", "fallback_mode": true, "raw_response_stored": false, "secret_material_observed": false},
  {"trial_id": "T05", "lookup_status": "not_run", "verified_source_status": "unknown", "abi_available": "unknown", "fallback_mode": true, "raw_response_stored": false, "secret_material_observed": false}
]

```

## 9) Success/failure interpretation

- A single successful lookup shows the provider path can work for that target only; it does not prove comprehensive ABI availability across Base or all contracts.
- It does not prove assurance of third-party source verification for arbitrary addresses.
- It does not prove safety or security outcomes.
- Provider failure must not break the Sentinel API response shape; fallback remains required.

Public copy policy reminder: include no full ABI coverage claim; does not promise verified source for arbitrary contracts.

## 10) Public claim controls

**Allowed**

- Trial result schema prepared.
- Future trial results will be sanitized per privacy rules.
- No trial run has been executed for this evidence path yet.

**Forbidden** wording for materials tied to this schema

- Implication that a trial already finished successfully (avoid “trial finished” style copy for this gate).
- Universal ABI availability claims for live explorers.
- Universal verified-source completeness claims.
- Third-party verification promises outside scoped evidence.
- Trap-detection or malicious-token guarantees.
- Outcome or user-protection guarantees tied to ABI/source lookup alone.
- MEV suppression claims from this schema scope.
- Claims that external production simulation workloads were executed via this schema step.

## 11) Cross-references

- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_DATASET.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md`
- `docs/18_investor/CLAIMS_LEDGER.md`
