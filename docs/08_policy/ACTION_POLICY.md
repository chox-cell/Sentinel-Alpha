# ⚖️ Action Policy (LOCKED LOGIC)

## Decision Mapping

IF risk_score >= 85:
→ BLOCK

IF 65 <= risk_score < 85:
→ REDUCE

IF risk_score < 65:
→ ALLOW

---

## Emergency Overrides

IF oracle_dislocation > threshold:
→ EXIT_NOW

IF simulation_revert == true:
→ BLOCK

IF insufficient_data:
→ REVIEW

---

## Priority Rules

1. EXIT_NOW overrides everything
2. BLOCK overrides REDUCE
3. REVIEW only if confidence < 0.5

---

## Output Guarantee

System must ALWAYS return:
- action
- confidence
- reason (optional)
