# Target research method (v4.4)

How to **find**, **verify**, and **record** real builder targets before filling **T01–T20** on `OUTREACH_TRACKER.md`. Follow `OUTREACH_OPERATING_RULES.md` and `FIRST_20_BUILDER_TARGETS.md`.

**Source verification required:** no target name, URL, or org may be written into the tracker until the checklist in this doc is satisfied. Placeholders stay **not contacted** until real outreach happens.

## Search queries (examples)

Use these as starting points; adapt by date and platform. Prefer primary sources (repo, docs, author posts) over second-hand lists.

**AgentKit / agent frameworks**

- `AgentKit` `coinbase` `github`
- `@coinbase/agentkit` OR `agentkit` `typescript` `npm`
- `langgraph` `evm` OR `autonomous agent` `ethereum`

**Base**

- `base` `chain id` `8453` `github`
- `viem` `base` `mainnet` OR `onchainkit` `base`
- `farcaster` `base` bot OR agent (watch for noise)

**x402 / payment-required APIs**

- `x402` `402` `payment` `api` `github`
- `HTTP 402` `crypto` `micropay`
- `pay per call` `api` `stablecoin`

**Trading / wallet / contract agents**

- `trading bot` `typescript` `ethers` `github`
- `wallet automation` `script` `web3`
- `defi` `agent` `contract call` autonomous

Combine categories when screening (e.g. Base + agent + recent commits).

## Scoring method

Use the **same +1 rubric** as `FIRST_20_BUILDER_TARGETS.md` (Base, AgentKit or similar, autonomous contract execution, GitHub active in 90 days, security/risk pain). Sum → map to relevance **1–5**. Record the score **after** verification—do not inflate for outreach optimism.

## Verification checklist before adding a target

Complete **all** before filling a tracker row with a real name/link:

1. **Canonical URL** — GitHub org/repo, company site, or community URL you will cite in **Link**.
2. **Evidence of fit** — at least one concrete signal (README, package.json, chain config, public post) matching the category.
3. **Recency** — default expectation: activity or relevance within **90 days** unless the project is clearly maintenance-mode but still relevant.
4. **Identity** — org or maintainer is identifiable; anonymous throwaways get extra scrutiny or skip.
5. **No scrape-only guesses** — if you only saw a keyword hit with no real context, do not add.
6. **Source link for notes** — paste the specific issue, README section, or post URL in **Notes** (see below).

If any step fails, leave the slot **— unassigned —** and **not contacted**.

## Classifying type: repo / builder / community / company

| Type | When to use |
|------|-------------|
| **repo** | Primary touchpoint is a specific open-source repository. |
| **builder** | Individual maintainer or indie dev (may have multiple repos). |
| **community** | Discord server, forum, hackathon collective, or DAO working group as the entry point. |
| **company** | Incorporated team or startup with a product; outreach may go through founders or devrel. |

Pick the **first outreach surface** you will use (one row = one primary type).

## How to avoid spam

- One tailored message per target; no mail-merge tone.
- Prefer **issues / discussions / PR comments** where the project invites feedback over cold blast DMs.
- Space outbound messages; respect **max one follow-up** from `OUTREACH_OPERATING_RULES.md`.
- Skip targets that explicitly discourage unsolicited contact.

## How to record source link

In **Notes** (and optionally in **Reason**), record:

- **What you saw:** e.g. “README states Base mainnet” or “package depends on @coinbase/agentkit”.
- **Primary source URL** — the exact page (commit-permalink ok for GitHub files).

Do not rely on “heard from someone” without a link.

## How to avoid fake claims

- **Never** mark **contacted** or **integrated** without real events; placeholders remain **not contacted** until you send a message.
- **Integrated** only after verifiable adoption (e.g. merged PR using Sentinel, or written confirmation of production use).
- **Product truth in outreach:** npm SDK `@beezshield/sentinel` is live; **AgentKit-style example** exists in-repo; **official provider coming next**; no promise of automatic payment settlement; no safety warranty.

Cross-check copy with `BUILDER_OUTREACH_PACK.md` before sending.
