# ABI/Source Provider Trial Approval Record v1

## 2) Current approval status

Documented posture (canonical for public-truth posture at file publication time):

```
approval_status: attempted_network_failed_provider_disabled
founder_phrase_observed: true
founder_phrase: "green light live provider trial"
trial_run: attempted
trial_completed_successfully: false
provider_active: false
live_calls_performed: true
usable_provider_metadata_received: false
api_keys_required: false
paid_calls_allowed: false
approved_by: "Chox"
approved_at: 2026-05-11
notes:
  - controlled read-only attempt made; all rows network_error
  - provider remains disabled; rerun requires confirmed network path
  - future rerun requires VPS preflight and exact phrase: "green light rerun Sourcify trial from VPS"
```

v11.2 VPS preflight only (separate founder approval; connectivity check only):

```
v11.2_preflight_phrase_observed: true
v11.2_preflight_phrase: "green light VPS Sourcify preflight only"
v11.2_preflight_run: true
v11.2_preflight_result: reachable_http_404
trial_rerun: false
provider_active: false
notes:
  - preflight completed; rerun not approved
  - trial rerun still requires exact phrase: "green light rerun Sourcify trial from VPS"
  - rerun blocked pending endpoint validation per SOURCIFY_ENDPOINT_CORRECTION_PLAN.md
```

v11.4 VPS Sourcify endpoint validation only (separate founder approval; one target, one GET):

```
v11.4_endpoint_validation_phrase_observed: true
v11.4_endpoint_validation_phrase: "green light VPS Sourcify endpoint validation only"
v11.4_endpoint_validation_run: true
trial_rerun: false
trial_rerun_still_blocked: true
provider_active: false
notes:
  - one-target endpoint validation recorded; not a full trial rerun
  - trial rerun still blocked until phrase: "green light rerun Sourcify trial from VPS"
```

v11.5 endpoint validation status consolidation (docs/test-only; no new network run):

```
v11.5_endpoint_validation_status_consolidation: true
endpoint_validation_status: unresolved
usable_metadata_received: false
full_trial_blocked: true
notes:
  - see docs/16_launch/SOURCIFY_ENDPOINT_VALIDATION_STATUS.md
  - metadata path has not returned usable metadata; full five-target trial remains blocked
```

v11.6 ABI/source provider pivot review (docs/test-only; no network; no provider activation):

```
v11.6_provider_pivot_review: true
provider_pivot_status: review_prepared / no new provider selected
notes:
  - see docs/16_launch/ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md
```

v11.7 Blockscout endpoint validation plan (docs/test-only; no network; plan not executed):

```
v11.7_blockscout_endpoint_validation_plan: true
blockscout_validation_plan_status: prepared / not run
provider_remains_disabled: true
notes:
  - see docs/16_launch/BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md
```

Historical note: v10.6 recorded the prior hold posture as `approval_status: not_approved`; v10.7 recorded `approval_status: approved_pending_real_target_validation` with `trial_run: false`, `live_calls_performed: false`, and `provider_active: false` before the v10.8A attempted Sourcify run.

## 3) Required founder phrase

Founder has now explicitly said the required phrase:

"green light live provider trial"

This phrase is an approval signal only. It does not run the trial, activate a provider, require API keys, or authorize lookup against placeholder targets.

## 4) Current default posture

- Provider disabled by default: `SENTINEL_ABI_SOURCE_PROVIDER_ENABLED=false` remains the documented default posture for repository guidance.
- No provider name is selected for outbound lookup in defaults.
- No production runtime provider activation is authorized by this record.
- The v10.8A attempted Sourcify run recorded read-only call attempts only; no usable provider metadata was received.
- No DB writes and no mandatory persistence stem from this document.
- ABI/source scanner wiring stays disabled or not_configured until a separately documented posture change tied to authorization.
- Live provider execution remains blocked until sourced public Base targets are reviewed and the runbook execution step is deliberately performed.

## 5) Already prepared assets

- ABI/source activation plan (gate documentation)
- fake backend ABI/source contract tests
- disabled ABI/source wiring skeleton
- `.env.example` placeholders (names only)
- controlled trial plan
- trial dataset (real public Base target candidates prepared)
- attempted Sourcify trial evidence (`reports/provider_trials/abi_source_trial_results.v10.8.attempted.json`)
- VPS Sourcify connectivity preflight plan (`ABI_SOURCE_PROVIDER_VPS_CONNECTIVITY_PREFLIGHT.md`)
- v11.2 VPS Sourcify connectivity preflight evidence (`reports/provider_trials/sourcify_vps_preflight.v11.2.json`)
- trial result schema
- Sourcify/Blockscout dry-run skeleton
- operational runbook
- static evidence-shape sample bundle (`reports/provider_trials/abi_source_trial_results.sample.json`)

## 6) What remains blocked (until future runbook execution)

Although the founder phrase has been received, the following remain **out of scope** for unattended automation:

- toggling outbound provider connectivity from repository defaults documented here
- selecting a billing-bearing live explorer endpoint beyond planning notes
- loading real explorer credentials into tracked files
- performing HTTP(S) lookups for ABI/source retrieval as part of a “trial completion” posture
- writing non-placeholder evidence rows claimed as definitive trial outcomes
- expanding public-product claims solely from one-off exploratory calls
- running lookup against placeholder targets or any unreviewed address list

## 7) Future authorization checklist pointers

Coordinate with `ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md` before any live execution:

- VPS Sourcify connectivity preflight completed with `reachable` status before any rerun
- founder rerun phrase recorded: "green light rerun Sourcify trial from VPS"
- provider selected (preferred: Sourcify or Blockscout)
- targets ≤ 5 and requests capped (≤ policy)
- env hash-before captured
- rollback owner assigned
- free-tier posture confirmed (`paid_calls_allowed` remains false unless separate budget artifact exists)
- conservative fallback semantics accepted again after any window
- public-language review complete

## 8) Reasons for hold posture

- keep integration disabled until deliberate authorization avoids surprise spend or traffic
- avoid premature marketing language tied to unexecuted scaffolding
- protect contributor `.env` discipline and hashing expectations
- maintain fallback-first risk messaging for downstream consumers

## 9) Public claim controls

Allowed public statements reflecting this file today:

- A provider trial **authorization record artifact** exists internally.
- The founder approval phrase has been recorded.
- A controlled read-only Sourcify attempt was recorded as `approval_status: attempted_network_failed_provider_disabled`.
- No usable provider metadata was received and the production runtime provider remains disabled.
- Providers remain disabled by documented defaults.

Forbidden public shorthand (marketing or social copy) implying any of:

- Finished execution clearance before sourced target review and runbook execution are recorded.
- Narratives that mirror a finalized lab run when scaffolding only exists.
- Universal ABI completeness for explorers or chains.
- Universal verified-source completeness.
- Assured honeypot-style trap guarantees from ABI lookups alone.
- Outcome narratives promising assured user protection from ABI lookups alone.

## 10) Cross references

- `docs/16_launch/ABI_SOURCE_PROVIDER_VPS_CONNECTIVITY_PREFLIGHT.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md`
- `reports/provider_trials/abi_source_trial_results.sample.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md`

This authorization record alone does **not** perform lookups, mutate runtime flags, modify `.env`, or execute shell commands.
