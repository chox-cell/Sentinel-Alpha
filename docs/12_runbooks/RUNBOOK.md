# 🏃 Runbook

## System Start

1. start API
2. connect Redis
3. connect DB
4. connect QuickNode

---

## Flow

receive request → process → return decision

---

## Health Check

- latency < 50ms
- error rate < 1%

---

## Restart

restart API + workers
