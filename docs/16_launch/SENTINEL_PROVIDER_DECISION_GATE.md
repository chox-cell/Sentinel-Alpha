# Sentinel provider decision gate (v6.7)

## 1) Purpose

This document defines a strict decision gate for future provider activation.
It is a policy guardrail, not provider activation itself.

## 2) Current status

- local analyzers are live.
- fixture dataset and local evaluation report artifacts are live.
- ABI/source provider boundary exists.
- Source/ABI cache boundary exists.
- simulation provider adapter boundary exists.
- mempool/MEV boundary exists.
- real external providers are not enabled by default.

## 3) Provider categories

- ABI/source provider activation plan (first candidate category):
  `docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md`
- ABI/source disabled wiring skeleton step (pre-activation readiness):
  `services/scanner_engine/abi_source_provider_config.py`
- ABI/source provider
- RPC/chain-read provider
- simulation provider
- mempool/MEV provider
- historical risk database
- managed cache/database

## 4) Activation requirements

A provider may only be activated if all are true:

- explicit founder approval
- documented provider name
- estimated monthly cost
- budget trigger met
- fallback behavior tested
- timeout/error handling tested
- no secrets in repo
- `.env.example` only includes empty placeholders
- tests prove `.env` unchanged
- public claims updated conservatively
- rollback plan exists

## 5) Budget triggers

- pre-revenue target remains <= $10/mo
- paid provider allowed only after:
  - paid scans,
  - committed pilot,
  - repeated integration demand,
  - or a specific technical blocker that local analysis cannot solve
- default: no paid providers

## 6) Risk triggers

Provider activation requires:

- rate-limit handling
- timeout handling
- invalid response handling
- provider down fallback
- confidence reduction on missing data
- no hard dependency on provider success

## 7) Claim controls

Even after provider activation:

- no guaranteed protection
- no "detects honeypots" claim unless simulation evidence proves specific scoped cases
- no MEV prevention claim
- no full bytecode coverage claim
- no full chain coverage claim

## 8) Rollback requirements

- provider can be disabled with one flag
- API response remains backward compatible
- fallback mode returns safe metadata
- no top-level schema break

## 9) Decision record template

- provider:
- purpose:
- cost:
- activation flag:
- fallback behavior:
- tests:
- public copy changes:
- rollback plan:
- approval date:
