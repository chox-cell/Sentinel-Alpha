# Known Base Contracts Trial Dataset v1

## 2) Purpose

Defines candidate contract categories and placeholder records for a future controlled ABI/source provider trial. This file is documentation and planning only. The dataset is not active now. It does not call providers, verify addresses against live endpoints in automation, require API keys, or change runtime behavior.

## 3) Current status

- Dataset is planning-only.
- No provider calls have been made by authoring this document.
- No address is claimed verified by a live provider lookup in this document; placeholders are non-production stand-ins unless replaced by an approved, fixture-backed list.
- Provider remains disabled by default in shipping configuration.
- Max 5 trial targets for the controlled trial scope (see trial plan).

## 4) Dataset selection rules

- Base chain only (chain id `8453` context; all targets listed as Base in the table below).
- Read-only lookup only for any future trial (no writes, no submissions).
- Prefer public, high-signal contract categories over arbitrary or obscure addresses.
- Include mixed categories for boundary exercise:
  - ERC20-like (token contract shape)
  - NFT-like (ERC721-style or ERC1155-style asset contract)
  - proxy-like (upgradeable / implementation pointer patterns)
  - router-like or pool-like (DEX/router/pool style; routing surface)
  - generic/utility contract (simple or common utility pattern)
- Avoid risky or unverified random addresses; do not pull unreviewed one-off contracts into the default dataset.
- Do not include private user wallets as trial targets.
- Do not include secrets, API keys, or private metadata in this dataset.

## 5) Trial target table

Exactly five placeholder targets. Replace with approved public fixtures only after founder approval, the operational gate in `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md`, and alignment with `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md`. Addresses below are explicit non-production placeholders (repeating hex digit patterns).

| trial_id | chain | category | contract_address | source_status_before_trial | expected_lookup_goal | risk_notes | trial_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | base | ERC20-like | `0x1111111111111111111111111111111111111111` | unknown | Exercise token-style ABI/source read path if verified | Placeholder only; not asserted live-verified by Sentinel in this doc | not_run |
| T02 | base | NFT-like | `0x2222222222222222222222222222222222222222` | unknown | Exercise NFT-style (ERC721/1155-like) lookup when verified | Placeholder only | not_run |
| T03 | base | proxy-like | `0x3333333333333333333333333333333333333333` | unknown | Exercise proxy/implementation metadata when available | Placeholder only | not_run |
| T04 | base | router/pool-like | `0x4444444444444444444444444444444444444444` | unknown | Exercise router/pool-style surface for heuristics alignment | Placeholder only | not_run |
| T05 | base | generic/utility | `0x5555555555555555555555555555555555555555` | unknown | Exercise generic utility contract path | Placeholder only | not_run |

Field defaults (all placeholder rows): `source_status_before_trial: unknown`; `trial_status: not_run` until a future trial executes and evidence is recorded.

## 6) Pre-trial validation checklist

Before any live trial execution (future; not performed by this document):

- founder approval recorded
- provider selected per trial plan ranking
- endpoint and terms reviewed
- max request count confirmed
- timeout confirmed against config
- rollback flag and owner confirmed
- .env unchanged proof for CI/local gate (tests assert hash stability; no automated write to the repo .env file)
- no paid call requirement for the scoped trial
- no public guarantee wording in materials tied to the trial

## 7) Success/failure evidence

- Before recording any trial evidence, use the field set and privacy rules in `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md` (sanitized rows only).
- Record response status codes or adapter outcomes only after a future trial runs and evidence exists.
- Record provider error type on failure (timeout, rate limit, invalid payload, provider down) using adapter vocabulary.
- Record fallback behavior observed (e.g., unknown status, confidence impact).
- Do not update product claims or the claims ledger for live ABI/source completeness until trial evidence exists and is reviewed.

## 8) Public claim controls

**Allowed**

- Trial dataset prepared (planning artifact).
- Provider trial not run (no live lookup performed for this dataset step).
- ABI/source provider disabled by default.

**Forbidden** for public copy tied to this dataset

- Any claim that placeholder addresses were validated as correct production contracts by a live lookup in this task.
- Implying universal ABI availability or explorer completeness for Base.
- Implied universal verified-source completeness.
- Implied assurance of third-party source verification.
- Implied trap or malicious-pattern detection guarantees.
- Implied outcome guarantees for user funds or execution safety.
- Implied MEV suppression or mempool control from ABI/source trial scope.
- Implied live external simulation as part of this dataset step.

## 9) Cross-references

- `reports/provider_trials/abi_source_trial_results.sample.json` / `.md` (static sanitized evidence **shape** only; all rows `not_run`; not trial evidence)
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md` (review before replacing placeholders or executing any live lookups)
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md` (required format before recording trial evidence; dry-run skeleton output is **not trial evidence** on its own)
- `docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md`
- `docs/18_investor/CLAIMS_LEDGER.md`

This dataset does not integrate a live provider, does not assert fixture addresses without a separate approved list, and does not replace local scanner fixture behavior.
