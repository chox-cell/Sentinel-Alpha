import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_submission_pack_exists_and_has_required_content():
    assert PACK.exists()
    text = PACK.read_text(encoding="utf-8")
    low = text.lower()

    assert "x402 directory submission pack" in low
    assert "x402scan.com" in text
    assert "Agentic.Market" in text
    assert "Pay.sh" in text
    assert "app.ampersend.ai/discover" in text
    assert "BeezShield builds guardians, not traders" in text
    assert "@beezshield/sentinel" in text
    assert "/contracts/risk-score" in text
    assert "x402-gated API posture" in text
    assert "not submitted" in low
    assert "official x402 integration" in low
    assert "not official x402 integration" in low or "no official x402 integration" in low
    assert "x402 partnership" in low
    assert "x402 endorsement" in low


def test_outreach_tracker_directory_redirection():
    ot = OUTREACH.read_text(encoding="utf-8").lower()
    assert "directory redirection" in ot
    assert "x402scan" in ot
    assert "not submitted" in ot
    assert "integration_claim: false" in ot or "no integration" in ot


def test_claims_directory_redirection_row():
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "x402 directory redirection signal" in cl
    assert "no integration" in cl
    assert "no partnership" in cl


def test_posture_docs_forbid_unsafe_positive_phrases():
    # Submission pack §8 lists forbidden shorthand explicitly; scan tracker + claims only.
    combined = (OUTREACH.read_text(encoding="utf-8") + CLAIMS.read_text(encoding="utf-8")).lower()
    forbidden = [
        "official x402 integration",
        "x402 partnership",
        "x402 endorsement",
        "automatic x402 settlement live",
        "guaranteed protection",
        "detects honeypots",
        "prevents mev",
        "prevents prompt injection",
    ]
    for phrase in forbidden:
        assert phrase not in combined, phrase


def test_env_unchanged_during_x402_submission_pack_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = PACK.read_bytes()
    _ = OUTREACH.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
