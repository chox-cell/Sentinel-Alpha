# Env safety policy

This policy protects local secret state and prevents accidental env leakage/mutation during development and tests.

## Core rules

- `.env` is sacred local secret state.
- Tests must never write to repo `.env`.
- Tests must never commit `.env`.
- Runtime and scripts must not print secret values.
- `.env.example` is the only env template that may be edited for config names/placeholders.
- `.env.example` may contain placeholders; `.env` must contain local secrets only and must never be mutated by tests.
- Real provider keys stay in local `.env` or secret manager only; never commit provider keys to repo.

## Test design rules

- Do not create helpers that target `repo_root / ".env"` for writes.
- Do not use `_write_repo_env` patterns that mutate `.env`.
- Prefer `monkeypatch.setenv` and direct function-level dependency injection.
- If file-backed behavior must be tested, use temp files outside the repo root.

## Verification guardrails

- Keep `.env` gitignored.
- Add tests that fail if test files include direct writes to `.env`.
- Run CI checks that detect `.env` mutation during test execution.
