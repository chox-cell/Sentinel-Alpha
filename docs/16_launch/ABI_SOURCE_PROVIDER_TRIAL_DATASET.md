# Known Base Contracts Trial Dataset v1

## 2) Purpose

Defines candidate contract categories and sourced public Base address records for a future controlled ABI/source provider trial. This file is documentation and planning only. The dataset is not active now. It does not call providers, verify addresses against live endpoints in automation, require API keys, or change runtime behavior.

## 3) Current status

- Dataset is planning-only.
- No provider calls have been made by authoring this document.
- Real target selection is prepared for review; no address is claimed verified by a live provider lookup in this document.
- Provider remains disabled by default in shipping configuration.
- Max 5 trial targets for the controlled trial scope (see trial plan).
- Dataset rows remain `trial_status: not_run` in this table; v10.8A attempted outcomes are recorded separately in `reports/provider_trials/abi_source_trial_results.v10.8.attempted.json`.
- Dataset-wide scripted lookups against all five rows remain blocked until endpoint validation succeeds on one representative target per `SOURCIFY_ENDPOINT_CORRECTION_PLAN.md`.
- v11.4 recorded a one-target endpoint validation attempt for T01 only (`reports/provider_trials/sourcify_endpoint_validation.v11.4.json`); dataset-wide scripted use of all rows remains blocked until a successful representative validation and explicit trial rerun approval.

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
- Include `source_url` for every real address candidate.
- If a category cannot be sourced safely in a future revision, keep a placeholder address and mark `replacement_required: true`.
- Privacy redaction pattern for future non-public examples remains `0x...`; the concrete addresses below are public contract candidates only.

## 5) Trial target table

Exactly five public Base contract target candidates are prepared for future review. Source URLs are public address/source pages only; Sentinel has not performed a live provider lookup or verified these contracts in runtime. If any row is rejected during review, replace it before live execution rather than running against placeholders or user wallets.

| trial_id | chain | chain_id | category | contract_address | source_url | source_label | source_status_before_trial | expected_lookup_goal | risk_notes | trial_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | base | 8453 | ERC20-like | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | `https://basescan.org/address/0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913#code` | BaseScan address/source page for USDC on Base | unknown | Exercise token-style ABI/source read path if provider returns metadata | Public contract candidate only; no Sentinel live lookup or source verification claim in this doc | not_run |
| T02 | base | 8453 | NFT-like | `0xBa5e05cb26b78eDa3A2f8e3b3814726305dcAc83` | `https://basescan.org/address/0xBa5e05cb26b78eDa3A2f8e3b3814726305dcAc83#code` | BaseScan address/source page for BasePaint-style NFT/1155 candidate | unknown | Exercise NFT-style (ERC721/1155-like) lookup if provider returns metadata | Public contract candidate only; category remains pre-trial review context, not Sentinel verification | not_run |
| T03 | base | 8453 | proxy-like | `0x4200000000000000000000000000000000000006` | `https://basescan.org/address/0x4200000000000000000000000000000000000006#code` | BaseScan address/source page for Base WETH/predeploy candidate | unknown | Exercise proxy/predeploy/implementation metadata handling when available | Public contract candidate only; proxy-like classification is a trial exercise target, not a coverage claim | not_run |
| T04 | base | 8453 | router/pool-like | `0x2626664c2603336E57B271c5C0b26F421741e481` | `https://basescan.org/address/0x2626664c2603336E57B271c5C0b26F421741e481#code` | BaseScan address/source page for Uniswap SwapRouter02 on Base | unknown | Exercise router/pool-style surface for heuristics alignment | Public contract candidate only; no execution simulation or routing safety claim | not_run |
| T05 | base | 8453 | generic/utility | `0xca11bde05977b3631167028862be2a173976ca11` | `https://basescan.org/address/0xca11bde05977b3631167028862be2a173976ca11#code` | BaseScan address/source page for Multicall3-style utility candidate | unknown | Exercise generic utility contract ABI/source lookup path | Public contract candidate only; no Sentinel live lookup or verified-source guarantee | not_run |

Field defaults (all rows): `source_status_before_trial: unknown`; `trial_status: not_run` until a future trial executes and evidence is recorded. No `replacement_required: true` row is present in this v10.7 candidate set because each row includes a public `source_url`.

## 6) Pre-trial validation checklist

Before any live trial execution (future; not performed by this document):

- founder approval recorded
- sourced target review completed
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
- Real public Base target candidates prepared for future review.
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
