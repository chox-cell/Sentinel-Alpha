"""ReaWorks-style Trust Receipt pilot artifact — claim-safe fixture and docs."""

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOC = REPO / "docs/17_growth/TRUST_RECEIPT_REAWORKS_PILOT.md"
FIXTURE = REPO / "docs/17_growth/fixtures/trust_receipt_reaworks_pilot.redacted.json"

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
    re.compile(r"\bseed\b", re.I),
    re.compile(r"\.env", re.I),
    re.compile(r"bearer\s+[a-z0-9._-]{20,}", re.I),
    re.compile(r"api[_-]?key\s*[:=]", re.I),
    re.compile(r"X402-PAYMENT", re.I),
    re.compile(r"0x[a-fA-F0-9]{64}"),
]

_RAW_ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}\b")

_GUARANTEE_POSITIVE = [
    "security guarantee is provided",
    "guaranteed protection",
    "proves execution quality",
    "safe to execute",
    "honeypot detected",
    "mev prevented",
]

_NEGATION = re.compile(
    r"\b(not|no|never|forbidden|do not|does not|without)\b",
    re.IGNORECASE,
)


def _load() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_doc_and_fixture_exist():
    assert DOC.is_file()
    text = DOC.read_text(encoding="utf-8")
    assert "What this proves / does not prove" in text
    assert "$25" in text and "50" in text
    assert FIXTURE.name in text
    assert "reaworks-pilot-2026-05-19-001" in text
    assert "does not prove" in text.lower()
    assert "execution quality" in text.lower()


def test_required_fields_present():
    data = _load()
    assert REQUIRED <= set(data.keys())
    assert data["receipt_id"] == "reaworks-pilot-2026-05-19-001"
    assert data["secrets_excluded"] is True
    assert data["sentinel_decision"] in {"allow", "review", "block"}
    assert isinstance(data["not_checked"], list) and len(data["not_checked"]) > 0
    assert isinstance(data["checked_signals"], list) and len(data["checked_signals"]) > 0
    low = data["disclaimer"].lower()
    assert "not a security guarantee" in low
    assert "execution-quality" in low or "execution quality" in low


def test_no_secrets_or_raw_internals_in_fixture():
    blob = FIXTURE.read_text(encoding="utf-8")
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
            if _NEGATION.search(line) or "no " in line.lower():
                start = m.end()
                continue
            raise AssertionError(f"secret pattern {pat.pattern!r} in: {line.strip()!r}")
    assert not _RAW_ADDRESS.search(blob)
    ref = _load()["agentkit_result_hash_or_tx_ref"]
    assert ref.startswith("exec_ref:") or ref.startswith("tx_ref:")


def test_no_positive_guarantee_claims_in_doc_and_fixture():
    combined = DOC.read_text(encoding="utf-8") + FIXTURE.read_text(encoding="utf-8")
    for phrase in _GUARANTEE_POSITIVE:
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
            if _NEGATION.search(line) or line.strip().startswith("- "):
                start = idx + len(phrase)
                continue
            raise AssertionError(f"positive guarantee claim {phrase!r} in: {line.strip()!r}")


def test_post_action_boundary_flags():
    data = _load()
    post = data.get("post_action_summary") or {}
    assert post.get("result_ref_only") is True
    assert post.get("execution_quality_claimed") is False
    assert post.get("raw_tx_internals_included") is False
    assert data.get("execution_quality_claimed") is False
