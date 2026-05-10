"""Dry-run ABI/source provider skeleton for Sourcify and Blockscout (no HTTP)."""

from __future__ import annotations

import hashlib
from typing import Any

SOURCIFY_ENDPOINT_TEMPLATE = (
    "https://repo.sourcify.dev/contracts/full_match/{chain_id}/{address}/metadata.json"
)

BLOCKSCOUT_ENDPOINT_TEMPLATE = "{blockscout_base_url}/api/v2/smart-contracts/{address}"

DRY_RUN_PROVIDERS = frozenset({"sourcify", "blockscout"})

CHAIN_ID_BY_CHAIN = {
    "base": 8453,
}


def hash_contract_address_for_plan(normalized_eth_address: str | None) -> str | None:
    """SHA-256 of lowercase normalized address hex; returns None when empty."""
    if not normalized_eth_address or not isinstance(normalized_eth_address, str):
        return None
    addr = normalized_eth_address.strip().lower()
    if not addr.startswith("0x") or len(addr) != 42:
        return None
    return hashlib.sha256(addr.encode("utf-8")).hexdigest()


def build_provider_lookup_plan(
    provider_name: str | None,
    chain: str | None,
    contract_address_hash: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = config if isinstance(config, dict) else {}
    pname = str(provider_name or "").strip().lower()
    chain_key = str(chain or "base").strip().lower()

    chain_id = CHAIN_ID_BY_CHAIN.get(chain_key)
    supported_chain = chain_id is not None

    if pname not in DRY_RUN_PROVIDERS:
        return {
            "plan_version": "v1",
            "provider_name": pname or "",
            "chain": chain_key,
            "contract_address_hash": contract_address_hash,
            "provider_category": "abi_source",
            "dry_run_only": True,
            "network_call_planned": False,
            "api_key_required_now": False,
            "endpoint_template": "",
            "chain_id": None,
            "supported_chain": False,
            "lookup_status": "unsupported_provider",
            "notes": [
                "Dry-run skeleton supports only sourcify and blockscout provider_name values.",
                "No network call is performed.",
            ],
        }

    if not supported_chain:
        return {
            "plan_version": "v1",
            "provider_name": pname,
            "chain": chain_key,
            "contract_address_hash": contract_address_hash,
            "provider_category": "abi_source",
            "dry_run_only": True,
            "network_call_planned": False,
            "api_key_required_now": False,
            "endpoint_template": "",
            "chain_id": None,
            "supported_chain": False,
            "lookup_status": "unsupported_chain",
            "notes": [
                f"Dry-run chain '{chain_key}' is not mapped for this skeleton (Base id 8453 only).",
                "No network call is performed.",
            ],
        }

    if pname == "sourcify":
        endpoint_template = SOURCIFY_ENDPOINT_TEMPLATE
        notes = [
            "Sourcify URL template is documentation only; it is not requested in dry-run mode.",
            "Base chain_id 8453 is used for template context only.",
            "Dry run does not prove provider availability or ABI coverage.",
        ]
    else:
        base = str(
            cfg.get("blockscout_base_url")
            or cfg.get("BLOCKSCOUT_BASE_URL")
            or ""
        ).strip().rstrip("/")
        if not base:
            endpoint_template = BLOCKSCOUT_ENDPOINT_TEMPLATE
        else:
            endpoint_template = f"{base}/api/v2/smart-contracts/{{address}}"
        notes = [
            "Blockscout URL template is documentation only; it is not requested in dry-run mode.",
            "Configure BLOCKSCOUT_BASE_URL before a future live trial if required.",
            "Dry run does not prove provider availability or ABI coverage.",
        ]

    return {
        "plan_version": "v1",
        "provider_name": pname,
        "chain": chain_key,
        "contract_address_hash": contract_address_hash,
        "provider_category": "abi_source",
        "dry_run_only": True,
        "network_call_planned": False,
        "api_key_required_now": False,
        "endpoint_template": endpoint_template,
        "chain_id": chain_id,
        "supported_chain": True,
        "lookup_status": "dry_run_not_executed",
        "notes": notes,
    }


def dry_run_abi_source_lookup(
    provider_name: str | None,
    chain: str | None,
    contract_address_hash: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = config if isinstance(config, dict) else {}
    try:
        timeout_ms = int(cfg.get("timeout_ms", 3000))
    except (TypeError, ValueError):
        timeout_ms = 3000
    timeout_ms = max(500, timeout_ms)

    plan = build_provider_lookup_plan(
        provider_name, chain, contract_address_hash=contract_address_hash, config=cfg
    )
    plan_status = str(plan.get("lookup_status") or "")

    if plan_status == "unsupported_provider":
        return {
            "result_version": "v1",
            "provider_name": str(provider_name or "").strip().lower(),
            "chain": str(chain or "").strip().lower(),
            "contract_address_hash": contract_address_hash,
            "lookup_status": "unsupported_provider",
            "verified_source_status": "unknown",
            "abi_available": "unknown",
            "abi_function_count": 0,
            "abi_function_names_sample": [],
            "source_fetch_error_type": "unsupported_provider",
            "latency_ms": None,
            "timeout_ms": timeout_ms,
            "fallback_mode": True,
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "response_sanitized": True,
            "raw_response_stored": False,
            "secret_material_observed": False,
            "dry_run_only": True,
            "external_integration_status": "not_integrated",
            "dry_run_plan": plan,
            "notes": [
                "Dry-run lookup only; unsupported provider for this skeleton.",
                "No network call is performed.",
            ],
        }

    if plan_status == "unsupported_chain":
        return {
            "result_version": "v1",
            "provider_name": str(plan.get("provider_name") or ""),
            "chain": str(plan.get("chain") or ""),
            "contract_address_hash": contract_address_hash,
            "lookup_status": "unsupported_chain",
            "verified_source_status": "unknown",
            "abi_available": "unknown",
            "abi_function_count": 0,
            "abi_function_names_sample": [],
            "source_fetch_error_type": "unsupported_chain",
            "latency_ms": None,
            "timeout_ms": timeout_ms,
            "fallback_mode": True,
            "confidence_impact": "low_confidence_due_to_unavailable_source",
            "response_sanitized": True,
            "raw_response_stored": False,
            "secret_material_observed": False,
            "dry_run_only": True,
            "external_integration_status": "not_integrated",
            "dry_run_plan": plan,
            "notes": [
                "Dry-run lookup only; unsupported chain for this skeleton.",
                "No network call is performed.",
            ],
        }

    return {
        "result_version": "v1",
        "provider_name": str(plan.get("provider_name") or ""),
        "chain": str(plan.get("chain") or ""),
        "contract_address_hash": contract_address_hash,
        "lookup_status": "dry_run_not_executed",
        "verified_source_status": "unknown",
        "abi_available": "unknown",
        "abi_function_count": 0,
        "abi_function_names_sample": [],
        "source_fetch_error_type": None,
        "latency_ms": None,
        "timeout_ms": timeout_ms,
        "fallback_mode": True,
        "confidence_impact": "low_confidence_due_to_unavailable_source",
        "response_sanitized": True,
        "raw_response_stored": False,
        "secret_material_observed": False,
        "dry_run_only": True,
        "external_integration_status": "not_integrated",
        "dry_run_plan": plan,
        "notes": [
            "Dry-run only; lookup was not executed and no endpoint was called.",
            "This row is not trial evidence.",
        ],
    }


def should_use_dry_run_skeleton(provider_config: dict[str, Any] | None) -> bool:
    cfg = provider_config if isinstance(provider_config, dict) else {}
    pname = str(cfg.get("provider_name") or "").strip().lower()
    if pname not in DRY_RUN_PROVIDERS:
        return False
    if not cfg.get("provider_enabled"):
        return False
    if cfg.get("network_calls_enabled"):
        return False
    if str(cfg.get("provider_mode") or "") != "adapter_ready":
        return False
    return bool(cfg.get("dry_run_only"))
