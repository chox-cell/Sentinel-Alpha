# ABI/Source Provider Trial Approval Record v1

## 2) Current approval status

Documented posture (canonical for public-truth posture at file publication time):

```
approval_status: approved_pending_real_target_validation
founder_phrase_observed: true
founder_phrase: "green light live provider trial"
trial_run: false
provider_active: false
live_calls_performed: false
api_keys_required: false
paid_calls_allowed: false
approved_by: "Chox"
approved_at: 2026-05-11
notes:
  - approval phrase received
  - live provider trial is still blocked until real public Base targets replace placeholders
  - provider remains disabled until runbook execution step
```

Historical note: v10.6 recorded the prior hold posture as `approval_status: not_approved`; v10.7 records the founder phrase while keeping live execution blocked pending target review and runbook execution.

## 3) Required founder phrase

Founder has now explicitly said the required phrase:

"green light live provider trial"

This phrase is an approval signal only. It does not run the trial, activate a provider, require API keys, or authorize lookup against placeholder targets.

## 4) Current default posture

- Provider disabled by default: `SENTINEL_ABI_SOURCE_PROVIDER_ENABLED=false` remains the documented default posture for repository guidance.
- No provider name is selected for outbound lookup in defaults.
- No live provider calls and no unsolicited network lookups are authorized by this record.
- No DB writes and no mandatory persistence stem from this document.
- ABI/source scanner wiring stays disabled or not_configured until a separately documented posture change tied to authorization.
- Live provider execution remains blocked until sourced public Base targets are reviewed and the runbook execution step is deliberately performed.

## 5) Already prepared assets

- ABI/source activation plan (gate documentation)
- fake backend ABI/source contract tests
- disabled ABI/source wiring skeleton
- `.env.example` placeholders (names only)
- controlled trial plan
- trial dataset (real public Base target candidates prepared; trial not run)
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

- founder authorization phrase reproduced in written approval (received: "green light live provider trial")
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
- The founder approval phrase has been recorded (`approval_status`: approved_pending_real_target_validation).
- The controlled live ABI/source trial has not run and provider execution remains blocked until runbook execution.
- Providers remain disabled by documented defaults.

Forbidden public shorthand (marketing or social copy) implying any of:

- Finished execution clearance before sourced target review and runbook execution are recorded.
- Narratives that mirror a finalized lab run when scaffolding only exists.
- Universal ABI completeness for explorers or chains.
- Universal verified-source completeness.
- Assured honeypot-style trap guarantees from ABI lookups alone.
- Outcome narratives promising assured user protection from ABI lookups alone.

## 10) Cross references

- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md`
- `reports/provider_trials/abi_source_trial_results.sample.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md`

This authorization record alone does **not** perform lookups, mutate runtime flags, modify `.env`, or execute shell commands.
