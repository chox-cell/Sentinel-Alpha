-- Sentinel Alpha local risk history schema v1 (v6.3.1 planning artifact)
-- Local-first schema only. Runtime writes are not enabled in this stage.
-- Security posture:
-- - no private keys
-- - no seed phrases
-- - no raw secrets
-- - payment proof minimized
-- - sensitive identifiers should be hashed/redacted where needed

CREATE TABLE IF NOT EXISTS scan_requests (
    id uuid PRIMARY KEY,
    trace_id text UNIQUE,
    chain text NOT NULL,
    contract_address_hash text NOT NULL,
    requested_action text,
    request_context jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS risk_results (
    id uuid PRIMARY KEY,
    request_id uuid NOT NULL REFERENCES scan_requests(id),
    attestation_id uuid,
    score numeric(6,2) NOT NULL,
    confidence numeric(6,4) NOT NULL,
    action text NOT NULL,
    threat_class text NOT NULL,
    decision_payload jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS contract_observations (
    id uuid PRIMARY KEY,
    request_id uuid REFERENCES scan_requests(id),
    chain text NOT NULL,
    contract_address_hash text NOT NULL,
    observation_type text NOT NULL,
    observation_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS asset_classifications (
    id uuid PRIMARY KEY,
    request_id uuid NOT NULL REFERENCES scan_requests(id),
    asset_type text NOT NULL,
    asset_confidence numeric(6,4),
    classification_basis jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS security_signals (
    id uuid PRIMARY KEY,
    request_id uuid NOT NULL REFERENCES scan_requests(id),
    signal_namespace text NOT NULL,
    signal_snapshot jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS attestations (
    id uuid PRIMARY KEY,
    request_id uuid NOT NULL REFERENCES scan_requests(id),
    trace_id text,
    attestation_digest text NOT NULL,
    agent_identity text,
    attestation_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS x402_payment_events (
    id uuid PRIMARY KEY,
    request_id uuid REFERENCES scan_requests(id),
    payment_reference_hash text,
    payment_status text NOT NULL,
    verification_status text,
    amount text,
    network text,
    payment_payload_min jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS integration_clients (
    id uuid PRIMARY KEY,
    client_ref_hash text,
    client_label text,
    client_type text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS provider_observations (
    id uuid PRIMARY KEY,
    request_id uuid REFERENCES scan_requests(id),
    provider_name text NOT NULL,
    provider_status text NOT NULL,
    error_type text,
    chain text,
    observation_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_scan_requests_chain_contract
    ON scan_requests (chain, contract_address_hash);

CREATE INDEX IF NOT EXISTS idx_scan_requests_created_at
    ON scan_requests (created_at);

CREATE INDEX IF NOT EXISTS idx_risk_results_request_id
    ON risk_results (request_id);

CREATE INDEX IF NOT EXISTS idx_risk_results_attestation_id
    ON risk_results (attestation_id);

CREATE INDEX IF NOT EXISTS idx_risk_results_created_at
    ON risk_results (created_at);

CREATE INDEX IF NOT EXISTS idx_contract_observations_chain_contract
    ON contract_observations (chain, contract_address_hash);

CREATE INDEX IF NOT EXISTS idx_contract_observations_request_id
    ON contract_observations (request_id);

CREATE INDEX IF NOT EXISTS idx_asset_classifications_request_id
    ON asset_classifications (request_id);

CREATE INDEX IF NOT EXISTS idx_security_signals_request_id
    ON security_signals (request_id);

CREATE INDEX IF NOT EXISTS idx_attestations_request_id
    ON attestations (request_id);

CREATE INDEX IF NOT EXISTS idx_attestations_trace_id
    ON attestations (trace_id);

CREATE INDEX IF NOT EXISTS idx_x402_payment_events_request_id
    ON x402_payment_events (request_id);

CREATE INDEX IF NOT EXISTS idx_x402_payment_events_reference_hash
    ON x402_payment_events (payment_reference_hash);

CREATE INDEX IF NOT EXISTS idx_provider_observations_request_id
    ON provider_observations (request_id);

CREATE INDEX IF NOT EXISTS idx_provider_observations_created_at
    ON provider_observations (created_at);
