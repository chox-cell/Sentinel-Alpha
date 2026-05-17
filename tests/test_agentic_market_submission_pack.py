"""Agentic.Market directory submission pack — docs-only preparation."""

import hashlib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/AGENTIC_MARKET_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"

_FORBIDDEN = [
    "official x402 integration",
    "x402 partnership",
    "x402scan endorsement",
    "security guarantee",
    "certified protection",
]

_NEGATION = re.compile(
    r"\b(not|no|never|forbidden|do not|does not|without)\b",
    re.IGNORECASE,
)


def _assert_no_positive_forbidden(text: str, *, label: str) -> None:
    for phrase in _FORBIDDEN:
        start = 0
        while True:
            idx = text.lower().find(phrase, start)
            if idx < 0:
                break
            line_start = text.rfind("\n", 0, idx) + 1
            line_end = text.find("\n", idx)
            if line_end < 0:
                line_end = len(text)
            line = text[line_start:line_end]
            if _NEGATION.search(line):
                start = idx + len(phrase)
                continue
            if "forbidden" in line.lower() and phrase in line.lower():
                start = idx + len(phrase)
                continue
            raise AssertionError(f"{label}: positive forbidden phrase {phrase!r} in: {line.strip()!r}")


def _pack_public_copy() -> str:
    body = PACK.read_text(encoding="utf-8")
    marker = "## Claim-safe boundaries"
    if marker in body:
        return body.split(marker, 1)[0]
    return body


def test_pack_exists_with_required_fields():
    assert PACK.exists()
    text = PACK.read_text(encoding="utf-8")
    low = text.lower()
    assert "prepared" in low and "not submitted" in low
    assert "Agentic.Market" in text
    assert "https://beezshield.com/" in text
    assert "https://api.beezshield.com/contracts/risk-score" in text
    assert "https://beezshield.com/registry/x402scan.html" in text
    assert "0.02 USDC" in text
    assert "Base" in text
    assert "x402scan" in low and "registered" in low
    assert "manual submission checklist" in low
    assert "@beezshield/sentinel" in text
    assert (
        "BeezShield Sentinel Alpha is a pre-execution risk decision API for autonomous agents, payable with x402 on Base."
        in text
    )


def test_outreach_tracker_prepared_block():
    ot = OUTREACH.read_text(encoding="utf-8")
    low = ot.lower()
    assert "prepared_not_submitted" in low
    assert "AGENTIC_MARKET_SUBMISSION_PACK.md" in ot
    assert "x402scan_proof_available: true" in ot
    assert "manual_submission_required: true" in ot
    assert "submission_result: null" in ot


def test_pack_public_copy_no_positive_forbidden_claims():
    _assert_no_positive_forbidden(_pack_public_copy(), label="pack public copy")


def test_outreach_and_claims_no_positive_forbidden_claims():
    combined = OUTREACH.read_text(encoding="utf-8") + CLAIMS.read_text(encoding="utf-8")
    _assert_no_positive_forbidden(combined, label="outreach+claims")


def test_env_unchanged_agentic_market_pack():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK.read_bytes()
    _ = OUTREACH.read_bytes()
    _ = CLAIMS.read_bytes()
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
