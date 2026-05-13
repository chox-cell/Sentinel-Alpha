# Sourcify VPS connectivity preflight — v11.2

VPS preflight completed. This was exactly one Sourcify connectivity check only. This was not a trial rerun. This was not a dataset-wide lookup. This did not activate provider runtime.

- reachable: true
- HTTP status: 404
- error_type: http_error
- latency_ms: 210
- requests_attempted: 1

This result is connectivity evidence only: the VPS reached Sourcify and received an HTTP response. A 404 on the health path still proves HTTP reachability; it does not prove usable ABI/source metadata availability.

No usable ABI/source metadata was received. No raw body was stored. No dataset-wide lookup occurred. No trial rerun occurred. Provider remains disabled.

Trial rerun still requires the exact phrase: "green light rerun Sourcify trial from VPS".

Machine-readable twin: `reports/provider_trials/sourcify_vps_preflight.v11.2.json`.
