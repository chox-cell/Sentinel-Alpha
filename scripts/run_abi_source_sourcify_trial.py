"""Controlled read-only Sourcify trial runner for approved Base targets.

Writes sanitized attempted evidence to v10.8A report paths. Rerun only from a
confirmed network path and under the operational runbook.
"""

from __future__ import annotations

import hashlib
import json
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

from services.scanner_engine.abi_source_dry_run_provider import (
    CHAIN_ID_BY_CHAIN,
    SOURCIFY_ENDPOINT_TEMPLATE,
    hash_contract_address_for_plan,
)
from services.scanner_engine.abi_source_provider_config import get_abi_source_provider_config

DATASET_PATH = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_DATASET.md"
JSON_OUT = REPO_ROOT / "reports/provider_trials/abi_source_trial_results.v10.8.attempted.json"
MD_OUT = REPO_ROOT / "reports/provider_trials/abi_source_trial_results.v10.8.attempted.md"
ENV_PATH = REPO_ROOT / ".env"
CHAIN = "base"
CHAIN_ID = CHAIN_ID_BY_CHAIN[CHAIN]
MAX_TARGETS = 5
MAX_REQUESTS = 5
TIMEOUT_SEC = 3.0
TIMEOUT_MS = 3000
PLACEHOLDER_ADDRESSES = {
    "0x1111111111111111111111111111111111111111",
    "0x2222222222222222222222222222222222222222",
    "0x3333333333333333333333333333333333333333",
    "0x4444444444444444444444444444444444444444",
    "0x5555555555555555555555555555555555555555",
}


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _strip_ticks(value: str) -> str:
    return value.strip().strip("`").strip()


