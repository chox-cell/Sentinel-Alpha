# Blockscout Base Endpoint Source Pack v12.0

## 2) Purpose

Collect **source-backed** candidate information for choosing a **Blockscout-compatible Base (chain id 8453)** base URL **before** any Blockscout endpoint validation (see `docs/16_launch/BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md`). This file is a **documentation-only source pack**: it does **not** call Blockscout, run validation, enable providers, require API keys, change `.env`, or store raw HTTP bodies.

## 3) Current status

- **Blockscout endpoint validation plan** exists (`docs/16_launch/BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md`); no Blockscout endpoint validation has run.
- No Blockscout base URL has been selected for runtime or committed as a live default here.
- Provider remains disabled by repository posture.
- Full trial remains blocked until endpoint validation and separate founder gates succeed.
- **`.env.example`** contains **`BLOCKSCOUT_BASE_URL=`** placeholder only (no live value required for this pack).

### Selection status

```
selected_candidate_id: B01
endpoint_validation_blocked: true
reason: validation phrase not yet given
```

**Note:** **B01** is **selected for future validation only**. No network validation has run.

### Explicit non-claims

- No endpoint validation run from this documentation revision.
- Endpoint **not** proven reachable (no probe; no “endpoint works” claim).
- No usable metadata received from Blockscout in this step.
- Provider disabled; no runtime provider activation authorized here.

## 4) Source requirements

Before any endpoint validation, a **chosen** candidate must be documented with:

- `source_url` — canonical citation for where the endpoint or API contract was observed (or `REQUIRED_SOURCE_URL` until replaced).
- `source_label` — short human label for the citation.
- `observed_endpoint_or_docs_path` — path pattern or docs-relative description (not a live probe from this file).
- `chain`: **base**
- `chain_id`: **8453**
- `evidence_note` — what the source supports vs does not prove (no “endpoint works” claim from this pack alone).
- `confidence`: **low** / **medium** / **high** (default **low** until verified sources replace placeholders).
- `selected_for_validation`: **true** for **at most one** row chosen for a future validation window (v12.0: **B01**); other rows remain **false**.
- `validation_status`: **not_run** until a future approved validation records otherwise.

## 5) Candidate table

- **B01** is the **single selected** candidate for a **future** one-target Blockscout endpoint validation (`selected_for_validation: true`); `validation_status` remains **not_run** until an approved validation executes.
- **B02** and **B03** remain **not selected** (`selected_for_validation: false`), **source-required placeholders** (`REQUIRED_SOURCE_URL`, `replacement_required: true`) until replaced.

### B01 — Base Mainnet API docs | Blockscout (source-backed)

| Field | Value |
| --- | --- |
| `candidate_id` | B01 |
| `source_url` | https://base.blockscout.com/api-docs |
| `source_label` | Base Mainnet API docs \| Blockscout |
| `observed_endpoint_or_docs_path` | https://base.blockscout.com/api/v2/smart-contracts/{address} |
| `candidate_base_url` | https://base.blockscout.com |
| `chain` | base |
| `chain_id` | 8453 |
| `evidence_note` | Public Base Blockscout API docs surface cited; endpoint shape remains **candidate only** until validation. REST base URL depends on Blockscout instance; here aligned to Base mainnet explorer host. |
| `confidence` | medium |
| `selected_for_validation` | true |
| `validation_status` | not_run |
| `selected_reason` | source-backed Base Blockscout API docs candidate |
| `replacement_required` | false |
| `notes` | Source-backed candidate only; no network validation performed. Additional context: Blockscout REST API overview — https://www.blog.blockscout.com/blockscout-rest-api/ |

### B02 — Base explorer / API candidate (placeholder)

| Field | Value |
| --- | --- |
| `candidate_id` | B02 |
| `source_url` | `REQUIRED_SOURCE_URL` |
| `source_label` | Base explorer/API candidate |
| `observed_endpoint_or_docs_path` | Blockscout-style `…/api/v2/smart-contracts/{address}` template under a Base-listed explorer (to be sourced) |
| `chain` | base |
| `chain_id` | 8453 |
| `evidence_note` | Candidate for Base-aligned explorer hosting; **no** runtime selection or health claim. |
| `confidence` | low |
| `selected_for_validation` | false |
| `validation_status` | not_run |
| `replacement_required` | true |
| `notes` | Requires terms-of-use and stability review before any selection. |

### B03 — Alternate Blockscout-compatible endpoint candidate (placeholder)

| Field | Value |
| --- | --- |
| `candidate_id` | B03 |
| `source_url` | `REQUIRED_SOURCE_URL` |
| `source_label` | Fallback alternate Blockscout-compatible endpoint candidate |
| `observed_endpoint_or_docs_path` | Same API shape family as Blockscout v2 smart-contracts path; base host TBD from verified source |
| `chain` | base |
| `chain_id` | 8453 |
| `evidence_note` | Fallback slot only; compatibility and licensing must be confirmed from sources, not assumed. |
| `confidence` | low |
| `selected_for_validation` | false |
| `validation_status` | not_run |
| `replacement_required` | true |
| `notes` | Use only if B01/B02 are unsuitable after sourced review. |

## 6) Selection rules

- Choose **exactly one** endpoint (one base URL origin) **before** validation.
- **One target** only for the first validation attempt.
- **One endpoint** only per validation attempt.
- **No API key** by default for the planned read-only posture.
- **No raw response body** in committed artifacts.
- **No provider runtime activation** from this documentation step.
- **No trial rerun** and **no dataset-wide lookup** from this pack.

## 7) Future validation phrase

**"green light VPS Blockscout endpoint validation only"**

## 8) Full trial phrase

**"green light rerun Blockscout trial from VPS"**

## 9) Public claim controls

**Allowed**

- Blockscout endpoint **source pack** is **prepared** (this document).
- **B01** is documented as a **source-backed candidate** and is **selected for future validation only** (not a validation result; `validation_status: not_run`).
- Endpoint validation is **still blocked** (`endpoint_validation_blocked: true`) until the founder phrase in §7 is given for an approved run.
- **Provider remains disabled** by default.

**Forbidden** (avoid implying)

- Blockscout endpoint works
- Blockscout integration live
- trial completed
- live ABI coverage
- full verified-source coverage
- guaranteed source verification
- detects honeypots
- guaranteed protection
- production provider active

## 10) Cross-references

- `docs/16_launch/BLOCKSCOUT_ENDPOINT_VALIDATION_PLAN.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_PIVOT_REVIEW.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md`
- `docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md`

This source pack does not perform network calls, select a live runtime URL, or enable providers.
