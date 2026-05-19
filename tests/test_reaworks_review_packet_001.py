"""ReaWorks $25 review packet 001 — claim-safe, no secrets."""

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKET = REPO / "docs/17_growth/REAWORKS_REVIEW_PACKET_001.md"
FIXTURE = REPO / "docs/17_growth/fixtures/trust_receipt_reaworks_review_packet_001.redacted.json"
SPEC = REPO / "docs/17_growth/TRUST_RECEIPT_V0_SPEC.md"
PILOT_PACK = REPO / "docs/17_growth/TRUST_RECEIPT_PILOT_PACK.md"

REQUIRED = {
    "receipt_id",
    "proposed_action",
    "normalized_args_hash",
    "secrets_excluded",
    "sentinel_decision",
    "risk_score",
    "policy_version",
    "decision_timestamp",
    "checked_signals",
    "not_checked",
    "agentkit_result_hash_or_tx_ref",
    "payment_lane",
    "release_refund_cure_rule",
    "disclaimer",
}

_SECRET_PATTERNS = [
    re.compile(r"private[_-]?key", re.I),
    re.compile(r"mnemonic|seed phrase", re.I),
    re.compile(r"\.env", re.I),
    re.compile(r"internal logs", re.I),
    re.compile(r"bearer\s+[a-z0-9._-]{20,}", re.I),
    re.compile(r"api[_-]?key\s*[:=]", re.I),
    re.compile(r"X402-PAYMENT", re.I),
    re.compile(r"0x[a-fA-F0-9]{64}"),
]

_RAW_ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}\b")

_FORBIDDEN_POSITIVE = [
    "security guarantee is provided",
    "guaranteed protection",
    "official agentkit integration",
    "partnership with coinbase",
    "endorsed by coinbase",
    "detects honeypots",
    "prevents mev",
    "proves execution quality",
    "safe to execute",
]

_NEGATION = re.compile(
    r"\b(not|no|never|forbidden|do not|does not|without|excluded)\b",
    re.IGNORECASE,
)


def _load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_v0_spec_and_pilot_pack_committed():
    assert SPEC.is_file()
    assert PILOT_PACK.is_file()
    assert "trust-receipt-v0" in SPEC.read_text(encoding="utf-8")
    assert "TRUST_RECEIPT_V0_SPEC" in PILOT_PACK.read_text(encoding="utf-8")


def test_review_packet_has_required_sections():
    text = PACKET.read_text(encoding="utf-8")
    assert "reaworks-review-packet-001" in text
    assert "secrets_excluded" in text
    assert "normalized_args_hash" in text
    assert "sentinel_decision" in text
    assert "What this proves / does not prove" in text
    assert "release_refund_cure_rule" in text or "release/refund" in text.lower()
    assert "$25" in text
    assert "a_reconstruct" in text.lower() or "reconstruct **what Sentinel checked**" in text
    assert "separate pre-check" in text.lower() or "separate pre-check from post-action" in text
    assert "unsupported guarantees" in text.lower() or "guarantees** explicitly excluded" in text


def test_fixture_required_fields_and_acceptance_checks():
    data = _load_fixture()
    assert REQUIRED <= set(data.keys())
    assert data["receipt_id"] == "reaworks-review-packet-001"
    assert data["secrets_excluded"] is True
    assert len(data["not_checked"]) > 0
    assert len(data["checked_signals"]) > 0
    checks = data.get("acceptance_checks") or {}
    assert "a_reconstruct_what_sentinel_checked" in checks
    assert "b_separate_precheck_from_post_action" in checks
    assert "c_guarantees_explicitly_excluded" in checks


def test_no_secrets_in_packet_and_fixture():
    for path in (PACKET, FIXTURE):
        blob = path.read_text(encoding="utf-8")
        for pat in _SECRET_PATTERNS:
            start = 0
            while True:
                m = pat.search(blob, start)
                if not m:
                    break
                line_start = blob.rfind("\n", 0, m.start()) + 1
                line_end = blob.find("\n", m.start())
                if line_end < 0:
                    line_end = len(blob)
                line = blob[line_start:line_end]
                if _NEGATION.search(line) or line.strip().startswith("- "):
                    start = m.end()
                    continue
                raise AssertionError(f"{path.name}: {pat.pattern!r} in {line.strip()!r}")
        assert not _RAW_ADDRESS.search(blob), f"raw address in {path.name}"


def test_no_guarantee_partnership_integration_claims():
    combined = PACKET.read_text(encoding="utf-8") + FIXTURE.read_text(encoding="utf-8")
    for phrase in _FORBIDDEN_POSITIVE:
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
            raise AssertionError(f"forbidden claim {phrase!r} in: {line.strip()!r}")
    data = _load_fixture()
    assert data.get("partnership_claimed") is False
    assert data.get("integration_claimed") is False
    assert data.get("endorsement_claimed") is False
    assert data.get("notSecurityGuarantee") is True
