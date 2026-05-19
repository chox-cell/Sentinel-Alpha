"""ReaWorks packet_sent_pending_review_payment — no unverified revenue/customer claims."""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TRACKER = REPO / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO / "docs/18_investor/CLAIMS_LEDGER.md"
ROADMAP = REPO / "docs/00_project/SENTINEL_ALPHA_ROADMAP_TRACKER.md"
PACKET = REPO / "docs/17_growth/REAWORKS_REVIEW_PACKET_001.md"

_FORBIDDEN_UNVERIFIED = [
    "paid customer",
    "revenue confirmed",
    "our customer",
    "official partnership",
    "endorsed by reaworks",
    "integration with reaworks",
]

_NEGATION = re.compile(
    r"\b(not|no|never|false|forbidden|pending|do not|does not|without)\b",
    re.IGNORECASE,
)


def _reaworks_block(text: str) -> str:
    marker = "## ReaWorks — Trust Receipt"
    start = text.find(marker)
    assert start >= 0, "ReaWorks section missing"
    nxt = text.find("\n## ", start + 1)
    return text[start:nxt] if nxt >= 0 else text[start:]


def test_tracker_packet_sent_status_and_files():
    text = _reaworks_block(TRACKER.read_text(encoding="utf-8"))
    assert "packet_sent_pending_review_payment" in text
    assert "2026-05-20" in text
    assert "REAWORKS_REVIEW_PACKET_001.md" in text
    assert "trust_receipt_reaworks_review_packet_001.redacted.json" in text
    assert "revenue_confirmed" in text and "**false**" in text
    assert "paid_customer_claim" in text and "**false**" in text


def test_claims_ledger_reaworks_row():
    row = CLAIMS.read_text(encoding="utf-8")
    assert "ReaWorks $25 Trust Receipt review" in row
    assert "packet sent" in row.lower()
    assert "payment and review outcome not confirmed" in row
    assert "Forbidden" in row or "forbidden" in row.lower()


def test_roadmap_v13_first_revenue_loop_pending():
    text = ROADMAP.read_text(encoding="utf-8")
    assert "v13.0 first-revenue loop" in text
    assert "packet sent" in text
    assert "payment pending" in text.lower() or "payment/review pending" in text.lower()
    assert "no revenue confirmed" in text.lower()


def test_no_unverified_customer_revenue_partnership_claims():
    combined = (
        _reaworks_block(TRACKER.read_text(encoding="utf-8"))
        + CLAIMS.read_text(encoding="utf-8")
        + ROADMAP.read_text(encoding="utf-8")
    )
    for phrase in _FORBIDDEN_UNVERIFIED:
        start = 0
        while True:
            idx = combined.lower().find(phrase, start)
            if idx < 0:
                break
            line_start = combined.rfind("\n", 0, idx) + 1
            line_end = combined.find("\n", idx)
            if line_end < 0:
                line_end = len(combined)
            line = combined[line_start:line_end]
            if _NEGATION.search(line) or line.strip().startswith(("- ", "| **")):
                start = idx + len(phrase)
                continue
            raise AssertionError(f"unverified claim {phrase!r} in: {line.strip()!r}")


def test_packet_doc_unchanged_claim_discipline():
    text = PACKET.read_text(encoding="utf-8").lower()
    assert "security guarantee" in text
    assert "execution-quality" in text or "execution quality" in text
    assert "partnership" in text and _NEGATION.search(text)
