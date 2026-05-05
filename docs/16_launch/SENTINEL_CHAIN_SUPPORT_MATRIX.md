# Sentinel chain support matrix (v5.7)

This matrix defines current chain-support truth for Sentinel Alpha.
It is intentionally conservative and cost-disciplined.

## Current support summary

| Chain | Support status | Network family | Risk engine support | Chain-read default | Paid RPC required | Notes |
|---|---|---|---|---|---|---|
| Base | primary | evm | full_v5_primary | config-gated (`enabled` only when explicitly configured) | false | Base is primary runtime target. |
| Ethereum | partial | evm | partial_signals | not_configured by default | false | Partial/roadmap-facing; no full primary claim. |
| Zora | roadmap | evm | docs_only / partial candidate context | not_configured by default | false | No full Zora support claim. |
| Unknown chain | unsupported / unknown | unknown | unsupported | not_configured | false | Fallback-safe behavior applies. |

## Cost discipline

- Paid RPC/provider dependencies are not enabled by default.
- Base-first approach keeps pre-revenue infrastructure lean.
- Multi-chain expansion requires explicit reliability and budget gates.

## Safety wording

- Base is the primary supported chain for current production flow.
- Ethereum and Zora are not claimed as full support today.
- No full multi-chain support claim.
- No full Zora support claim.
