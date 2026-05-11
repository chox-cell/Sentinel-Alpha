import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = REPO_ROOT / "reports/provider_trials/abi_source_trial_results.v10.8.attempted.json"
REPORT_MD = REPO_ROOT / "reports/provider_trials/abi_source_trial_results.v10.8.attempted.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_attempted_json_exists_and_parses():
    assert REPORT_JSON.exists()
    data = json.loads(REPORT_JSON.read_text(encoding="utf-8"))

    assert data["report_type"] == "abi_source_provider_trial_attempt"
    assert data["version"] == "v10.8A"
    assert data["trial_attempted"] is True
    assert data["trial_completed_successfully"] is False
    assert data["provider_active"] is False
    assert data["runtime_provider_enabled"] is False
    assert data["live_calls_attempted"] is True
    assert data["usable_provider_metadata_received"] is False
    assert data["provider_name"] == "sourcify"
    assert data["attempted_targets"] == 5
    assert data["attempted_requests"] == 5
    assert data["api_keys_required"] is False
    assert data["paid_calls_allowed"] is False
    assert data["raw_responses_stored"] is False
    assert data["secret_material_observed"] is False
    assert data["notSecurityGuarantee"] is True
    assert data["env_hash_before"] == data["env_hash_after"]
    assert len(data["results"]) == 5


def test_attempted_rows_record_network_error_only():
    data = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    raw_text = REPORT_JSON.read_text(encoding="utf-8")

    for row in data["results"]:
        assert row["lookup_status"] == "error"
        assert row["source_fetch_error_type"] == "network_error"
        assert row["raw_response_stored"] is False
        assert row["secret_material_observed"] is False
        assert row["response_sanitized"] is True
        assert "contract_address" not in row

    assert '"abi":' not in raw_text
    assert '"sources":' not in raw_text


def test_attempted_markdown_and_docs_reflect_failed_attempt():
    md = REPORT_MD.read_text(encoding="utf-8").lower()
    approval = APPROVAL.read_text(encoding="utf-8").lower()
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()

    assert "all 5 lookups failed with network_error" in md
    assert "no usable sourcify metadata was received" in md
    assert "approval_status: attempted_network_failed_provider_disabled" in approval
    assert "controlled sourcify abi/source trial attempt" in ledger
    assert "attempted / network_error / no usable metadata / provider disabled" in ledger


def test_attempted_artifacts_forbid_unsafe_positive_phrases():
    combined = (
        REPORT_JSON.read_text(encoding="utf-8")
        + REPORT_MD.read_text(encoding="utf-8")
        + APPROVAL.read_text(encoding="utf-8")
        + CLAIMS_LEDGER.read_text(encoding="utf-8")
    ).lower()
    forbidden = [
        "trial completed successfully",
        "live abi coverage",
        "full verified-source coverage",
        "guaranteed source verification",
        "detects honeypots",
        "guaranteed protection",
        "prevents mev",
        "live simulation",
        "production provider active",
    ]
    for phrase in forbidden:
        assert phrase not in combined, phrase


def test_env_unchanged_during_attempted_trial_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = REPORT_JSON.read_bytes()
    _ = REPORT_MD.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = CLAIMS_LEDGER.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
