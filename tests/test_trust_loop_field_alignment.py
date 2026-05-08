import hashlib
from pathlib import Path


ALIGNMENT_DOC = Path("docs/17_growth/TRUST_LOOP_FIELD_ALIGNMENT_V1.md")
TRUST_LOOP_DOC = Path("docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md")
COMPOSABILITY_DOC = Path("docs/17_growth/COMPOSABILITY_REFERENCE_DRAFT.md")
REPORT_MD = Path("reports/trust_loop/minimum_verifiable_loop.sample.md")


def test_alignment_doc_exists_and_has_required_fields():
    assert ALIGNMENT_DOC.exists()
    text = ALIGNMENT_DOC.read_text(encoding="utf-8")
    lower = text.lower()

    for field in [
        "trace_id",
        "receipt_id",
        "action_ref",
        "sentinel_decision_ref",
        "payment_decision_link_ref",
        "payment_hash",
        "contract_address_hash",
        "decision_action",
        "confidence",
        "notSecurityGuarantee",
        "trail_id",
        "agent_id",
        "service",
        "operation",
        "success",
        "anchors.arbitrum.tx_hash",
        "anchors.base.tx_hash",
        "claims",
    ]:
        assert field in text

    for layer in [
        "ATCP-style tool pre-flight",
        "Sentinel Alpha / BeezShield",
        "x402 / Lightning payment context",
        "AgentKit-style execution",
        "Mycelium Trails-style post-action record",
    ]:
        assert layer in text

    assert "safe_to_store" in lower
    assert "raw_secret_allowed" in lower
    assert "integration_status" in lower
    assert "no private keys" in lower
    assert "no seed phrases" in lower
    assert "no raw auth headers" in lower
    assert "no live integration" in lower
    assert "no partnership claim" in lower


def test_docs_link_field_alignment():
    trust = TRUST_LOOP_DOC.read_text(encoding="utf-8")
    report = REPORT_MD.read_text(encoding="utf-8")
    composability = COMPOSABILITY_DOC.read_text(encoding="utf-8")
    assert "TRUST_LOOP_FIELD_ALIGNMENT_V1.md" in trust
    assert "TRUST_LOOP_FIELD_ALIGNMENT_V1.md" in report
    assert "TRUST_LOOP_FIELD_ALIGNMENT_V1.md" in composability


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            ALIGNMENT_DOC.read_text(encoding="utf-8"),
            TRUST_LOOP_DOC.read_text(encoding="utf-8"),
            COMPOSABILITY_DOC.read_text(encoding="utf-8"),
            REPORT_MD.read_text(encoding="utf-8"),
        ]
    ).lower()

    forbidden = [
        "partnership live",
        "integration is live and active",
        "official provider is live",
        "guaranteed protection is provided",
        "claims it detects honeypots",
        "claims it prevents mev",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in combined


def test_env_unchanged_during_alignment_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = ALIGNMENT_DOC.read_text(encoding="utf-8")
    _ = TRUST_LOOP_DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
