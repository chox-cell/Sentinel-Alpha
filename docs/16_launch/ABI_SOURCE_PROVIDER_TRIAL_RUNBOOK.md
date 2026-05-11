# ABI/Source Provider Trial Runbook v1

## 2) Purpose

Operational checklist for a future controlled live ABI/source provider trial. This file is documentation and gating only. The trial is not active now. It does not execute commands, enable providers, perform network calls, require API keys, change runtime defaults, or mutate `.env`.

## 3) Current status

- Trial runbook prepared (documentation only).
- Trial not run.
- Provider not active for live lookup in default configuration.
- No live calls have been performed under this runbook.
- No API keys are required now to read this runbook.
- Dry-run skeleton exists (`abi_source_dry_run_provider.py`).
- Result schema exists (`ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md`).
- Dataset exists (`ABI_SOURCE_PROVIDER_TRIAL_DATASET.md`).
- Founder phrase received: "green light live provider trial".
- Live execution still requires sourced target review, env hash capture, and this runbook's execution step.

## 4) Founder approval gate

Authorization posture is anchored in `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md` (currently **`approved_pending_real_target_validation`**). Founder has articulated the verbatim phrase mandated in that file: **"green light live provider trial"**. This runbook supplements that artifact; neither file executes network calls itself.

A live trial cannot run until all of the following are explicitly true and recorded:

- founder phrase recorded: explicit yes (written decision), including reproduction of the required phrase gate from the approval record.
- sourced target review complete: public Base contract candidates accepted, with no placeholder target in the execution list.
- provider selected: Sourcify or Blockscout preferred for first trial.
- max target count confirmed: <= 5 (aligned with dataset/trial plan).
- max request count confirmed (hard cap for the run window).
- timeout confirmed (matches `SENTINEL_ABI_SOURCE_PROVIDER_TIMEOUT_MS` policy).
- rollback owner assigned (name and contact on the decision record).
- .env hash recorded before run (see pre-run commands; store as `env_hash_before` on the decision record).
- provider config flags reviewed (`SENTINEL_ABI_SOURCE_PROVIDER_ENABLED`, `SENTINEL_ABI_SOURCE_PROVIDER_NAME`, `SENTINEL_ABI_SOURCE_DRY_RUN_ONLY`, `BLOCKSCOUT_BASE_URL` if relevant).
- no paid call requirement confirmed for the scoped trial.
- public claims reviewed (no overclaim pressure before/during/after).
- fallback behavior accepted (Sentinel must remain usable when provider fails).

## 5) Pre-run commands (document only — do not execute from this file)

Record these as the expected local gate checks before any approved live attempt. The agent or human operator runs them in their own environment; this markdown file does not run them.

- `git status --short`
- `pytest -q`
- `pytest -q tests/test_abi_source_dry_run_provider.py`
- `pytest -q tests/test_abi_source_provider_trial_result_schema.py`
- `sha256sum .env` on GNU/Linux, or `shasum -a 256 .env` on macOS — capture digest as env hash before run.
- confirm provider flag disabled before trial: `SENTINEL_ABI_SOURCE_PROVIDER_ENABLED=false` for the repository default path until the approved local window only.

## 6) Trial execution outline (documentation only)

- Choose provider (Sourcify or Blockscout preferred) per approval record and target review.
- Choose 1 to 5 targets from the sourced dataset (or a reviewed replacement list).
- Enable provider only for a controlled local run after approval (never from this doc).
- Run read-only lookups only; respect max requests and timeout.
- Record sanitized result rows only per the result schema.
- Disable provider immediately after the run window closes.
- Verify fallback still works (adapter returns safe unknown path when provider off).

## 7) Post-run evidence checklist

- Future real result files should follow the **shape** of the static sample bundle `reports/provider_trials/abi_source_trial_results.sample.json` (field names, sanitization posture) while replacing placeholder values with sanctioned, sanitized trial facts only after a run. The sample file itself remains `not_run` and is **not evidence** of execution.
- .env hash after run: record `env_hash_after` using the same hash command as pre-run; compare to `env_hash_before` for unexpected drift.
- git status clean or only expected documentation/evidence files changed.
- result rows sanitized; no raw provider bodies unless a separate explicit exception is approved.
- raw_response_stored false unless explicitly approved otherwise.
- secret_material_observed false.
- no top-level schema break for API consumers.
- provider disabled after run (return flags to safe defaults).
- claims ledger not updated beyond reviewed evidence (no capability inflation).

## 8) Abort conditions

Stop immediately and roll back if any occur:

- unexpected paid call or billable API usage outside the approved free scope.
- secret exposure in logs, artifacts, or metadata.
- .env mutation not expected or not approved.
- provider timeout storm (runaway retries or hung workers).
- rate limit escalation without backoff approval.
- invalid response patterns that confuse parsing or corrupt metadata.
- provider becomes a blocking hard dependency for core Sentinel responses.
- unsafe claim pressure (“ship it live” narratives without evidence review).

## 9) Rollback

- Set `SENTINEL_ABI_SOURCE_PROVIDER_ENABLED=false`.
- Set `SENTINEL_ABI_SOURCE_DRY_RUN_ONLY=false` if it was toggled during experiments.
- Remove or clear `SENTINEL_ABI_SOURCE_PROVIDER_NAME` if needed to return to not_configured posture.
- Rerun env safety tests: `pytest -q tests/test_env_safety_policy.py`.
- Rerun adapter/fallback tests: `pytest -q tests/test_abi_source_provider_wiring_skeleton.py` and `pytest -q tests/test_abi_source_adapter.py`.
- Document rollback outcome in the decision record `evidence_summary` / notes.

## 10) Decision record template

| Field | Value |
| --- | --- |
| `approval_status` | pending / approved / rejected |
| `approved_by` | founder name |
| `approved_at` | ISO-8601 |
| `provider_name` | e.g., sourcify / blockscout |
| `provider_endpoint` | documented base URL scope only |
| `provider_mode` | e.g., controlled local trial |
| `max_targets` | integer ≤ 5 |
| `max_requests` | integer cap |
| `timeout_ms` | integer |
| `retry_limit` | integer (prefer 0–1) |
| `paid_calls_allowed` | false (required default for gated trial posture) |
| `env_hash_before` | SHA-256 of repo `.env` before run |
| `env_hash_after` | SHA-256 of repo `.env` after run |
| `rollback_owner` | name |
| `run_started_at` | ISO-8601 or empty if not_run |
| `run_finished_at` | ISO-8601 or empty if not_run |
| `result_file` | path or artifact id for sanitized rows only |
| `evidence_summary` | short factual summary |
| `follow_up_required` | yes/no |

## 11) Public claim controls

Allowed public statements **after** a run **only when factually true**:

- A controlled trial was run under documented limits (no default-on production claim).
- N targets attempted (exact count).
- M sanitized lookup results recorded (exact count).
- Provider disabled again after trial (flags returned).

Forbidden public implications (avoid these exact marketing phrases):

- Universal ABI completeness for Base or any chain.
- Universal verified-source completeness.
- Guaranteed third-party verification outcomes.
- Honeypot or trap detection guarantees tied to ABI/source lookup.
- Outcome narratives that imply assured user safety beyond evidence.
- Implication that paid production provider endpoints are enabled by default after the trial.

## 12) Cross-references

- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_DATASET.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md`
- `docs/16_launch/SENTINEL_PROVIDER_DECISION_GATE.md`
- `docs/18_investor/CLAIMS_LEDGER.md`

This runbook does not run trials, activate providers by default, or replace explicit founder approval and engineering review.
