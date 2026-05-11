# ABI/source provider trial attempt — v10.8A

A controlled read-only Sourcify trial attempt was made against five approved Base targets.

- trial_attempted: true
- trial_completed_successfully: false
- live_calls_attempted: true
- usable_provider_metadata_received: false
- runtime_provider_enabled: false
- provider_active: false
- api_keys_required: false
- paid_calls_allowed: false
- raw_responses_stored: false
- secret_material_observed: false
- abort_reason: network_error_all_rows
- connectivity_status: unconfirmed_from_local_environment
- env_hash_before equals env_hash_after: 77b2b7f7f3b14a9c42877bbcb1b731b4c631407c2fe443fb87c0661fa5ab542d

All 5 lookups failed with network_error. No usable Sourcify metadata was received. A direct connectivity check after the attempt was inconclusive and was interrupted. The production runtime provider remains disabled. No raw provider responses were stored.

This artifact is attempted-trial evidence only. It is not evidence of ABI coverage or source verification. A future rerun requires a confirmed network path, such as a VPS, and must follow the operational runbook.

## Lookup status counts

- error: 5

## Result rows

| trial_id | category | lookup_status | source_fetch_error_type | verified_source_status | abi_available | latency_ms |
| --- | --- | --- | --- | --- | --- | ---: |
| T01 | ERC20-like | error | network_error | unknown | unknown | 129 |
| T02 | NFT-like | error | network_error | unknown | unknown | 23 |
| T03 | proxy-like | error | network_error | unknown | unknown | 21 |
| T04 | router/pool-like | error | network_error | unknown | unknown | 24 |
| T05 | generic/utility | error | network_error | unknown | unknown | 21 |

Machine-readable twin: `reports/provider_trials/abi_source_trial_results.v10.8.attempted.json`.
