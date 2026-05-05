# Cost discipline plan (pre-revenue)

## 1) Current cost posture

- Target monthly infrastructure cost: `<= $10` before revenue.
- Contabo VPS is the core paid infrastructure.
- Static website + API remain on the VPS baseline.
- npm public package (`@beezshield/sentinel`) has no direct hosting cost.
- Cloudflare DNS/SSL can remain on free tier when applicable.

## 2) Service cost table

| Service area | Current decision | Cost discipline |
|---|---|---|
| Contabo VPS | Keep | Low-cost baseline; primary runtime host |
| QuickNode / paid RPC | Avoid paid until real traffic | Use existing/free reads first; add budget-gated only when needed |
| Postgres / Supabase / Neon | Postpone managed DB | No managed DB before clear durability/customer need |
| Redis | Use local/existing | Avoid managed Redis now |
| Simulation providers | Roadmap only | No paid simulation calls now |
| Monitoring | Free/basic logs now | Keep local/basic observability until load justifies upgrades |
| Backups | VPS file backups now | Keep simple file-level backup routine first |

## 3) Upgrade triggers

### QuickNode / paid RPC only if
- sustained real scans/day threshold is reached,
- provider failures materially hurt UX/SLA,
- v5.3 or v5.5 reliability goals require stronger RPC guarantees.

### Managed Postgres only if
- paid scans or paying customers exist,
- durable scan history/query depth is required,
- attestation/payment ledger must be normalized and queryable,
- dashboard/auth and account-level persistence becomes required.

### Managed Redis/queue only if
- repeated scans overload synchronous API handling,
- simulation jobs require reliable queue semantics,
- local Redis reliability becomes insufficient.

## 4) Roadmap tracking (cost gates)

- v5.1 and v5.2 should remain no-extra-cost (metadata/signal layers on current stack).
- v5.3 should prefer cached/free reads where possible before any paid RPC expansion.
- v5.5 simulation adapter should be interface-first; no paid provider until demand.
- v5.6 explanation engine should not require extra paid infrastructure.
- v5.7 chain support expansion may require explicit RPC budget planning.
- v6 data-provider ladder should progress local/free-first before any paid provider activation.
- v6.3 local risk history DB should start as local Postgres planning/optional rollout, with no managed DB default.

## 5) Forbidden actions

- Do not add paid QuickNode by default.
- Do not add managed Postgres before need.
- Do not store secrets in repo.
- Do not enable costly chain reads by default.
- Do not introduce simulation paid calls without a budget gate.
