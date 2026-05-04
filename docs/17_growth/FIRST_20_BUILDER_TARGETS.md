# First 20 builder targets (v4.4)

Define **categories**, score prospects with a transparent rubric, then assign the top fits into **T01–T20** on `OUTREACH_TRACKER.md`.

## Source verification required

Every row moved off **— unassigned —** must pass **`TARGET_RESEARCH_METHOD.md`** verification (canonical URL, evidence, recency, source link in Notes). **Source verification required** before any real name or URL appears in the tracker.

Do **not** list real repos or people in this file as a substitute for the tracker—research feeds **OUTREACH_TRACKER.md** row-by-row. Until research is done, **T01–T20** stay placeholders with status **not contacted** (do not fake **contacted** or **integrated**).

## Target categories

Use these buckets when sourcing the first 20 outreach targets:

| Category | What to look for |
|----------|-------------------|
| **AgentKit builders** | Teams or solo builders wiring agents with Coinbase AgentKit-style flows (example integrations, tutorials, OSS). |
| **Base autonomous agents** | Agents or bots targeting **Base** (8453) for execution or policy loops. |
| **x402 builders** | Projects already talking about HTTP 402 / payment-required flows, micropayments, or pay-per-call APIs. |
| **Onchain trading bots** | Strategies that sign and send tx onchain; pre-execution checks reduce blind execution. |
| **Wallet automation bots** | Scripts that move funds, swap, or batch operations from hot or custodial-adjacent flows. |
| **Contract execution agents** | Agents that call contracts autonomously (defi, routing, MEV-adjacent helpers, etc.). |

## Scoring (0–5 relevance, sum of flags)

For each candidate, add **+1** for each true row (cap interpretation honestly—if unsure, do not add the point):

| +1 if… | Rationale |
|--------|-----------|
| **Uses Base** | Execution or primary chain context is Base (or clearly migrating to it). |
| **Uses AgentKit or similar** | AgentKit, LangGraph-style agents, or another agent framework with tool execution. |
| **Executes contracts autonomously** | Non-trivial onchain calls without a human in the loop for each step. |
| **Active GitHub in last 90 days** | Commits, issues, or releases indicating the project is alive. |
| **Likely security / risk pain** | Handles user funds, high-value txs, or has been public about incidents, audits, or safety concerns. |

**Map score to relevance (1–5) for the tracker:**

| Sum | Tracker “Relevance (1–5)” |
|-----|---------------------------|
| 0–1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 5 |

## Integration handoff (truthful)

When outreach lands, builders can evaluate:

- **npm SDK (live):** `@beezshield/sentinel` — `npm install @beezshield/sentinel`
- **AgentKit-style example:** in-repo pattern (not an official Coinbase AgentKit provider); **official provider coming next**
- **Truth:** risk signals support decisions; they do not replace audits, monitoring, or a promise of protection
- **x402:** unpaid API paths may return a payment challenge; builders wire settlement in their own code (SDK does not auto-settle)
