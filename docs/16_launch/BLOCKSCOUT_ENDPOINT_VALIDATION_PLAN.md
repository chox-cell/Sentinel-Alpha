# Blockscout Endpoint Validation Plan v11.7

## 2) Purpose

Prepare **Blockscout** as an alternative ABI/source **endpoint validation** path after **unresolved** Sourcify validation (see `docs/16_launch/SOURCIFY_ENDPOINT_VALIDATION_STATUS.md` and `docs/16_launch/ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md`). This document is **planning only**: it does **not** call Blockscout, run a trial, enable runtime providers, change `.env`, deploy, publish packages, or commit raw provider bodies.

## 3) Current context

- **Sourcify** remains **unresolved** after **v10.8A**, **v11.2**, **v11.4**, and **v11.5** recorded evidence (no usable Sourcify metadata in consolidated posture).
- The **v11.6** pivot review recommends preparing the **Blockscout** path as the next **docs/test** step unless the founder chooses a Sourcify retry instead.
- **Provider remains disabled** by default.
- **Full trial remains blocked** until endpoint validation succeeds and separate founder gates are met.
- **No usable metadata** has been received from **Sourcify** in recorded evidence.

## 4) Blockscout validation scope

- **One target** only for the first validation attempt.
- **One endpoint** only per validation attempt.
- **No dataset-wide lookup**.
- **Not** a trial rerun by itself.
- **Timeout ≤ 5 seconds** for the single request when a validation run is eventually approved.
- **No API key** by default for the planned public read-only posture (unless a later explicitly approved path documents otherwise).
- **No paid calls** in the scoped free posture.
- **No raw response body** committed to the repository from the validation run.
- **Provider disabled** before and after any approved validation window.

## 5) Endpoint candidate

Document as **candidate template only** — **no calls** from this file:

`{blockscout_base_url}/api/v2/smart-contracts/{address}`

For **Base**, a candidate **`blockscout_base_url`** must be **reviewed and approved** before any live validation:

- `BLOCKSCOUT_BASE_URL` placeholder exists in **`.env.example`** (configuration documentation only).
- **No live value** is required to author or store **this** plan.
- **No real endpoint** is selected or endorsed **in this task** unless already documented elsewhere under the same safety rules.

## 5a) Endpoint source pack and selection gate

- **Candidate base URLs** for Base must be collected and reviewed using `docs/16_launch/BLOCKSCOUT_BASE_ENDPOINT_SOURCE_PACK.md` (v11.8 source pack; docs/test only).
- **Blockscout endpoint validation is blocked** until **exactly one** candidate is **selected** for validation (steward replaces placeholder `REQUIRED_SOURCE_URL` values with reviewed `source_url` entries and marks **only one** row `selected_for_validation: true` in a future approved revision of that pack or a successor artifact — **not** done in the v11.8 pack revision).

## 6) Future required phrase

A future **one-target, one-endpoint** Blockscout **endpoint validation** run on an approved VPS requires the founder to say **exactly**:

**"green light VPS Blockscout endpoint validation only"**

## 7) Sanitized fields to record in future

When a validation run is executed and evidence is recorded, retain only a **sanitized** summary shape including at minimum:

- `endpoint_label`
- `endpoint_hash`
- `target` `trial_id`
- `contract_address_hash`
- `reachable`
- `http_status`
- `error_type`
- `latency_ms`
- `metadata_shape_observed`
- `abi_available`
- `abi_function_count`
- `abi_function_names_sample`
- `raw_response_stored: false` (default posture)
- `secret_material_observed: false`
- `usable_metadata_received`
- `notSecurityGuarantee: true`

## 8) Success criteria

- **One request** completes without TLS/DNS/network-class failure (per recorded error taxonomy).
- Response can be **parsed** into a **sanitized metadata** summary (shape observed; no raw body).
- **No raw body** stored in committed artifacts.
- **No secrets** observed in handled material.
- **Provider remains disabled** outside any explicitly approved narrow window (default remains off).
- Evidence does **not** claim **full** ABI/source **coverage** for the dataset.

## 9) Failure criteria

Treat as failure (stop; record; do not expand scope):

- **Timeout**
- **DNS / TLS / network** error
- **Invalid response** / non-parseable payload for the intended summary shape
- **No ABI/source shape** observed in sanitized parsing
- **Raw body** accidentally stored
- **Provider runtime** enabled without explicit rollback-approved posture
- **`.env` mutation** outside documented env-hash discipline

## 10) Rerun / trial gate

A **full five-target** provider trial remains **blocked** until:

- **One-target** Blockscout **endpoint validation** **succeeds** (per success criteria above), **and**
- the founder explicitly says **exactly**:

  **"green light rerun Blockscout trial from VPS"**

- runbook gates pass,
- **provider remains disabled** before the approved run window,
- **max 5 targets** remains enforced for any full trial.

## 11) Public claim controls

**Allowed**

- Blockscout **validation plan** is **prepared** (this document).
- Blockscout is a **candidate** path only until validation evidence exists.
- **Provider remains disabled** by default.

**Forbidden** (avoid implying)

- Blockscout integration live
- trial completed
- live ABI coverage
- full verified-source coverage
- guaranteed source verification
- detects honeypots
- guaranteed protection
- production provider active

## 12) Cross-references

- `docs/16_launch/BLOCKSCOUT_BASE_ENDPOINT_SOURCE_PACK.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md`
- `docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md`

This plan does not perform network calls, enable providers, or select a live Blockscout base URL.
