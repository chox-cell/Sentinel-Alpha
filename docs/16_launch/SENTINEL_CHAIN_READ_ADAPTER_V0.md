# Sentinel Chain Read Adapter v0

## Role
The Python service does not embed the Viem JavaScript library. Chain reads use a small **JSON-RPC adapter** (`services/scanner_engine/chain_read_adapter.py`) with the same responsibilities a future Viem-based worker or TypeScript SDK would cover: `eth_getCode`, readiness checks, and account classification from bytecode presence.

## Public Boundary
- `get_chain_readiness(chain)` — whether reads are allowed for the chain, RPC is configured, and the opt-in flag is on.
- `get_contract_code(address, chain)` — `eth_getCode` with safe error mapping; **never** returns or logs provider URLs.
- `classify_account_type(address, chain)` — `contract` | `eoa` | `unknown` from bytecode (unknown on RPC errors or missing reads).

## Opt-In: `SENTINEL_CHAIN_READ_ENABLED`
`BASE_RPC_URL` may exist for other features (for example payment verification). Bytecode reads are **off by default** so accidental RPC usage does not change risk confidence in environments that only wanted payments wired.

Set `SENTINEL_CHAIN_READ_ENABLED=true` to allow `eth_getCode` when `BASE_RPC_URL` is set and `chain` is supported (currently **base** only).

## Status Values
Reads surface `chain_read_status` in `meta.chain_read`:
- `ok` — JSON-RPC succeeded.
- `not_configured` — no RPC URL.
- `reads_disabled` — RPC present but chain reads flag is false.
- `unsupported_chain` — chain not wired to this adapter yet.
- `provider_error` — HTTP/JSON-RPC failure or malformed payload.
- `invalid_address` — address failed basic validation before a call.
- `unavailable` — reserved path for sentinel-only skips (for example enforced zero-address posture without asserting live bytecode semantics).

Heuristic ints on `signals` (additive, backward compatible):
- `contract_code_available`
- `eoa_account` (EOA lowers confidence caps when bytecode read succeeds)
- `unknown_account_kind` (only after `provider_error`—not for absent/disabled RPC)
- `chain_read_provider_unavailable` (marks degraded read posture without faking bytecode proof)

## What Is Still Not Live
This adapter confirms bytecode **presence**. It does not perform deep bytecode analysis, WhatsABI decoding, or static analysis pipelines—those belong in future scanner tiers.
