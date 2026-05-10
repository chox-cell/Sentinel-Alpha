import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STATUS_REPORT = REPO_ROOT / "docs/16_launch/SENTINEL_ALPHA_TECHNICAL_STATUS_REPORT.md"
CLAIMS_LEDGER = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_technical_status_report_core_truths():
    assert STATUS_REPORT.exists()
    text = STATUS_REPORT.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Sentinel Alpha Technical Status Report v11.0" in text
    assert "beezshield builds guardians, not traders" in lower
    assert "pre-execution risk decision layer" in lower
    assert "/contracts/risk-score" in text
    assert "@beezshield/sentinel" in text
    assert "agentkit-style" in lower
    assert "decision receipt" in lower
    assert "payment decision link" in lower
    assert "trust loop report fixture" in lower
    assert "approval_status: not_approved" in text
    assert '"green light live provider trial"' in text
    assert "611 passed" in text
    assert ".env" in lower and "remained unchanged" in lower
    assert "no wallet execution/signing" in lower
    assert "no automatic x402 settlement claim" in lower
    assert "no official integration claim" in lower
    assert "no partnership claim" in lower
    assert "not a trading/arbitrage agent" in lower


def test_claims_ledger_status_report_row():
    ledger = CLAIMS_LEDGER.read_text(encoding="utf-8").lower()
    assert "sentinel alpha technical status report v11.0" in ledger
    assert "report created / no new runtime activation" in ledger


def test_forbidden_overclaim_phrases_absent():
    lower = STATUS_REPORT.read_text(encoding="utf-8").lower()
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
    ]
    for token in forbidden:
        assert token not in lower, token


def test_env_unchanged_during_status_report_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = STATUS_REPORT.read_text(encoding="utf-8")
    _ = CLAIMS_LEDGER.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
