"""ReaWorks commercial status — clarification pending; no revenue/customer claims."""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TRACKER = REPO / "docs/17_growth/OUTREACH_TRACKER.md"
CLAIMS = REPO / "docs/18_investor/CLAIMS_LEDGER.md"
ROADMAP = REPO / "docs/00_project/SENTINEL_ALPHA_ROADMAP_TRACKER.md"
PACKET = REPO / "docs/17_growth/REAWORKS_REVIEW_PACKET_001.md"
FIXTURE = REPO / "docs/17_growth/fixtures/trust_receipt_reaworks_review_packet_001.redacted.json"

_FORBIDDEN_UNVERIFIED = [
    "paid customer",
    "revenue confirmed",
    "first revenue",
    "pilot sold",
    "our customer",
    "official partnership",
    "endorsed by reaworks",
    "integration with reaworks",
]

_NEGATION = re.compile(
    r"\b(not|no|never|false|forbidden|pending|clarification|do not|does not|without|likely)\b",
    re.IGNORECASE,
)


def _reaworks_block(text: str) -> str:
    marker = "## ReaWorks — Trust Receipt"
    start = text.find(marker)
    assert start >= 0, "ReaWorks section missing"
    nxt = text.find("\n## ", start + 1)
    return text[start:nxt] if nxt >= 0 else text[start:]


def test_tracker_clarification_pending_status():
    text = _reaworks_block(TRACKER.read_text(encoding="utf-8"))
    assert "outside_review_offer_clarification_pending" in text
    assert "clarification pending" in text.lower() or "clarification_pending" in text.lower()
    assert "REAWORKS_REVIEW_PACKET_001.md" in text
    assert "trust_receipt_reaworks_review_packet_001.redacted.json" in text
    assert "payment_sent" in text and "**false**" in text
    assert "reviewer_payment_method_pending" in text
    assert "revenue_confirmed" in text and "**false**" in text
    assert "paid_customer_claim" in text and "**false**" in text
    assert "first_revenue_claim" in text and "**false**" in text


def test_claims_ledger_clarification_not_revenue():
    row = CLAIMS.read_text(encoding="utf-8")
    assert "ReaWorks" in row
    assert "clarification pending" in row.lower() or "pending clarification" in row.lower()
    assert "not customer revenue" in row.lower() or "not revenue" in row.lower()
    assert "Forbidden" in row or "forbidden" in row.lower()
    assert "first revenue" in row.lower()
    assert "pilot sold" in row.lower()


def test_roadmap_buyer_reviewer_validation_not_revenue():
    text = ROADMAP.read_text(encoding="utf-8").lower()
    assert "first buyer/reviewer validation loop" in text
    assert "first-revenue loop" not in text
    assert "clarification pending" in text
    assert "not revenue" in text


def test_no_unverified_revenue_customer_partnership_claims():
    combined = (
        _reaworks_block(TRACKER.read_text(encoding="utf-8"))
        + CLAIMS.read_text(encoding="utf-8")
        + ROADMAP.read_text(encoding="utf-8")
        + PACKET.read_text(encoding="utf-8")
        + FIXTURE.read_text(encoding="utf-8")
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
            if _NEGATION.search(line) or line.strip().startswith(("- ", "| **", '"')):
                start = idx + len(phrase)
                continue
            raise AssertionError(f"unverified claim {phrase!r} in: {line.strip()!r}")


def test_packet_no_payment_received_implied():
    text = PACKET.read_text(encoding="utf-8").lower()
    assert "no payment sent or received" in text or "not confirmed" in text
    assert "pending clarification" in text
    assert "partnership" in text and _NEGATION.search(text)
