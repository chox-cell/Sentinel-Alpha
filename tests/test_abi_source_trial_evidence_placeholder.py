import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = REPO_ROOT / "reports/provider_trials/abi_source_trial_results.sample.json"
MD_PATH = REPO_ROOT / "reports/provider_trials/abi_source_trial_results.sample.md"
SCHEMA_DOC = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RESULT_SCHEMA.md"
RUNBOOK = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_RUNBOOK.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_json_evidence_placeholder_parses_and_shape():
    assert JSON_PATH.exists()
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    assert data["report_type"] == "abi_source_provider_trial_results"
    assert data["version"] == "v10.5"
    assert data["sampleOnly"] is True
    assert data["documentationOnly"] is True
    assert data["trial_run"] is False
    assert data["provider_active"] is False
    assert data["live_calls_performed"] is False
    assert data["api_keys_required"] is False
    assert data["raw_responses_stored"] is False
    assert data["secret_material_observed"] is False
    assert data["notSecurityGuarantee"] is True
    assert isinstance(data.get("created_at"), str)

    ts = data["trial_summary"]
    assert ts["provider_name"] is None
    assert ts["provider_endpoint_hash"] is None
    assert ts["chain"] == "base"
    assert ts["max_targets"] == 5
    assert ts["max_requests"] == 5
    assert ts["paid_calls_allowed"] is False
    assert ts["approval_status"] == "not_approved"
    assert ts["approved_by"] is None
    assert ts["env_hash_before"] is None
    assert ts["env_hash_after"] is None
    assert ts["rollback_status"] == "not_needed_not_run"

    results = data["results"]
    assert len(results) == 5

    cats = []
    expected_ids = []
    for i in range(1, 6):
        expected_ids.append(f"T0{i}")

    seen = []
    for row in results:
        assert row["result_version"] == "v1"
        assert row["trial_id"] in expected_ids
        seen.append(row["trial_id"])
        assert row["chain"] == "base"
        assert len(row["contract_address_hash"]) == 64
        cats.append(row["category"])
        assert row["provider_name"] is None
        assert row["provider_endpoint_hash"] is None
        assert row["lookup_status"] == "not_run"
        assert row["verified_source_status"] == "unknown"
        assert row["abi_available"] == "unknown"
        assert row["abi_function_count"] == 0
        assert row["abi_function_names_sample"] == []
        assert row["source_fetch_error_type"] is None
        assert row["latency_ms"] is None
        assert row["timeout_ms"] == 3000
        assert row["fallback_mode"] is True
        assert row["confidence_impact"] == "low_confidence_due_to_unavailable_source"
        assert row["response_sanitized"] is True
        assert row["raw_response_stored"] is False
        assert row["secret_material_observed"] is False
        assert row["created_at"] is None
        assert row["notes"] == "Placeholder row; trial not run."

    assert sorted(seen) == sorted(expected_ids)
    assert cats == [
        "ERC20-like",
        "NFT-like",
        "proxy-like",
        "router/pool-like",
        "generic/utility",
    ]


def test_markdown_placeholder_exists_and_disclaimers():
    assert MD_PATH.exists()
    md = MD_PATH.read_text(encoding="utf-8").lower()

    assert "sample only" in md
    assert "trial not run" in md
    assert "no live calls" in md
    assert "no api keys required" in md
    assert "no raw responses stored" in md
    assert "not_run" in MD_PATH.read_text(encoding="utf-8").lower()


def test_schema_and_runbook_reference_sample_placeholder():
    schema = SCHEMA_DOC.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")

    assert "abi_source_trial_results.sample.json" in schema
    assert "placeholder" in schema.lower()
    assert "not trial evidence" in schema.lower()

    assert "abi_source_trial_results.sample.json" in runbook
    assert "sample" in runbook.lower()


def test_claims_ledger_evidence_placeholder_row():
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    assert "abi/source trial evidence placeholder" in ledger
    assert "sample prepared / trial not run" in ledger


def test_placeholder_files_forbid_overclaim_language():
    combined = (
        JSON_PATH.read_text(encoding="utf-8") + MD_PATH.read_text(encoding="utf-8")
    ).lower()
    forbidden = [
        "trial completed",
        "live abi coverage",
        "full verified-source coverage",
        "guaranteed source verification",
        "detects honeypots",
        "guaranteed protection",
        "prevents mev",
        "live simulation",
    ]
    for token in forbidden:
        assert token not in combined, token


def test_env_unchanged_during_placeholder_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = JSON_PATH.read_bytes()
    _ = MD_PATH.read_bytes()
    _ = SCHEMA_DOC.read_text(encoding="utf-8")
    _ = RUNBOOK.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
