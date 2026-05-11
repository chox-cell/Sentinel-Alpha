import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
APPROVAL = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_APPROVAL_RECORD.md"
DATASET = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_DATASET.md"
SAMPLE_JSON = REPO_ROOT / "reports/provider_trials/abi_source_trial_results.sample.json"
SAMPLE_MD = REPO_ROOT / "reports/provider_trials/abi_source_trial_results.sample.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def _dataset_rows() -> list[dict[str, str]]:
    text = DATASET.read_text(encoding="utf-8")
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip().startswith("| T0")
    ]
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


def test_approval_record_captures_founder_phrase_without_execution():
    text = APPROVAL.read_text(encoding="utf-8")

    assert '"green light live provider trial"' in text
    assert "founder_phrase_observed: true" in text
    assert "approval_status: approved_pending_real_target_validation" in text
    assert "trial_run: false" in text
    assert "provider_active: false" in text
    assert "live_calls_performed: false" in text
    assert "api_keys_required: false" in text
    assert "paid_calls_allowed: false" in text


def test_dataset_has_five_base_targets_with_source_urls_or_replacement_flags():
    rows = _dataset_rows()

    assert [row["trial_id"] for row in rows] == ["T01", "T02", "T03", "T04", "T05"]
    for row in rows:
        assert row["chain"] == "base"
        assert row["chain_id"] == "8453"
        assert row["source_status_before_trial"] == "unknown"
        assert row["trial_status"] == "not_run"

        address = row["contract_address"].strip("`")
        source_url = row["source_url"].strip("`")
        row_text = " ".join(row.values()).lower()
        is_placeholder = address.lower() in {
            "0x1111111111111111111111111111111111111111",
            "0x2222222222222222222222222222222222222222",
            "0x3333333333333333333333333333333333333333",
            "0x4444444444444444444444444444444444444444",
            "0x5555555555555555555555555555555555555555",
        }
        if is_placeholder:
            assert "replacement_required: true" in row_text
        else:
            assert source_url.startswith("https://")
            assert address.lower() in source_url.lower()


def test_sample_evidence_remains_not_run():
    data = json.loads(SAMPLE_JSON.read_text(encoding="utf-8"))

    assert data["trial_run"] is False
    assert data["provider_active"] is False
    assert data["live_calls_performed"] is False
    assert data["api_keys_required"] is False
    for row in data["results"]:
        assert row["lookup_status"] == "not_run"
        assert len(row["contract_address_hash"]) == 64
        assert row["raw_response_stored"] is False


def test_claims_ledger_records_phrase_received_trial_not_run():
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()

    assert "founder approval for controlled abi/source provider trial" in ledger
    assert "phrase received / trial not run" in ledger
    assert "founder approval phrase recorded; live provider trial not executed yet" in ledger


def test_pretrial_files_do_not_use_forbidden_positive_phrases():
    combined = (
        APPROVAL.read_text(encoding="utf-8")
        + DATASET.read_text(encoding="utf-8")
        + SAMPLE_MD.read_text(encoding="utf-8")
        + SAMPLE_JSON.read_text(encoding="utf-8")
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
    for phrase in forbidden:
        assert phrase not in combined, phrase


def test_env_unchanged_during_founder_approval_target_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = APPROVAL.read_text(encoding="utf-8")
    _ = DATASET.read_text(encoding="utf-8")
    _ = SAMPLE_JSON.read_bytes()
    _ = SAMPLE_MD.read_text(encoding="utf-8")
    _ = CLAIMS_LEDGER.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
