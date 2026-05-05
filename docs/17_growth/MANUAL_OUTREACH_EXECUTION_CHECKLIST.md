# Manual Outreach Execution Checklist (v7.4)

## 1) Purpose

This checklist defines manual execution steps for outreach sending.
This task is preparation only; no outreach is performed here.

## 2) Pre-send checklist

Before sending any message:

- verify target source_url
- verify message references only documented evidence
- verify no forbidden claims
- verify status is currently not contacted
- verify correct channel selected
- verify optional PR offer is respectful
- verify no secrets or private info
- verify message is not spammy

## 3) Approved evidence

Allowed evidence:

- `@beezshield/sentinel`
- `npm install @beezshield/sentinel`
- `/contracts/risk-score`
- x402-gated API
- ERC-8004 identity
- AgentKit-style example available
- official provider coming next
- Guardian Doctrine public
- local fixture evaluation: 8 fixtures / 8 passed / 0 review
- regression evidence only, not a security guarantee

## 4) Forbidden claims

Must not say:

- guaranteed protection
- detects honeypots
- prevents MEV
- live simulation
- full contract coverage
- AgentKit provider live
- official AgentKit integration live
- you are vulnerable
- exploited

## 5) Send protocol

- human founder sends manually
- one target at a time
- no bulk spam
- record timestamp only after send
- preserve source URL
- preserve exact sent message if possible
- status can change from not contacted to contacted only after actual send

## 6) Tracker update protocol

After real send only, update `OUTREACH_TRACKER.md`:

- status: contacted
- date
- channel
- message link or short note
- next_follow_up_date
- response_status: pending

Never use integrated unless PR merged or public proof exists.

## 7) Follow-up protocol

- wait reasonable time
- one polite follow-up max
- no pressure language
- no fear-selling
