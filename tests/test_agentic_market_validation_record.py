"""Agentic.Market v2 validation record — claim-safe docs."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROWTH = ROOT / "docs" / "17_growth"
CLAIMS = ROOT / "docs" / "18_investor" / "CLAIMS_LEDGER.md"

_FORBIDDEN = [
    "official x402 partnership",
    "endorsed by agentic",
    "certified by agentic",
    "guaranteed protection",
    "listed on agentic.market",
    "partnership with agentic",
]

_NEGATION = re.compile(
    r"\b(not|no|never|forbidden|do not|does not|without)\b",
    re.IGNORECASE,
)

DOCS = (
    GROWTH / "BAZAAR_V2_COMPATIBILITY_PLAN.md",
    GROWTH / "AGENTIC_MARKET_SUBMISSION_PACK.md",
    GROWTH / "OUTREACH_TRACKER.md",
    CLAIMS,
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
            if (
                _NEGATION.search(line)
                or "forbidden" in line.lower()
                or line.strip().startswith("- ")
            ):
                start = idx + len(phrase)
                continue
            raise AssertionError(f"{label}: positive forbidden {phrase!r} in: {line.strip()!r}")


def test_v2_validation_record_present():
    plan = (GROWTH / "BAZAAR_V2_COMPATIBILITY_PLAN.md").read_text(encoding="utf-8")
    assert "agentic.market/validate" in plan
    assert "risk-score-v2" in plan
    assert "rejected_needs_fix" in plan
    assert "b57330a" in plan
    assert "Production verification" in plan
    assert "toolName" in plan and "output.example" in plan
    assert "agentic-market-validate-v2-b57330a-2026-05-19.png" in plan


def test_submission_pack_rejected_not_listed():
    pack = (GROWTH / "AGENTIC_MARKET_SUBMISSION_PACK.md").read_text(encoding="utf-8")
    assert "**rejected_needs_fix**" in pack
    assert "validator_passed_not_listed" in pack
    assert "listed_verified" in pack


def test_outreach_v2_attempt_block():
    tracker = (GROWTH / "OUTREACH_TRACKER.md").read_text(encoding="utf-8")
    assert "Bazaar v2 production verify" in tracker
    assert "b57330a" in tracker
    assert "risk-score-v2" in tracker
    assert "listing_success_claim: false" in tracker
    assert "SDK Parse Error" in tracker


def test_no_forbidden_agentic_claims_in_growth_docs():
    for path in DOCS:
        _assert_no_positive_forbidden(path.read_text(encoding="utf-8"), label=path.name)


def test_evidence_screenshot_exists():
    shot = GROWTH / "evidence" / "agentic-market-validate-v2-2026-05-19.png"
    assert shot.is_file() and shot.stat().st_size > 0
