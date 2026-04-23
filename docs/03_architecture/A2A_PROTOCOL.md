# 🤖 Sentinel Alpha — A2A Protocol

## Purpose
Enable Machine-to-Machine interaction

---

## Request

POST /contracts/risk-score

Headers:
- x402-payment
- agent-id
- trace-id

Body:
{
  contract_address: string,
  chain: string,
  tx_context: optional
}

---

## Response

{
  risk_score: number,
  confidence: number,
  action: "BLOCK | REDUCE | ALLOW | EXIT_NOW | REVIEW",
  emergency_signal: string,
  latency_ms: number,
  trace_id: string
}

---

## Payment

- Model: x402
- Paid per request

---

## Rules

- stateless request
- deterministic output
- latency critical

---

## Failure Modes

- timeout → return REVIEW
- insufficient data → REVIEW
