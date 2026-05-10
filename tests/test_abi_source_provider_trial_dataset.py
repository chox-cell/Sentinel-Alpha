import hashlib
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DATASET_DOC = REPO_ROOT / "docs/16_launch/ABI_SOURCE_PROVIDER_TRIAL_DATASET.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_dataset_doc_exists_and_core_content():
    assert DATASET_DOC.exists()
    text = DATASET_DOC.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Known Base Contracts Trial Dataset v1" in text
    assert "planning-only" in lower or "planning only" in lower
    assert "no provider calls" in lower
    assert "provider disabled by default" in lower
    assert "max 5 trial targets" in lower

    trial_ids = re.findall(r"\bT0[1-5]\b", text)
    assert len(set(trial_ids)) == 5
    table_rows = len(re.findall(r"\| T0[1-5] \|", text))
    assert table_rows == 5

    assert "base chain only" in lower
    assert "erc20-like" in lower
    assert "nft-like" in lower
    assert "proxy-like" in lower
    assert "router/pool-like" in lower
    assert "generic/utility" in lower

    assert "trial_status: not_run" in text
    assert "source_status_before_trial: unknown" in text

    assert ".env unchanged proof" in lower
    assert "no paid call requirement" in lower
    assert "no public guarantee wording" in lower


def test_claims_ledger_dataset_row():
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    assert "known base contracts trial dataset" in ledger
    assert "prepared / not run" in ledger


def test_dataset_forbidden_phrases_absent():
    text = DATASET_DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "addresses live verified",
        "live abi coverage",
        "full verified-source coverage",
        "guaranteed source verification",
        "detects honeypots",
        "guaranteed protection",
        "prevents mev",
        "live simulation",
    ]
    for token in forbidden:
        assert token not in text, f"unexpected phrase: {token}"


def test_env_unchanged_during_dataset_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DATASET_DOC.read_text(encoding="utf-8")
    _ = CLAIMS_LEDGER.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
