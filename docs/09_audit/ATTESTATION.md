# 🧾 Attestation Layer

## Purpose

Proof that decision was made by Sentinel Alpha

---

## Structure

hash = SHA256(
  contract_address +
  risk_score +
  action +
  timestamp
)

---

## Output

{
  attestation_hash: string
}

---

## Usage

- proof for bots
- proof for investors