def _parse_dataset_targets() -> list[dict[str, str]]:
    text = DATASET_PATH.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip().startswith("| T0")]
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
    rows: list[dict[str, str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        rows.append(dict(zip(headers, cells, strict=True)))
    return rows


def _allowed_dirty_path(path: str) -> bool:
    allowed_prefixes = (
        "scripts/run_abi_source_sourcify_trial.py",
        "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_",
        "docs/00_project/SENTINEL_ALPHA_ROADMAP_TRACKER.md",
        "docs/18_investor/CLAIMS_LEDGER.md",
        "tests/test_abi_source_sourcify_trial_attempted_network_error.py",
        "reports/provider_trials/abi_source_trial_results.v10.8.attempted.",
    )
    return any(path == prefix or path.startswith(prefix) for prefix in allowed_prefixes)


def _assert_preconditions(env_hash_before: str) -> None:
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
            "git working tree must be clean except allowed v10.8 trial files: "
            + ", ".join(sorted(unexpected))
        )

    cfg = get_abi_source_provider_config()
    if cfg.get("provider_enabled"):
        raise RuntimeError("runtime provider must remain disabled by default")
    if cfg.get("network_calls_enabled"):
        raise RuntimeError("runtime network_calls_enabled must remain false")

    rows = _parse_dataset_targets()
    if len(rows) != MAX_TARGETS:
        raise RuntimeError(f"dataset must contain exactly {MAX_TARGETS} targets")
    for row in rows:
        address = _strip_ticks(row["contract_address"]).lower()
        source_url = _strip_ticks(row["source_url"])
        if address in PLACEHOLDER_ADDRESSES:
            raise RuntimeError(f"placeholder target not allowed: {row['trial_id']}")
        if not source_url.startswith("https://"):
            raise RuntimeError(f"missing source_url for {row['trial_id']}")
        if row["chain_id"] != str(CHAIN_ID):
            raise RuntimeError(f"unexpected chain_id for {row['trial_id']}")

    if not env_hash_before:
        raise RuntimeError("env_hash_before is required")


def _build_endpoint(address: str) -> str:
    return SOURCIFY_ENDPOINT_TEMPLATE.format(chain_id=CHAIN_ID, address=address.lower())


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
        item_type = str(item.get("type") or "").lower()
        if item_type != "function":
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        names.append(name)
        if len(names) >= limit:
            break
    return names


def _lookup_target(target: dict[str, str]) -> dict[str, Any]:
    address = _strip_ticks(target["contract_address"])
    endpoint = _build_endpoint(address)
    endpoint_hash = _sha256_text(endpoint)
    address_hash = hash_contract_address_for_plan(address)
    started = time.perf_counter()
    lookup_status = "error"
    verified_source_status = "unknown"
    abi_available: str | bool = "unknown"
    abi_function_count = 0
    abi_function_names_sample: list[str] = []
    source_fetch_error_type: str | None = None
    notes = "Read-only Sourcify request attempted; network error; no usable metadata received."

    request = urllib.request.Request(endpoint, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SEC) as response:
            status_code = int(getattr(response, "status", response.getcode()))
            body = response.read()
    except urllib.error.HTTPError as exc:
        status_code = int(exc.code)
        body = exc.read()
    except TimeoutError:
        latency_ms = int((time.perf_counter() - started) * 1000)
        return {
            "result_version": "v1",
            "trial_id": target["trial_id"],
            "chain": CHAIN,
            "contract_address_hash": address_hash,
            "category": target["category"],
            "provider_name": "sourcify",
            "provider_endpoint_hash": endpoint_hash,
            "lookup_status": "timeout",
            "verified_source_status": "unknown",
            "abi_available": "unknown",
            "abi_function_count": 0,
            "abi_function_names_sample": [],
            "source_fetch_error_type": "timeout",
            "latency_ms": latency_ms,
            "timeout_ms": TIMEOUT_MS,
            "fallback_mode": True,
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "response_sanitized": True,
            "raw_response_stored": False,
            "secret_material_observed": False,
            "created_at": _iso_now(),
            "notes": notes,
            "http_status_code": None,
        }
    except urllib.error.URLError as exc:
        latency_ms = int((time.perf_counter() - started) * 1000)
        reason = str(getattr(exc, "reason", exc))
        if "timed out" in reason.lower():
            lookup_status = "timeout"
            source_fetch_error_type = "timeout"
        else:
            lookup_status = "error"
            source_fetch_error_type = "network_error"
        return {
            "result_version": "v1",
            "trial_id": target["trial_id"],
            "chain": CHAIN,
            "contract_address_hash": address_hash,
            "category": target["category"],
            "provider_name": "sourcify",
            "provider_endpoint_hash": endpoint_hash,
            "lookup_status": lookup_status,
            "verified_source_status": "unknown",
            "abi_available": "unknown",
            "abi_function_count": 0,
            "abi_function_names_sample": [],
            "source_fetch_error_type": source_fetch_error_type,
            "latency_ms": latency_ms,
            "timeout_ms": TIMEOUT_MS,
            "fallback_mode": True,
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "response_sanitized": True,
            "raw_response_stored": False,
            "secret_material_observed": False,
            "created_at": _iso_now(),
            "notes": notes,
            "http_status_code": None,
        }
    except Exception:
        latency_ms = int((time.perf_counter() - started) * 1000)
        return {
            "result_version": "v1",
            "trial_id": target["trial_id"],
            "chain": CHAIN,
            "contract_address_hash": address_hash,
            "category": target["category"],
            "provider_name": "sourcify",
            "provider_endpoint_hash": endpoint_hash,
            "lookup_status": "error",
            "verified_source_status": "unknown",
            "abi_available": "unknown",
            "abi_function_count": 0,
            "abi_function_names_sample": [],
            "source_fetch_error_type": "unexpected_exception",
            "latency_ms": latency_ms,
            "timeout_ms": TIMEOUT_MS,
            "fallback_mode": True,
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "response_sanitized": True,
            "raw_response_stored": False,
            "secret_material_observed": False,
            "created_at": _iso_now(),
            "notes": notes,
            "http_status_code": None,
        }

    latency_ms = int((time.perf_counter() - started) * 1000)
    if status_code >= 500:
        lookup_status = "provider_down"
        source_fetch_error_type = "provider_down"
    elif status_code != 200:
        lookup_status = "invalid_response"
        source_fetch_error_type = "http_error"
    else:
        try:
            metadata = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            lookup_status = "invalid_response"
            source_fetch_error_type = "invalid_json"
            metadata = None
        else:
            if not isinstance(metadata, dict):
                lookup_status = "invalid_response"
                source_fetch_error_type = "invalid_shape"
            else:
                lookup_status = "success"
                verified_source_status = "verified"
                abi = _extract_abi(metadata)
                if abi:
                    abi_available = True
                    abi_function_count = sum(
                        1 for item in abi if str(item.get("type") or "").lower() == "function"
                    )
                    abi_function_names_sample = _abi_function_names(abi)
                else:
                    abi_available = False

    return {
        "result_version": "v1",
        "trial_id": target["trial_id"],
        "chain": CHAIN,
        "contract_address_hash": address_hash,
        "category": target["category"],
        "provider_name": "sourcify",
        "provider_endpoint_hash": endpoint_hash,
        "lookup_status": lookup_status,
        "verified_source_status": verified_source_status,
        "abi_available": abi_available,
        "abi_function_count": abi_function_count,
        "abi_function_names_sample": abi_function_names_sample,
        "source_fetch_error_type": source_fetch_error_type,
        "latency_ms": latency_ms,
        "timeout_ms": TIMEOUT_MS,
        "fallback_mode": lookup_status != "success",
        "confidence_impact": (
            "low_confidence_due_to_unavailable_source"
            if lookup_status != "success"
            else "neutral_source_metadata_only"
        ),
        "response_sanitized": True,
        "raw_response_stored": False,
        "secret_material_observed": False,
        "created_at": _iso_now(),
        "notes": notes,
        "http_status_code": status_code,
    }


def _sanitize_result_row(row: dict[str, Any]) -> dict[str, Any]:
    sanitized = dict(row)
    sanitized.pop("http_status_code", None)
    return sanitized


def _build_report(env_hash_before: str, env_hash_after: str, results: list[dict[str, Any]]) -> dict[str, Any]:
    sanitized_results = [_sanitize_result_row(row) for row in results]
    all_network_error = bool(sanitized_results) and all(
        row.get("lookup_status") == "error"
        and row.get("source_fetch_error_type") == "network_error"
        for row in sanitized_results
    )
    return {
        "report_type": "abi_source_provider_trial_attempt",
        "version": "v10.8A",
        "trial_attempted": True,
        "trial_completed_successfully": not all_network_error,
        "provider_active": False,
        "runtime_provider_enabled": False,
        "live_calls_attempted": True,
        "usable_provider_metadata_received": not all_network_error,
        "provider_name": "sourcify",
        "chain": CHAIN,
        "chain_id": CHAIN_ID,
        "attempted_targets": len(sanitized_results),
        "attempted_requests": len(sanitized_results),
        "api_keys_required": False,
        "paid_calls_allowed": False,
        "raw_responses_stored": False,
        "secret_material_observed": False,
        "notSecurityGuarantee": True,
        "env_hash_before": env_hash_before,
        "env_hash_after": env_hash_after,
        "abort_reason": "network_error_all_rows" if all_network_error else None,
        "connectivity_status": (
            "unconfirmed_from_local_environment" if all_network_error else "confirmed_for_attempt"
        ),
        "created_at": _iso_now(),
        "results": sanitized_results,
    }


def _to_markdown(report: dict[str, Any]) -> str:
    counts: dict[str, int] = {}
    for row in report["results"]:
        status = str(row.get("lookup_status") or "unknown")
        counts[status] = counts.get(status, 0) + 1

    lines = [
        "# ABI/source provider trial attempt — v10.8A",
        "",
        "A controlled read-only Sourcify trial attempt was made against approved Base targets.",
        "",
        "- trial_attempted: true",
        "- trial_completed_successfully: false",
        "- live_calls_attempted: true",
        "- usable_provider_metadata_received: false",
        "- runtime_provider_enabled: false",
        "- provider_active: false",
        "- api_keys_required: false",
        "- paid_calls_allowed: false",
        "- raw_responses_stored: false",
        "- secret_material_observed: false",
        "",
        "All five lookups failed with network_error. No usable Sourcify metadata was received. This artifact is attempted-trial evidence only and is not evidence of ABI coverage or source verification.",
        "",
        "## Lookup status counts",
        "",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            "## Result rows",
            "",
            "| trial_id | category | lookup_status | verified_source_status | abi_available | abi_function_count | latency_ms |",
            "| --- | --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in report["results"]:
        lines.append(
            f"| {row['trial_id']} | {row['category']} | {row['lookup_status']} | "
            f"{row['verified_source_status']} | {row['abi_available']} | {row['abi_function_count']} | {row['latency_ms']} |"
        )
    lines.extend(
        [
            "",
            "Machine-readable twin: `reports/provider_trials/abi_source_trial_results.v10.8.attempted.json`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    env_hash_before = _sha256_file(ENV_PATH) if ENV_PATH.exists() else "missing"
    _assert_preconditions(env_hash_before)

    targets = _parse_dataset_targets()[:MAX_TARGETS]
    results = [_lookup_target(target) for target in targets]
    if len(results) > MAX_REQUESTS:
        raise RuntimeError("trial exceeded max request count")

    env_hash_after = _sha256_file(ENV_PATH) if ENV_PATH.exists() else "missing"
    if env_hash_before != env_hash_after:
        raise RuntimeError(".env hash changed during trial execution")

    report = _build_report(env_hash_before, env_hash_after, results)
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    MD_OUT.write_text(_to_markdown(report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
