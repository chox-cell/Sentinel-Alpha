"""x402scan directory registration success — docs-only evidence pack."""

import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"
EVIDENCE = REPO_ROOT / "docs/17_growth/X402SCAN_REGISTRATION_EVIDENCE.md"
BRAND = REPO_ROOT / "docs/17_growth/BEEZSHIELD_BRAND_LOGO_BRIEF.md"

_FORBIDDEN_IN_NEW_ROW = [
    "official x402 integration",
    "x402 partnership",
    "x402 endorsement",
    "security guarantee",
    "x402scan partner",
    "x402scan partnership",
]


def test_submission_pack_records_registration_success():
    text = PACK.read_text(encoding="utf-8")
    low = text.lower()
    assert "x402scan" in low
    assert "registered" in low
    assert "Successfully registered 1 of 1 resources" in text
    assert "/contracts/risk-score" in text
    assert "§3o" in text or "3o)" in low
    assert "BeezShield | Pre-execution decision engine for agents" in text
    assert "no official x402 integration" in low or "not official x402 integration" in low


def test_outreach_tracker_registered_with_claim_posture():
    ot = OUTREACH.read_text(encoding="utf-8")
    low = ot.lower()
    assert "registered" in low
    assert "official_integration_claim: false" in ot
    assert "partnership_claim: false" in ot
    assert "endorsement_claim: false" in ot
    assert "Successfully registered 1 of 1 resources" in ot


def test_claims_ledger_registration_row_public_safe():
    cl = CLAIMS.read_text(encoding="utf-8")
    low = cl.lower()
    assert "x402scan directory registration" in low
    assert "directory registration only" in low
    # Locate new row slice (after fourteenth diagnosis, before Mycelium)
    idx = low.find("x402scan directory registration")
    assert idx >= 0
    row_chunk = low[idx : idx + 800]
    for phrase in _FORBIDDEN_IN_NEW_ROW:
        assert phrase not in row_chunk, phrase
    assert "registered as a payable x402 resource on x402scan" in row_chunk


def test_evidence_and_brand_brief_files():
    assert EVIDENCE.exists()
    ev = EVIDENCE.read_text(encoding="utf-8")
    assert "What this proves" in ev
    assert "What this does not prove" in ev
    assert "no security guarantee" in ev.lower()

    assert BRAND.exists()
    br = BRAND.read_text(encoding="utf-8")
    assert "BeezShield" in br
    assert "Machine Trust Infrastructure" in br
    assert "readable at 16px" in br
    assert "apps/website/public/brand/beezshield-logo.svg" in br
    assert "apps/website/public/brand/beezshield-icon.svg" in br
    assert "apps/website/public/brand/beezshield-og.png" in br
    assert "apps/website/public/brand/x402scan-logo.png" in br


def test_env_unchanged_registration_success_docs():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    _ = OUTREACH.read_bytes()
    _ = CLAIMS.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
