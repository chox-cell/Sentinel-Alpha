# 🤖 Sentinel Alpha — AI Builder Pack

## Purpose

Control all AI builders (Claude, Cursor, Codex)

---

## Core Rule

AI must FOLLOW SSOT

Never:
- rename system
- change endpoint
- change pipeline
- modify agent names

---

## Build Mode

AI builds ONLY:

- modules
- functions
- logic

NOT:
- architecture
- system identity

---

## Input Context

Always load:

- SSOT.md
- TRUTH.md
- ARCHITECTURE.md
- ACTION_POLICY.md

---

## Output Expectation

AI must produce:

- clean code
- deterministic logic
- no hallucination

---

## Failure Rule

If AI violates SSOT:

→ reject output
