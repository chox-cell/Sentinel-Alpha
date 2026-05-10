# ABI/Source Provider Trial Approval Record v1

## 2) Current approval status

Documented posture (canonical for public-truth posture at file publication time):

```
approval_status: not_approved
trial_run: false
provider_active: false
live_calls_performed: false
api_keys_required: false
paid_calls_allowed: false
approved_by: null
approved_at: null
```

## 3) Required future approval phrase

A live ABI/source provider trial may only begin after founder explicitly says exactly:

"green light live provider trial"

## 4) Current default posture

- Provider disabled by default: `SENTINEL_ABI_SOURCE_PROVIDER_ENABLED=false` remains the documented default posture for repository guidance.
- No provider name is selected for outbound lookup in defaults.
- No live provider calls and no unsolicited network lookups are authorized by this record.
- No DB writes and no mandatory persistence stem from this document.
- ABI/source scanner wiring stays disabled or not_configured until a separately documented posture change tied to authorization.

## 5) Already prepared assets

- ABI/source activation plan (gate documentation)
- fake backend ABI/source contract tests
- disabled ABI/source wiring skeleton
- `.env.example` placeholders (names only)
- controlled trial plan
- trial dataset (placeholder targets)
- trial result schema
- Sourcify/Blockscout dry-run skeleton
- operational runbook
- static evidence-shape sample bundle (`reports/provider_trials/abi_source_trial_results.sample.json`)

## 6) What remains blocked (until future authorization workflow)

Until the founder authorization workflow and gates are satisfied, the following remain **out of scope** for unattended automation:

- toggling outbound provider connectivity from repository defaults documented here
- selecting a billing-bearing live explorer endpoint beyond planning notes
- loading real explorer credentials into tracked files
- performing HTTP(S) lookups for ABI/source retrieval as part of a “trial completion” posture
- writing non-placeholder evidence rows claimed as definitive trial outcomes
- expanding public-product claims solely from one-off exploratory calls

## 7) Future authorization checklist pointers

Coordinate with `ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md` when/if authorization happens later:

- founder authorization phrase reproduced in written approval
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
- The controlled live ABI/source trial is **not cleared** (`approval_status`: not_approved).
- Providers remain disabled by documented defaults.

Forbidden public shorthand (marketing or social copy) implying any of:

- Finished executive clearance when `approval_status` is still `not_approved`.
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
