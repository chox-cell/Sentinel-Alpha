"""VPS Sourcify endpoint validation — one target (T01), one GET, sanitized output only.

Requires founder phrase (exact match) via --founder-phrase. Does not read `.env` for
configuration; only hashes `.env` for integrity fields. Does not enable runtime provider.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from services.scanner_engine.abi_source_dry_run_provider import hash_contract_address_for_plan
from services.scanner_engine.abi_source_provider_config import get_abi_source_provider_config

DATASET_PATH = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_DATASET.md"
JSON_OUT = REPO_ROOT / "reports/provider_trials/sourcify_endpoint_validation.v11.4.json"
MD_OUT = REPO_ROOT / "reports/provider_trials/sourcify_endpoint_validation.v11.4.md"
ENV_PATH = REPO_ROOT / ".env"

REQUIRED_PHRASE = "green light VPS Sourcify endpoint validation only"
ENDPOINT_LABEL = "sourcify_full_match_metadata"
CHAIN = "base"
CHAIN_ID = 8453
TIMEOUT_SEC = 5.0
TRIAL_ID = "T01"


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _strip_ticks(value: str) -> str:
    return value.strip().strip("`").strip()


def _parse_t01_target() -> dict[str, str]:
    text = DATASET_PATH.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("| T01 |"):
            continue
        headers = [
            "trial_id",
            "chain",
            "chain_id",
            "category",
            "contract_address",
            "source_url",
            "source_label",
            "source_status_before_trial",
            "expected_lookup_goal",
            "risk_notes",
            "trial_status",
        ]
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        return dict(zip(headers, cells, strict=True))
    raise RuntimeError("T01 row not found in dataset")


def _allowed_dirty_path(path: str) -> bool:
    prefixes = (
        "scripts/run_vps_sourcify_endpoint_validation.py",
        "reports/provider_trials/sourcify_endpoint_validation.v11.4.",
        "tests/test_sourcify_endpoint_validation_result.py",
        "docs/16_launch/SOURCIFY_ENDPOINT_CORRECTION_PLAN.md",
        "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md",
        "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md",
        "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md",
        "docs/00_project/SENTINEL_ALPHA_ROADMAP_TRACKER.md",
        "docs/18_investor/CLAIMS_LEDGER.md",
    )
    return any(path == p or path.startswith(p) for p in prefixes)


def _assert_preconditions() -> None:
    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    unexpected: list[str] = []
    for line in status.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        if not _allowed_dirty_path(path):
            unexpected.append(path)
    if unexpected:
        raise RuntimeError(
            "git working tree must be clean except allowed v11.4 files: "
            + ", ".join(sorted(unexpected))
        )

    cfg = get_abi_source_provider_config()
    if cfg.get("provider_enabled"):
        raise RuntimeError("runtime provider must remain disabled")
    if cfg.get("network_calls_enabled"):
        raise RuntimeError("runtime network_calls_enabled must remain false")


def _extract_abi(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    output = metadata.get("output")
    if not isinstance(output, dict):
        return []
    abi = output.get("abi")
    if not isinstance(abi, list):
        return []
    return [item for item in abi if isinstance(item, dict)]


def _abi_function_names(abi: list[dict[str, Any]], limit: int = 10) -> list[str]:
    names: list[str] = []
    for item in abi:
        if str(item.get("type") or "").lower() != "function":
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        names.append(name)
        if len(names) >= limit:
            break
    return names


def _classify_url_error(exc: BaseException) -> str:
    reason = str(getattr(exc, "reason", exc)).lower()
    if isinstance(exc, TimeoutError) or "timed out" in reason:
        return "timeout"
    if "certificate" in reason or "ssl" in reason or isinstance(exc, ssl.SSLError):
        return "tls_error"
    if "name or service not known" in reason or "nodename nor servname" in reason:
        return "dns_error"
    return "network_error"


def _run_validation(address: str) -> dict[str, Any]:
    url = (
        "https://repo.sourcify.dev/contracts/full_match/"
        f"{CHAIN_ID}/{address.lower()}/metadata.json"
    )
    endpoint_hash = _sha256_text(url)
    contract_hash = hash_contract_address_for_plan(address)
    started = time.perf_counter()

    reachable = False
    http_status: int | None = None
    error_type: str | None = None
    metadata_json_parse_success = False
    has_output_abi = False
    abi_function_count = 0
    abi_function_names_sample: list[str] = []
    verified_source_status = "unknown"
    abi_available: str | bool = "unknown"
    usable_metadata_received = False

    request = urllib.request.Request(url, method="GET")
    body: bytes | None = None
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SEC) as response:
            http_status = int(getattr(response, "status", response.getcode()))
            reachable = True
            body = response.read()
    except urllib.error.HTTPError as exc:
        http_status = int(exc.code)
        reachable = True
        body = exc.read()
    except Exception as exc:
        error_type = _classify_url_error(exc)
        http_status = None

    latency_ms = int((time.perf_counter() - started) * 1000)

    if body is not None and http_status == 200:
        try:
            metadata = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            metadata_json_parse_success = False
            error_type = error_type or "invalid_response"
        else:
            metadata_json_parse_success = isinstance(metadata, dict)
            if metadata_json_parse_success:
                abi = _extract_abi(metadata)
                has_output_abi = bool(abi)
                if has_output_abi:
                    abi_available = True
                    abi_function_count = sum(
                        1 for item in abi if str(item.get("type") or "").lower() == "function"
                    )
                    abi_function_names_sample = _abi_function_names(abi)
                    verified_source_status = "verified"
                    usable_metadata_received = True
                else:
                    abi_available = False
                    usable_metadata_received = False
    elif http_status is not None and http_status != 200:
        error_type = error_type or "http_error"

    fallback_mode = not usable_metadata_received
    confidence_impact = (
        "low_confidence_due_to_unavailable_source"
        if fallback_mode
        else "neutral_source_metadata_only"
    )

    return {
        "endpoint_hash": endpoint_hash,
        "contract_address_hash": contract_hash,
        "reachable": reachable,
        "http_status": http_status,
        "error_type": error_type,
        "latency_ms": latency_ms,
        "metadata_json_parse_success": metadata_json_parse_success,
        "usable_metadata_received": usable_metadata_received,
        "verified_source_status": verified_source_status,
        "abi_available": abi_available,
        "abi_function_count": abi_function_count,
        "abi_function_names_sample": abi_function_names_sample,
        "fallback_mode": fallback_mode,
        "confidence_impact": confidence_impact,
    }


def _build_report(env_before: str, env_after: str, fields: dict[str, Any]) -> dict[str, Any]:
    return {
        "report_type": "sourcify_endpoint_validation",
        "version": "v11.4",
        "endpoint_validation_run": True,
        "trial_rerun": False,
        "provider_active": False,
        "runtime_provider_enabled": False,
        "dataset_wide_lookup": False,
        "requests_attempted": 1,
        "target_count": 1,
        "provider_name": "sourcify",
        "chain": CHAIN,
        "chain_id": CHAIN_ID,
        "endpoint_label": ENDPOINT_LABEL,
        "endpoint_hash": fields["endpoint_hash"],
        "contract_address_hash": fields["contract_address_hash"],
        "trial_id": TRIAL_ID,
        "api_keys_required": False,
        "paid_calls_allowed": False,
        "raw_response_stored": False,
        "raw_body_stored": False,
        "secret_material_observed": False,
        "notSecurityGuarantee": True,
        "reachable": fields["reachable"],
        "http_status": fields["http_status"],
        "error_type": fields["error_type"],
        "latency_ms": fields["latency_ms"],
        "metadata_json_parse_success": fields["metadata_json_parse_success"],
        "usable_metadata_received": fields["usable_metadata_received"],
        "verified_source_status": fields["verified_source_status"],
        "abi_available": fields["abi_available"],
        "abi_function_count": fields["abi_function_count"],
        "abi_function_names_sample": fields["abi_function_names_sample"],
        "fallback_mode": fields["fallback_mode"],
        "confidence_impact": fields["confidence_impact"],
        "checked_at": _iso_now(),
        "env_hash_before": env_before,
        "env_hash_after": env_after,
        "notes": (
            "Endpoint validation only for T01 via Sourcify full_match; one GET; "
            "no trial rerun; no dataset-wide lookup; no raw body stored. "
            "Canonical evidence should be produced on the approved VPS host per runbook."
        ),
    }


def _to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Sourcify endpoint validation — v11.4",
        "",
        "Endpoint validation only. No trial rerun. Exactly one Sourcify full_match metadata GET was performed for trial target T01 only. No dataset-wide lookup occurred.",
        "",
        "- provider remains disabled",
        "- no raw response body stored",
        "- one-target validation is not ABI coverage evidence",
        "",
        f"- reachable: {report['reachable']}",
        f"- http_status: {report['http_status']}",
        f"- error_type: {report['error_type']}",
        f"- usable_metadata_received: {report['usable_metadata_received']}",
        f"- verified_source_status: {report['verified_source_status']}",
        "",
        "Trial rerun still blocked until separate approval phrase: \"green light rerun Sourcify trial from VPS\" plus runbook gates.",
        "",
        "Operator note: regenerate this artifact on the approved VPS host if TLS or network errors reflect the automation environment rather than VPS reachability.",
        "",
        "Machine-readable twin: `reports/provider_trials/sourcify_endpoint_validation.v11.4.json`.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="VPS Sourcify endpoint validation (one target).")
    parser.add_argument(
        "--founder-phrase",
        required=True,
        help='Must be exactly: green light VPS Sourcify endpoint validation only',
    )
    args = parser.parse_args()
    if args.founder_phrase != REQUIRED_PHRASE:
        raise SystemExit("founder phrase mismatch; refusing to run endpoint validation")

    _assert_preconditions()

    env_before = _sha256_file(ENV_PATH) if ENV_PATH.exists() else "missing"
    target = _parse_t01_target()
    address = _strip_ticks(target["contract_address"])
    if target["trial_id"] != TRIAL_ID:
        raise RuntimeError("expected T01 target")

    fields = _run_validation(address)
    env_after = _sha256_file(ENV_PATH) if ENV_PATH.exists() else "missing"
    if env_before != env_after:
        raise RuntimeError(".env hash changed during validation")

    report = _build_report(env_before, env_after, fields)
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    MD_OUT.write_text(_to_markdown(report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
