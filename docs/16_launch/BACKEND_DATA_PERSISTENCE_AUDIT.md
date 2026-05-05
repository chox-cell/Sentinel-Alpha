# Backend data persistence audit (v5 pre-implementation)

Scope: current backend/runtime audit before further v5 engine work.  
Constraints: no runtime changes, no website changes, no secret exposure.

## 1) Current backend entrypoints

Primary API app: `apps/api/main.py`

### Public route
- `POST /contracts/risk-score` (main product endpoint)

### Public/operational route
- `GET /health`

### Internal routes (status/ops)
- `/internal/env/source`
- `/internal/cache-metrics`
- `/internal/manifest`
- `/internal/quicknode-live-check`
- `/internal/rate-limit/status`
- `/internal/security/status`
- `/internal/dlq/status`
- `/internal/ingestion/status`
- `/internal/identity/status`
- `/internal/identity/erc8004/status`
- `/internal/attestation/status`
- `/internal/x402/status`
- `/internal/x402/pricing`
- `/internal/x402/lanes`
- `/internal/x402/challenge`
- `/internal/x402/verification/status`
- `/internal/x402/replay/status`
- `/internal/x402/settlements/status`
- `/internal/x402/onchain/status`

## 2) Current runtime architecture

Request flow for `/contracts/risk-score`:
1. Request enters FastAPI route (`apps/api/main.py`).
2. In-memory per-IP rate limit check (process memory, not durable).
3. x402 gate (`services/x402/payment.py`) validates demo or real payment header paths.
4. Risk service (`services/risk_service/service.py`) runs cache lookup + analysis.
5. Scanner engine (`services/scanner_engine/engine_v0.py`) runs:
   - address normalization,
   - deterministic signal extraction (`services/signals/extractor.py`),
   - chain-read classification (`chain_read_adapter.py`) when configured,
   - conservative asset classification (`asset_classification.py`).
6. Mycelium decision engine (`services/mycelium_engine/engine.py`) computes score/confidence/action/threat class.
7. Attestation layer signs decision payload and returns attestation block.
8. Response includes billing metadata (`billing.method = x402`, status amount/lane metadata).
9. Background tasks schedule event log write + outcome memory write.

## 3) Data persistence matrix

| Data type | Saved now? | Where/how | Notes |
|---|---|---|---|
| scan requests | Partially | `logs/events.log` payload logging | Not a dedicated request table; request+response payload is logged as event row. |
| risk results | Yes (partial) | Redis response cache + `logs/outcome_memory.jsonl` + event log payload | Cache TTL-based; outcome memory stores selected decision record fields. |
| attestations | Yes (embedded) | In API response + outcome memory row + event payload | No standalone attestation ledger/table yet. |
| x402 payment challenges | No durable ledger | Generated on demand in-memory response | Challenge template returned; not persisted as separate records. |
| settled payments | Yes | `logs/x402_settlements.jsonl` | Settlement ledger is filesystem JSONL. |
| contract metadata | No structured persistence | Derived per request from signals/chain-read | Not persisted in dedicated store. |
| chain-read results | No standalone store | Included in response `meta.chain_read` and logs if payload captured | No chain-read history table. |
| asset classifications | No standalone store | Included in response `meta.asset` | Additive metadata only; no dedicated datastore yet. |
| logs | Yes | `logs/events.log`, `logs/dlq.jsonl`, cache metrics JSON, payment/settlement logs | Local filesystem log persistence. |
| users/accounts | No | N/A | No user/account subsystem in current backend API flow. |
| API keys | Not persisted by app logic | Env-based config only | Read from env; no DB-backed key management observed. |
| analytics | Minimal local | `logs/cache_metrics.json`, event log | No warehouse/BI pipeline in current code. |
| rate limits | Ephemeral only | in-process dict `_RATE_LIMIT_BUCKETS` | Reset on process restart; no durable store. |
| cache | Yes | Redis (`services/cache/redis_client.py`) | Risk response caching with TTL (`setex`). |

## 4) Current storage systems

### Present
- Redis (localhost db 0) for API response cache.
- Filesystem logs under `logs/`:
  - `events.log`
  - `outcome_memory.jsonl`
  - `verified_outcomes.jsonl`
  - `x402_payments.jsonl`
  - `x402_settlements.jsonl`
  - `dlq.jsonl`
  - `cache_metrics.json`
  - `replay.jsonl` (worker replay path)
  - `phi_state.json` (mycelium phi state)

