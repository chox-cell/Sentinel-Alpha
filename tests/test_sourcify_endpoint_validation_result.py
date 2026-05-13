import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = REPO_ROOT / "reports/provider_trials/sourcify_endpoint_validation.v11.4.json"
REPORT_MD = REPO_ROOT / "reports/provider_trials/sourcify_endpoint_validation.v11.4.md"
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_endpoint_validation_json_exists_and_matches_required_posture():
    assert REPORT_JSON.exists()
    data = json.loads(REPORT_JSON.read_text(encoding="utf-8"))

    assert data["report_type"] == "sourcify_endpoint_validation"
    assert data["version"] == "v11.4"
    assert data["endpoint_validation_run"] is True
    assert data["trial_rerun"] is False
    assert data["provider_active"] is False
    assert data["runtime_provider_enabled"] is False
    assert data["dataset_wide_lookup"] is False
    assert data["requests_attempted"] == 1
    assert data["target_count"] == 1
    assert data["provider_name"] == "sourcify"
    assert data["chain_id"] == 8453
    assert data["api_keys_required"] is False
    assert data["paid_calls_allowed"] is False
    assert data["raw_response_stored"] is False
    assert data["raw_body_stored"] is False
    assert data["secret_material_observed"] is False
    assert data["notSecurityGuarantee"] is True
    assert data["env_hash_before"] == data["env_hash_after"]
    assert data["trial_id"] == "T01"
    assert data["endpoint_label"] == "sourcify_full_match_metadata"
    assert isinstance(data.get("http_status"), (int, type(None)))
    assert data.get("error_type") is None or isinstance(data["error_type"], str)
    assert isinstance(data.get("reachable"), bool)
    assert isinstance(data.get("usable_metadata_received"), bool)
    assert isinstance(data.get("verified_source_status"), str)
    assert data.get("abi_available") in (True, False, "unknown", "true", "false")


def test_endpoint_validation_markdown_connectivity_only():
    md = REPORT_MD.read_text(encoding="utf-8").lower()

    assert "endpoint validation only" in md
    assert "no dataset-wide lookup" in md
    assert "no trial rerun" in md
    assert "provider remains disabled" in md


def test_approval_and_claims_reflect_endpoint_validation():
    approval = APPROVAL.read_text(encoding="utf-8").lower()
    claims = CLAIMS.read_text(encoding="utf-8").lower()

    assert "v11.4_endpoint_validation_phrase_observed: true" in approval
    assert '"green light vps sourcify endpoint validation only"' in approval
    assert "trial rerun still blocked" in approval
    assert "sourcify endpoint validation one target" in claims
    assert "endpoint validation recorded / no trial rerun" in claims


def test_endpoint_validation_artifacts_forbid_unsafe_positive_phrases():
    combined = (
        REPORT_JSON.read_text(encoding="utf-8")
        + REPORT_MD.read_text(encoding="utf-8")
        + APPROVAL.read_text(encoding="utf-8")
        + CLAIMS.read_text(encoding="utf-8")
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
        "production provider active",
    ]
    for phrase in forbidden:
        assert phrase not in combined, phrase


def test_env_unchanged_during_endpoint_validation_result_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = REPORT_JSON.read_bytes()
    _ = REPORT_MD.read_text(encoding="utf-8")
    _ = APPROVAL.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
