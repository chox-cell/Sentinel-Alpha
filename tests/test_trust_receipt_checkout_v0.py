"""Trust Receipt pilot checkout v0 — page, docs, and claim discipline."""

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PILOT_HTML = REPO / "apps/website/pilot/trust-receipt.html"
CHECKOUT_DOC = REPO / "docs/17_growth/TRUST_RECEIPT_CHECKOUT_V0.md"
PLAYBOOK = REPO / "docs/17_growth/FIRST_REVENUE_PLAYBOOK.md"
ENV_FILE = REPO / ".env"

TREASURY = "0x3cf9C2E55485fF8DAFfb59c84a0fa7c03bDbAeaf"

_CHECKOUT_FIELDS = [
    "contact",
    "selected_tier",
    "payment_tx_hash",
    "proposed_action_summary",
    "chain",
    "result_ref_optional",
    "notes",
]

_NEGATION = re.compile(
    r"\b(not|no|never|false|forbidden|does not|do not|without|manual)\b",
    re.IGNORECASE,
)


def test_page_tiers_and_usdc_on_base():
    html = PILOT_HTML.read_text(encoding="utf-8")
    assert "Pay for Pilot" in html
    assert "$25" in html and "$50" in html and "$250" in html
    assert "Draft Review" in html
    assert "Operator Pilot" in html
    assert "Integration Sprint" in html
    low = html.lower()
    assert "usdc on base" in low
    assert TREASURY in html
    assert "manual pilot payment address" in low


def test_page_manual_verification_and_copy_actions():
    html = PILOT_HTML.read_text(encoding="utf-8")
    low = html.lower()
    assert "manual verification" in low
    assert "copy payment address" in low
    assert "copy checkout json" in low
    for field in _CHECKOUT_FIELDS:
        assert field in html or field.replace("_", " ") in low


def test_page_no_escrow_or_automated_fulfillment_claims():
    html = PILOT_HTML.read_text(encoding="utf-8")
    low = html.lower()
    # Must not positively claim escrow or automated fulfillment
    assert "escrow service" not in low
    assert "automated fulfillment on payment" not in low
    assert "instant delivery" not in low
    # Negated forms are required on page
    assert "not escrow" in low or "not escrow." in low or "not a custodial escrow" in low
    assert "not automated fulfillment" in low or "no automated fulfillment" in low


def test_checkout_doc_no_revenue_until_tx_confirmed():
    assert CHECKOUT_DOC.is_file()
    doc = CHECKOUT_DOC.read_text(encoding="utf-8").lower()
    assert "no revenue claim" in doc or "no revenue" in doc
    assert "tx confirmed" in doc or "payment confirmed" in doc
    assert "no escrow" in doc or "not escrow" in doc
    assert "not automated" in doc or "no automated" in doc
    assert TREASURY in CHECKOUT_DOC.read_text(encoding="utf-8")
    assert "refund" in doc or "cure" in doc


def test_playbook_references_checkout_v0():
    text = PLAYBOOK.read_text(encoding="utf-8")
    assert "TRUST_RECEIPT_CHECKOUT_V0.md" in text
    assert "checkout v0" in text.lower()


def test_env_file_unchanged_in_git():
    """This mission must not modify .env."""
    result = subprocess.run(
        ["git", "status", "--porcelain", ".env"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout.strip() == "", f".env git status not clean: {result.stdout!r}"
