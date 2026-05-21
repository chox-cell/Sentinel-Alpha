"""ReaWorks — community feedback only; paid review cancelled; no payment/revenue claims."""

import json
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
    "paid review completed",
    "payment sent",
]

_NEGATION = re.compile(
    r"\b(not|no|never|false|forbidden|cancelled|paused|did not|does not|without|null)\b",
    re.IGNORECASE,
)


def _reaworks_block(text: str) -> str:
    marker = "## ReaWorks — Trust Receipt"
    start = text.find(marker)
    assert start >= 0, "ReaWorks section missing"
    nxt = text.find("\n## ", start + 1)
    return text[start:nxt] if nxt >= 0 else text[start:]


def _load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_tracker_community_feedback_only_status():
    text = _reaworks_block(TRACKER.read_text(encoding="utf-8"))
    assert "community_feedback_only" in text
    assert "cancelled_or_paused" in text
    assert "REAWORKS_REVIEW_PACKET_001.md" in text
    assert "trust_receipt_reaworks_review_packet_001.redacted.json" in text
    assert "payment_sent" in text and "**false**" in text
    assert "tx_hash" in text and "**null**" in text
    assert "revenue_confirmed" in text and "**false**" in text
    assert "paid_customer_claim" in text and "**false**" in text
    assert "paid_review_completed" in text and "**false**" in text


def test_fixture_payment_and_revenue_flags():
    data = _load_fixture()
    assert data["status"] == "community_feedback_only"
    assert data["paid_review_status"] in {"cancelled_or_paused", "cancelled", "paused"}
    assert data["payment_sent"] is False
    assert data["tx_hash"] is None
    assert data["revenue_confirmed"] is False
    assert data["paid_customer_claim"] is False


def test_claims_ledger_community_feedback_not_revenue():
    row = CLAIMS.read_text(encoding="utf-8")
    assert "ReaWorks" in row
    assert "community feedback" in row.lower()
    assert "paid review not proceeded" in row.lower() or "not proceeded" in row.lower()
    assert "Forbidden" in row or "forbidden" in row.lower()
    assert "payment sent" in row.lower()
    assert "revenue confirmed" in row.lower()


def test_roadmap_community_validation_not_first_revenue():
    text = ROADMAP.read_text(encoding="utf-8").lower()
    assert "community validation" in text or "community feedback" in text
    assert "direct buyer" in text or "buyer/operator" in text
    assert "cancelled_or_paused" in text or "not proceeded" in text
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


def test_packet_no_active_paid_review():
    text = PACKET.read_text(encoding="utf-8").lower()
    assert "community_feedback_only" in text or "community feedback" in text
    assert "cancelled_or_paused" in text or "did not proceed" in text
    assert "payment_sent" in text and "false" in text
    assert "tx_hash" in text and "null" in text
    assert "partnership" in text and _NEGATION.search(text)
