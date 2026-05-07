# Sentinel local risk history DB plan (v6.3)

## 1) Purpose

v6.3 prepares durable risk history design for scans, decisions, and signal lineage while keeping current runtime unchanged.  
This stage is docs/schema planning only and does not enable runtime DB dependency yet.

## 2) Current persistence state

- Redis TTL cache is active for response caching.
- JSONL outcome/payment/settlement logs are active for local persistence.
- No normalized Postgres/Supabase runtime integration is active today.
- No managed DB before need.

## 3) Proposed local-first Postgres schema

### `scan_requests`
- **Purpose:** durable envelope for submitted scan inputs and execution context.
- **Key fields:** `id`, `trace_id`, `chain`, `contract_address_hash`, `requested_action`, `created_at`.
- **Retention/privacy notes:** avoid storing raw headers; hash/redact client identifiers.

### `risk_results`
- **Purpose:** normalized decision/risk outputs linked to request history.
- **Key fields:** `id`, `scan_request_id`, `score`, `confidence`, `action`, `threat_class`, `created_at`.
- **Retention/privacy notes:** keep computed outputs and minimal context only.

### `contract_observations`
- **Purpose:** track observed contract-level metadata over time.
- **Key fields:** `id`, `chain`, `contract_address_hash`, `observation_type`, `observation_payload`, `observed_at`.
- **Retention/privacy notes:** hash addresses when feasible; do not store raw secrets.

### `asset_classifications`
- **Purpose:** historical record of asset-type classification decisions.
- **Key fields:** `id`, `scan_request_id`, `asset_type`, `asset_confidence`, `classification_basis`, `created_at`.
- **Retention/privacy notes:** store explainable basis and avoid sensitive user fields.

### `security_signals`
- **Purpose:** append-only signal snapshots (source/proxy/admin, ERC20, NFT, simulation boundary, ABI/source boundary, mempool boundary).
- **Key fields:** `id`, `scan_request_id`, `signal_namespace`, `signal_key`, `signal_value`, `created_at`.
- **Retention/privacy notes:** exclude private material and full raw request headers.

### `attestations`
- **Purpose:** durable attestation ledger keyed by trace and contract context.
- **Key fields:** `id`, `trace_id`, `scan_request_id`, `attestation_digest`, `signed_at`, `agent_identity`.
- **Retention/privacy notes:** store attestation payload digest and metadata, not secret signing keys.

### `x402_payment_events`
- **Purpose:** structured payment verification/replay/settlement event history.
- **Key fields:** `id`, `trace_id`, `payment_status`, `verification_status`, `amount`, `network`, `created_at`.
- **Retention/privacy notes:** keep payment proof minimal; avoid full raw transaction blobs unless required.

### `integration_clients`
- **Purpose:** optional attribution of traffic sources and integration cohorts.
- **Key fields:** `id`, `client_label`, `client_type`, `first_seen_at`, `last_seen_at`.
- **Retention/privacy notes:** hash or redact sensitive identifiers where needed.

### `provider_observations`
- **Purpose:** provider-readiness and adapter-result timeline (ABI/source/simulation/mempool boundaries).
- **Key fields:** `id`, `provider_name`, `provider_status`, `error_type`, `chain`, `observed_at`.
- **Retention/privacy notes:** never store API keys or raw credentials.

## 4) Privacy/security rules

- no private keys.
- no seed phrases.
- no raw secrets.
- avoid storing full request headers.
- hash or redact sensitive identifiers where needed.
- keep payment proof minimal.

## 5) Cost discipline

- local Postgres on VPS first.
- no managed DB until paid scans/customers/dashboard need.
- backups outside repo.
- no Supabase/Neon by default.

## 6) Migration strategy

- v6.3 docs/schema only.
- v6.3.1 SQL schema file exists at `db/schema/local_risk_history_v1.sql`.
- v6.3.2 disabled adapter boundary exists in `services/risk_history/adapter.py` with runtime writes still off by default.
- v6.3.2 write-through optional in a future gated stage.
- v6.3.3 dashboard/API analytics later.
- v9.1 disabled Decision Receipt Store boundary exists in `services/scanner_engine/decision_receipt_store.py` for sanitized receipt history prep.
- migration execution is manual/future only.

## 7) Upgrade triggers

- repeated scans.
- paid scans.
- need attestation ledger.
- customer dashboard.
- simulation history.
- analytics.

## 8) Non-goals

- no runtime DB dependency now.
- no Supabase service role.
- no analytics dashboard.
- no user accounts.
- no managed DB spend.

## Notes

- `DATABASE_URL` is not required yet.
- Supabase is postponed and not default in current runtime posture.
- runtime DB writes are still disabled in current implementation.
- Decision receipts are not persisted by default; v9.1 store boundary remains disabled-by-default.
- No raw contract addresses or raw secrets are allowed in receipt storage records.
- Source / ABI cache boundary is disabled by default.
- managed Redis is postponed by default.
- no secrets/API keys/raw headers are cached.
