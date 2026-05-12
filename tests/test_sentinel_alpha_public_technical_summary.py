import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SUMMARY = REPO_ROOT / "docs/17_growth/SENTINEL_ALPHA_PUBLIC_TECHNICAL_SUMMARY.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_public_summary_exists_and_covers_core_truths():
    assert SUMMARY.exists()
    text = SUMMARY.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Sentinel Alpha Public Technical Summary" in text
    assert "pre-execution decision layer" in lower
    assert "beezshield builds guardians, not traders" in lower
    assert "autonomous agents should not execute blind" in lower
    assert "/contracts/risk-score" in text
    assert "@beezshield/sentinel" in text
    assert "agentkit-style local demo" in lower
    assert "decision receipt" in lower
    assert "payment decision link" in lower
    assert "trust loop report fixture" in lower
    assert "live abi/source provider not active" in lower
    assert "sourcify attempt recorded as network_error only" in lower
    assert "vps preflight planned but not run" in lower
    assert "no wallet execution/signing" in lower
    assert "no automatic x402 settlement claim" in lower
    assert "no official integration/partnership claim" in lower
    assert "631 tests" in lower
    assert ".env" in lower and "unchanged" in lower
    assert "not a trading/arbitrage agent" in lower


def test_claims_ledger_public_summary_row():
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    assert "sentinel alpha public technical summary" in ledger
    assert "public-safe summary created / no runtime activation" in ledger


def test_public_summary_forbids_unsafe_positive_phrases():
    lower = SUMMARY.read_text(encoding="utf-8").lower()
    forbidden = [
        "guaranteed protection",
        "detects honeypots",
        "prevents mev",
        "prevents prompt injection",
        "live simulation",
        "full abi coverage",
        "guaranteed source verification",
        "partnership live",
        "integration is live",
        "production provider active",
    ]
    for phrase in forbidden:
        assert phrase not in lower, phrase


def test_env_unchanged_during_public_summary_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = SUMMARY.read_text(encoding="utf-8")
    _ = CLAIMS_LEDGER.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
