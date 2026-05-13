# Sourcify endpoint validation — v11.4

Endpoint validation only. No trial rerun. Exactly one Sourcify full_match metadata GET was performed for trial target T01 only. No dataset-wide lookup occurred.

- provider remains disabled
- no raw response body stored
- one-target validation is not ABI coverage evidence

- reachable: False
- http_status: None
- error_type: tls_error
- usable_metadata_received: False
- verified_source_status: unknown

Trial rerun still blocked until separate approval phrase: "green light rerun Sourcify trial from VPS" plus runbook gates.

Operator note: regenerate this artifact on the approved VPS host if TLS or network errors reflect the automation environment rather than VPS reachability.

Machine-readable twin: `reports/provider_trials/sourcify_endpoint_validation.v11.4.json`.
