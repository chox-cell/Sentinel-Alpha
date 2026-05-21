"""First-revenue pilot workflow — docs, fixture, and public pilot page claim discipline."""

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PILOT_HTML = REPO / "apps/website/pilot/trust-receipt.html"
INTAKE_SCHEMA = REPO / "docs/17_growth/TRUST_RECEIPT_PILOT_INTAKE_SCHEMA.md"
PLAYBOOK = REPO / "docs/17_growth/FIRST_REVENUE_PLAYBOOK.md"
BUYER_FIXTURE = REPO / "docs/17_growth/fixtures/trust_receipt_buyer_pilot_sample.redacted.json"

_INTAKE_FIELDS = [
    "contact",
    "project_name",
    "agent_or_tool_description",
    "proposed_action_summary",
    "chain",
    "contract_or_tool_ref_redacted",
    "has_post_action_result_ref",
    "preferred_payment_method",
    "notes",
]

_FORBIDDEN_REVENUE = [
    "revenue confirmed",
    "first revenue achieved",
    "we have revenue",
    "paid customer acquired",
]

_FORBIDDEN_PARTNERSHIP = [
    "official partnership",
    "official integration",
    "endorsed by coinbase",
    "endorsed by agentkit",
]

_SECRET_PATTERNS = [
    re.compile(r"private[_-]?key", re.I),
    re.compile(r"mnemonic|seed phrase", re.I),
    re.compile(r"\.env", re.I),
    re.compile(r"bearer\s+[a-z0-9._-]{20,}", re.I),
    re.compile(r"api[_-]?key\s*[:=]", re.I),
    re.compile(r"X402-PAYMENT", re.I),
    re.compile(r"0x[a-fA-F0-9]{64}"),
]

_RAW_ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}\b")

_NEGATION = re.compile(
    r"\b(not|no|never|false|forbidden|does not|do not|without|manual)\b",
    re.IGNORECASE,
)


def test_intake_schema_and_playbook_exist():
    assert INTAKE_SCHEMA.is_file()
    assert PLAYBOOK.is_file()
    schema = INTAKE_SCHEMA.read_text(encoding="utf-8")
    playbook = PLAYBOOK.read_text(encoding="utf-8")
    for field in _INTAKE_FIELDS:
        assert field in schema
    assert "$25" in playbook and "$50" in playbook and "$250" in playbook
    assert "conversion metric" in playbook.lower()
    assert "claim boundar" in playbook.lower()


def test_pilot_page_has_fifty_dollar_cta():
    html = PILOT_HTML.read_text(encoding="utf-8")
    assert "$50 Trust Receipt Pilot" in html
    low = html.lower()
    assert "one redacted" in low or "redacted action" in low
    assert "json" in low and "markdown" in low
    assert "manual" in low or "no payment automation" in low or "not automated" in low


def test_pilot_page_no_revenue_or_partnership_claims():
    html = PILOT_HTML.read_text(encoding="utf-8")
    low = html.lower()
    for phrase in _FORBIDDEN_REVENUE + _FORBIDDEN_PARTNERSHIP:
        idx = low.find(phrase)
        if idx < 0:
            continue
        line_start = html.rfind("\n", 0, idx) + 1
        line_end = html.find("\n", idx)
        if line_end < 0:
            line_end = len(html)
        line = html[line_start:line_end]
        assert _NEGATION.search(line), f"unqualified claim {phrase!r} in: {line.strip()!r}"
    assert "security guarantee" in low
    assert _NEGATION.search(html), "page should qualify guarantee/partnership language"


def test_buyer_pilot_fixture_excludes_secrets():
    blob = BUYER_FIXTURE.read_text(encoding="utf-8")
    for pat in _SECRET_PATTERNS:
        assert not pat.search(blob), f"secret pattern {pat.pattern!r} in fixture"
    assert not _RAW_ADDRESS.search(blob), "raw address in buyer pilot fixture"
    data = json.loads(blob)
    assert data["secrets_excluded"] is True
    assert data.get("revenue_confirmed") is False
    assert data.get("partnership_claimed") is False
    assert data.get("integration_claimed") is False
    assert data.get("endorsement_claimed") is False
    assert "json_receipt" in data.get("buyer_deliverables", {})
    assert "markdown_receipt" in data.get("buyer_deliverables", {})