### Not present (in current backend runtime path)
- Postgres/Supabase: no active runtime persistence integration observed for core risk/x402 path.
- SQLite: not used in backend service path.
- Cloud object storage: not used in current risk/x402 path.

## 5) Environment config (names only)

Observed config names relevant to backend/runtime:

- `APP_ENV`
- `PUBLIC_BASE_URL`
- `PAYMENT_MODE`
- `PAYMENT_DEMO_SIGNATURE`
- `X402_ENABLED`
- `X402_ONCHAIN_VERIFY`
- `X402_MOCK_ONCHAIN_VERIFY`
- `X402_NETWORK`
- `X402_REVENUE_ADDRESS`
- `SENTINEL_TREASURY_WALLET`
- `AGENT_WALLET_ADDRESS`
- `BASE_RPC_URL`
- `SENTINEL_CHAIN_READ_ENABLED`
- `SENTINEL_WHATSABI_ENABLED`
- `PRICE_BASIC`
- `PRICE_EXECUTIVE`
- `PRICE_PREMIUM`
- `PRICE_PRIORITY`
- `X402_DEFAULT_PRICE_USDC`
- `CDP_PROJECT_ID`
- `CDP_API_KEY_NAME`
- `CDP_API_KEY_ID`
- `CDP private-key env var` (name intentionally omitted in launch docs)
- `CDP key-secret env var` (name intentionally omitted in launch docs)
- `RATE_LIMIT_ENABLED`
- `RATE_LIMIT_PER_MINUTE`
- `QUICKNODE_DRY_RUN`
- `QUICKNODE_WEBHOOK_URL`
- `QUICKNODE webhook signing key env var` (name intentionally omitted in launch docs)
- `QUICKNODE_CHAIN`
- `QUICKNODE_WEBHOOK_ID`
- `QUICKNODE_TEMPLATE_ID`
- `QUICKNODE_SIGNATURE_REQUIRED`
- `SENTINEL_IDENTITY_MODE`
- `SENTINEL_AGENT_DID`
- `SENTINEL_ERC8004_CONTRACT_ADDRESS`
- `ERC8004_ENABLED`
- `ERC8004_REGISTRY_ADDRESS`
- `ERC8004_AGENT_ID`
- `SENTINEL attestation signing key env var` (name intentionally omitted in launch docs)
- `SENTINEL_ATTESTATION_PUBLIC_KEY`
- `PHI_LEARNING_RATE`

No secrets are listed here; names only.

## 6) Gaps before v5 engine expansion

### v5.1 (asset/contract intelligence) gaps
- Dedicated scan persistence is not normalized (currently mixed event log + outcome memory JSONL).
- No contract metadata store/history (asset type, chain-read trends, admin/proxy/source signals).
- Asset classification cache/history is not modeled separately (only response metadata).
- No schema-backed analytics for classification quality over time.

### v5.5 (simulation boundary) gaps
- No simulation job queue/worker persistence boundary yet.
- No simulation-result ledger keyed by trace/contract/chain.
- No durable attestation ledger (only embedded records).
- Payment ledger exists as JSONL but may need migration path for higher volume querying.
- Rate-limit and replay controls are partly file/in-memory; may need stronger centralized persistence.

### Operational scale gaps
- Redis is used for cache only; no queue/backpressure structure yet.
- Filesystem JSONL logs are simple and effective but can become operationally brittle at higher throughput.

## 7) Recommendation

### Keep stateless now (short term)
- Keep risk scoring stateless at request compute layer.
- Keep additive metadata in response (`meta.chain_read`, `meta.asset`) and avoid schema-breaking changes.
- Keep x402 gate behavior unchanged and conservative.

### Add before v5.5 simulation
- Introduce a durable, queryable store for:
  - scan request envelope + normalized result summary,
  - simulation job records and outputs,
  - attestation lookup ledger (trace-indexed),
  - payment/replay records (migration from flat JSONL when needed).
- Add an explicit queue boundary for simulation/adapters (Redis queue or equivalent worker queue).
- Add contract/asset signal cache with TTL + provenance fields for chain/source/ABI reads.

### Postpone until traffic warrants
- Full analytics warehouse and complex BI.
- Deep per-user account management in backend API (if still single endpoint product mode).
- Multi-region persistence complexity before sustained demand.

## Notes on safety posture

- Current architecture is mostly stateless compute + lightweight persistence sidecars (Redis + local logs).
- This is acceptable for early-stage velocity, but v5.x depth (especially simulation and intent layers) will need stronger persistence primitives.
- Documentation intentionally avoids exposing secret values and uses no secret material.
