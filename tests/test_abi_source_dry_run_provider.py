import hashlib
from pathlib import Path

from services.scanner_engine.abi_source_adapter import analyze_abi_source_status
from services.scanner_engine.abi_source_dry_run_provider import (
    build_provider_lookup_plan,
    dry_run_abi_source_lookup,
)
from services.scanner_engine.abi_source_provider_config import get_abi_source_provider_config

REPO_ROOT = Path(__file__).resolve().parents[1]
DRY_RUN_MOD = REPO_ROOT / "services/scanner_engine/abi_source_dry_run_provider.py"
TRIAL_PLAN = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_PLAN.md"
ACTIVATION_PLAN = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_dry_run_module_has_no_http_client_imports():
    text = DRY_RUN_MOD.read_text(encoding="utf-8")
    lower = text.lower()
    forbidden_imports = [
        "import requests",
        "import httpx",
        "from requests",
        "from httpx",
        "urllib.request",
        "import urllib",
    ]
    for frag in forbidden_imports:
        assert frag not in lower, frag


def test_sourcify_lookup_plan_shapes():
    cfg = {}
    addr_h = "a" * 64
    plan = build_provider_lookup_plan("sourcify", "base", contract_address_hash=addr_h, config=cfg)
    assert plan["plan_version"] == "v1"
    assert plan["provider_name"] == "sourcify"
    assert plan["dry_run_only"] is True
    assert plan["network_call_planned"] is False
    assert plan["api_key_required_now"] is False
    assert plan["supported_chain"] is True
    assert plan["lookup_status"] == "dry_run_not_executed"
    assert "8453" in plan["endpoint_template"] or any("8453" in str(n) for n in plan.get("notes", []))
    assert "repo.sourcify.dev" in plan["endpoint_template"]


def test_blockscout_lookup_plan_shapes():
    plan = build_provider_lookup_plan("blockscout", "base", config={})
    assert plan["dry_run_only"] is True
    assert plan["network_call_planned"] is False
    assert plan["api_key_required_now"] is False
    assert plan["supported_chain"] is True
    assert plan["lookup_status"] == "dry_run_not_executed"
    assert "blockscout_base_url" in plan["endpoint_template"] or "/api/v2/smart-contracts/{address}" in plan[
        "endpoint_template"
    ]


def test_dry_run_lookup_paths():
    sour = dry_run_abi_source_lookup("sourcify", "base", contract_address_hash="abcd" * 16, config={"timeout_ms": 4000})
    assert sour["lookup_status"] == "dry_run_not_executed"
    assert sour["external_integration_status"] == "not_integrated"
    assert sour["raw_response_stored"] is False
    assert sour["secret_material_observed"] is False
    assert sour["dry_run_only"] is True
    assert sour["timeout_ms"] == 4000

    bad_pv = dry_run_abi_source_lookup("basescan", "base", contract_address_hash=None, config=None)
    assert bad_pv["lookup_status"] == "unsupported_provider"

    bad_ch = dry_run_abi_source_lookup("sourcify", "polygon", contract_address_hash=None, config=None)
    assert bad_ch["lookup_status"] == "unsupported_chain"


def test_adapter_defaults_remain_disabled_skeleton():
    out = analyze_abi_source_status("0x1111111111111111111111111111111111111111", chain="base", config=None)
    assert out["fallback_mode"] is True
    assert out["source_provider_status"] in {"disabled", "not_configured"}

    cfg = get_abi_source_provider_config()
    assert cfg.get("dry_run_only") is False


def test_adapter_dry_run_sourcify_branch():
    cfg = {
        "SENTINEL_ABI_SOURCE_PROVIDER_ENABLED": True,
        "SENTINEL_ABI_SOURCE_PROVIDER_NAME": "sourcify",
        "SENTINEL_ABI_SOURCE_DRY_RUN_ONLY": True,
    }
    out = analyze_abi_source_status(
        "0x1111111111111111111111111111111111111111",
        chain="base",
        config=cfg,
    )
    assert out["source_provider_status"] == "adapter_ready"
    dry = out.get("dry_run_lookup") or {}
    assert dry.get("lookup_status") == "dry_run_not_executed"
    note_blob = "\n".join(out.get("notes") or []).lower()
    assert "not called" in note_blob


def test_docs_and_claims_dry_run_gates():
    plan = TRIAL_PLAN.read_text(encoding="utf-8").lower()
    act = ACTIVATION_PLAN.read_text(encoding="utf-8").lower()
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    gate_docs = "\n".join([plan, act]).lower()

    assert "not called" in plan
    assert "dry-run" in plan or "dry run" in plan
    assert "not trial evidence" in plan or "trial evidence" in plan
    assert "not called" in act
    assert "sourcify/blockscout dry-run skeleton" in ledger
    assert "no live calls" in ledger or "no live" in ledger

    forbidden = [
        "trial completed",
        "live abi coverage is available",
        "full verified-source coverage is available",
        "guaranteed source verification is provided",
        "claims it detects honeypots",
        "guaranteed protection is provided",
        "claims it prevents mev",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in gate_docs, token


def test_env_unchanged_during_dry_run_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DRY_RUN_MOD.read_text(encoding="utf-8")
    analyze_abi_source_status("0x2222222222222222222222222222222222222222", chain="base")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
