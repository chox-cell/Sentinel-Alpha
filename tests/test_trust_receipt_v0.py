"""Trust Receipt v0 — spec, pilot pack, and redacted fixture claim discipline."""

import json
import re
from pathlib import Path

_NEGATION = re.compile(
    r"\b(not|no|never|forbidden|do not|does not|without)\b",
    re.IGNORECASE,
)

REPO = Path(__file__).resolve().parents[1]
SPEC = REPO / "docs/17_growth/TRUST_RECEIPT_V0_SPEC.md"
PACK = REPO / "docs/17_growth/TRUST_RECEIPT_PILOT_PACK.md"
FIXTURE = REPO / "docs/17_growth/fixtures/trust_receipt_v0.redacted.sample.json"

REQUIRED_TOP_LEVEL = {
    "receipt_version",
    "receipt_id",
    "pilot_only",
    "secrets_excluded",
    "proposed_action",
    "normalized_args_hash",
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

_FORBIDDEN_POSITIVE = [
    "security guarantee is provided",
    "guaranteed protection",
    "official agentkit integration",
    "partnership with coinbase",
    "detects honeypots",
    "prevents mev",
    "execution-quality proof",
    "safe to execute",
]

_SECRET_PATTERNS = [
    re.compile(r"private[_-]?key", re.I),
    re.compile(r"mnemonic|seed phrase", re.I),
    re.compile(r"bearer\s+[a-z0-9._-]{20,}", re.I),
    re.compile(r"api[_-]?key\s*[:=]", re.I),
    re.compile(r"X402-PAYMENT", re.I),
    re.compile(r"0x[a-fA-F0-9]{64}"),  # signed tx / long secrets
]

# Allow known hash-only linking refs (64 hex) but not 66+ char 0x payloads
_RAW_ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}\b")


def _load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_spec_and_pilot_pack_exist():
    assert SPEC.is_file()
    assert PACK.is_file()
    spec = SPEC.read_text(encoding="utf-8")
    pack = PACK.read_text(encoding="utf-8")
    assert "trust-receipt-v0" in spec
    assert "GET /pilot/trust-receipt/v0" in spec
    assert "secrets_excluded" in spec
    assert "not a security guarantee" in spec.lower()
    assert "$25" in pack or "25–$50" in pack or "25-$50" in pack
    assert FIXTURE.name in pack
    assert "post_execution_trail" in spec
    assert "reputation_axis" in spec
    assert "mycelium" in spec.lower()
    assert "does not replace" in spec.lower() or "does not" in spec.lower()
    assert "Mycelium Trails" in pack
    assert "AURA" in pack


def test_fixture_has_required_fields_and_enums():
    data = _load_fixture()
    assert REQUIRED_TOP_LEVEL <= set(data.keys())
    assert data["receipt_version"] == "trust-receipt-v0"
    assert data["secrets_excluded"] is True
    assert data["sentinel_decision"] in {"allow", "review", "block"}
    assert isinstance(data["risk_score"], (int, float))
    assert isinstance(data["checked_signals"], list) and data["checked_signals"]
    assert isinstance(data["not_checked"], list) and data["not_checked"]
    assert data["payment_lane"] == "basic"
    low = data["disclaimer"].lower()
    assert "not a security guarantee" in low
    assert "not" in low and "execution-quality" in low


def test_fixture_excludes_secrets_and_raw_internals():
    blob = FIXTURE.read_text(encoding="utf-8")
    for pat in _SECRET_PATTERNS:
        assert not pat.search(blob), f"secret pattern {pat.pattern!r} in fixture"
    assert not _RAW_ADDRESS.search(blob), "raw 0x address in fixture"
    data = _load_fixture()
    ref = data["agentkit_result_hash_or_tx_ref"]
    assert ref.startswith("exec_ref:") or ref.startswith("tx_ref:")
    assert "calldata" not in blob.lower()
    assert "private_key" not in blob.lower()


def _assert_no_positive_forbidden(text: str) -> None:
    for phrase in _FORBIDDEN_POSITIVE:
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
            raise AssertionError(f"positive forbidden {phrase!r} in: {line.strip()!r}")


def test_docs_forbidden_positive_claims():
    combined = SPEC.read_text(encoding="utf-8") + PACK.read_text(encoding="utf-8")
    _assert_no_positive_forbidden(combined)


def test_fixture_flags_non_guarantee_boundaries():
    data = _load_fixture()
    assert data.get("notSecurityGuarantee") is True
    assert data.get("partnership_claimed") is False
    assert data.get("integration_claimed") is False
    assert data.get("automatic_settlement_claimed") is False


def test_fixture_post_execution_trail_is_external_evidence():
    data = _load_fixture()
    trail = data.get("post_execution_trail")
    assert trail is not None
    provider = str(trail.get("provider", "")).lower()
    assert "mycelium" in provider
    assert trail.get("trail_ref")
    assert trail.get("signature_scheme") == "ed25519"
    blob = FIXTURE.read_text(encoding="utf-8").lower()
    assert "sentinel-owned" not in blob
    assert "replaces mycelium" not in blob


def test_fixture_reputation_axis_optional_unknown():
    data = _load_fixture()
    rep = data.get("reputation_axis")
    assert rep is not None
    assert rep.get("verdict") == "unknown" or rep.get("unavailable_behavior") == "unknown"
    claims = (REPO / "docs/18_investor/CLAIMS_LEDGER.md").read_text(encoding="utf-8")
    assert "Trust Receipt v0 layer composition" in claims
    assert "does not replace" in claims.lower() or "replacing" in claims.lower()


def test_no_partnership_integration_endorsement_with_mycelium_aura():
    combined = SPEC.read_text(encoding="utf-8") + PACK.read_text(encoding="utf-8")
    for phrase in (
        "official partnership with mycelium",
        "official integration with aura",
        "endorsed by mycelium",
        "replaces mycelium trails protocol",
    ):
        assert phrase not in combined.lower()
