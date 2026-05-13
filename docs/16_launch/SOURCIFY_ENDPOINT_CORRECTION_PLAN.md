# Sourcify Endpoint Correction Plan v1

## 2) Purpose

Plan how to correct the Sourcify endpoint strategy before any controlled trial rerun. This is not a network run.

## 3) Current evidence

Consolidated posture (no new network run): `docs/16_launch/SOURCIFY_ENDPOINT_VALIDATION_STATUS.md` (v11.5). **Next decision point** for continuing Sourcify vs preparing Blockscout vs holding live work: `docs/16_launch/ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md` (v11.6; docs/test only).

- v10.8A local attempt: 5 requests attempted, all network_error, no usable metadata.
- v11.2 VPS preflight: one request, reachable true, HTTP 404, no usable metadata.
- v11.4 one-target endpoint validation: one request for T01 via full_match template; see `reports/provider_trials/sourcify_endpoint_validation.v11.4.json` (endpoint validation only; not a trial rerun). Recorded outcome included `tls_error` with `reachable: false`; **endpoint validation therefore remains unresolved** until canonical retry or different evidence succeeds.
- Provider remains disabled.
- Trial rerun has not happened.

## 4) Interpretation

- HTTP 404 means the VPS reached Sourcify but the checked endpoint is not a usable metadata endpoint.
- This does not prove ABI availability.
- This does not prove source verification.
- This does not authorize dataset-wide trial rerun.

## 5) Endpoint candidates to validate in future

Document as candidates only; no calls from this file:

- Sourcify repository metadata endpoint (full match):

  `https://repo.sourcify.dev/contracts/full_match/8453/{address}/metadata.json`

- Sourcify repository metadata endpoint (partial match):

  `https://repo.sourcify.dev/contracts/partial_match/8453/{address}/metadata.json`

- Sourcify server API alternatives if later confirmed by upstream documentation (names and paths TBD; do not guess live URLs without docs review).

## 6) Future endpoint validation rules

- one target only first
- one endpoint only per validation attempt
- timeout <= 5 seconds
- no API key
- no raw response body committed
- store only:
  - endpoint_label
  - endpoint_hash
  - http_status
  - reachable
  - metadata_shape_observed true/false
  - raw_response_stored false
  - secret_material_observed false
- do not update trial results from endpoint validation alone

## 7) Rerun gate

A full controlled trial rerun remains blocked until:

- endpoint validation succeeds on one target
- founder explicitly says:

  "green light rerun Sourcify trial from VPS"

- runbook gates pass
- provider remains disabled before run
- max 5 targets remains enforced

## 8) Failure handling

- 404 on metadata endpoint -> record endpoint_not_found or no_match
- timeout -> timeout
- DNS/TLS/network -> corresponding error
- invalid JSON -> invalid_response
- no ABI in metadata -> abi_available unknown/false
- fallback mode remains true unless valid metadata is sanitized

## 9) Public claim controls

Allowed:

- VPS can reach Sourcify
- endpoint correction plan prepared
- no usable metadata received yet
- provider disabled by default

Forbidden public shorthand (avoid implying):

- finished successful provider trial claims
- live ABI availability claims
- full verified-source completeness claims
- assured third-party source verification claims
- honeypot or trap detection claims
- assured user protection claims
- production provider activation claims

## 10) Operator execution notes

Regenerate `reports/provider_trials/sourcify_endpoint_validation.v11.4.json` from the approved VPS host when TLS or network errors reflect a non-VPS automation environment.

## 11) v11.4 recorded one-target validation (sanitized evidence)

Artifact: `reports/provider_trials/sourcify_endpoint_validation.v11.4.json` (Markdown twin: `reports/provider_trials/sourcify_endpoint_validation.v11.4.md`).

This records **one** metadata endpoint check for **T01** only. It is endpoint validation only: it is **not** a five-target provider trial rerun, **not** dataset-wide lookup evidence, and **not** proof of ABI coverage. A full controlled trial rerun remains blocked until the separate founder phrase **"green light rerun Sourcify trial from VPS"** plus runbook gates.

If the recorded attempt shows TLS or network errors, treat it as environment-specific until a canonical VPS re-run produces reachability evidence.

## 12) Cross-references

- `docs/16_launch/SOURCIFY_ENDPOINT_VALIDATION_STATUS.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_VPS_CONNECTIVITY_PREFLIGHT.md`
- `reports/provider_trials/sourcify_vps_preflight.v11.2.json`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md`
- `reports/provider_trials/sourcify_endpoint_validation.v11.4.json`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_DATASET.md`

This endpoint correction plan does not perform network calls, mutate runtime flags, modify `.env`, or execute a provider trial.
