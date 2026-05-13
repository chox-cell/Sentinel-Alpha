# VPS Sourcify Connectivity Preflight v1

## 2) Purpose

Define a safe preflight checklist for checking whether the VPS can reach Sourcify before any controlled trial rerun. This is not a trial run.

## 3) Current status

- Previous local Mac attempt recorded as v10.8A.
- All five rows returned network_error.
- No usable metadata was received.
- Provider remains disabled.
- Trial completion remains false.
- v11.2 manual VPS Sourcify connectivity preflight completed (one check only; not a trial rerun).

## 4) Preflight scope

- Connectivity check only.
- Max 1 Sourcify endpoint check before trial rerun.
- No dataset-wide trial.
- No provider runtime activation.
- No API keys.
- No paid calls.
- No DB writes.
- No raw provider response committed.

## 5) VPS preflight command plan

Document commands only; do not execute from this file:

- ssh to VPS
- confirm repo path
- `git status --short`
- `pytest -q tests/test_env_safety_policy.py`
- record `.env` hash if `.env` exists
- run a single short-timeout curl or head command to a Sourcify metadata endpoint or root endpoint
- record only:
  - reachable true/false
  - HTTP status
  - latency if available
  - no raw body

## 6) Allowed preflight result statuses

- not_run
- reachable
- timeout
- network_error
- dns_error
- tls_error
- http_error
- blocked

## 7) Evidence rules

- Store only sanitized preflight status.
- Do not store raw body.
- Do not store headers containing sensitive material.
- Do not record API keys.
- Do not change provider trial result rows.
- Do not update trial as completed.

## 8) Rerun gate

A controlled trial rerun may only happen if:

- VPS preflight result is reachable
- founder approves rerun explicitly
- `.env` hash before is recorded
- provider remains disabled before run
- max 5 target cap remains
- runbook is followed

Required rerun phrase:

"green light rerun Sourcify trial from VPS"

## 9) Public claim controls

Allowed:

- VPS preflight plan prepared
- previous local attempt failed due to network_error
- no usable metadata received
- provider disabled by default

Forbidden:

- finished successful provider trial claims
- live ABI availability claims
- full verified-source completeness claims
- assured third-party source verification claims
- honeypot or trap detection claims
- assured user protection claims
- production provider activation claims

## 10) Cross-references

- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md`
- `reports/provider_trials/abi_source_trial_results.v10.8.attempted.json`

This preflight plan does not run trials, activate providers, perform network calls from repository automation, or modify `.env`.

## 11) v11.2 recorded VPS result (sanitized evidence)

Recorded artifact: `reports/provider_trials/sourcify_vps_preflight.v11.2.json` (Markdown twin: `reports/provider_trials/sourcify_vps_preflight.v11.2.md`).

- `preflight_result: reachable_http_404`
- `reachable: true`
- `http_status: 404`
- `error_type: http_error`

Interpretation: the VPS reached Sourcify and received an HTTP response. A 404 on the health-style path still demonstrates HTTP reachability; it does **not** prove usable ABI/source metadata, source verification, or trial success. No raw response body was stored. No dataset-wide lookup was performed. Provider runtime remains disabled. A controlled trial rerun still requires the separate founder phrase **"green light rerun Sourcify trial from VPS"** plus runbook gates.

After `reachable_http_404`, follow `docs/16_launch/SOURCIFY_ENDPOINT_CORRECTION_PLAN.md` before attempting metadata endpoint validation or any trial rerun.
