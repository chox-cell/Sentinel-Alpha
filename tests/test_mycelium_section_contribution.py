import hashlib
from pathlib import Path


TRUST_LOOP_DOC = Path("docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md")
COMPOSABILITY_DOC = Path("docs/17_growth/COMPOSABILITY_REFERENCE_DRAFT.md")
OUTREACH_TRACKER = Path("docs/17_growth/OUTREACH_TRACKER.md")


def test_mycelium_section_exists_with_required_content():
    assert TRUST_LOOP_DOC.exists()
    text = TRUST_LOOP_DOC.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Mycelium Trails-style Post-Action Section — External Community Contribution" in text
    assert "giskard09" in text
    assert "external/community section, not a Sentinel dependency".lower() in lower
    assert "not official integration or partnership".lower() in lower

    for field in [
        "trail_id",
        "agent_id",
        "action_ref",
        "payment_hash",
        "service",
        "operation",
        "success",
        "timestamp",
        "\"chain_id\": 42161",
        "\"chain_id\": 8453",
    ]:
        assert field in text

    assert "SHA-256(agent_id:action_type:scope:timestamp)" in text
    assert "https://argentum.rgiskard.xyz/trails/verify?payment_hash=<hex>" in text
    assert "no partnership claim" in lower
    assert "no official integration claim" in lower
    assert "no stripe/coinbase/x402-foundation affiliation claim" in lower
    assert "not audited; community-built infrastructure" in lower
    assert "composability pattern only" in lower


def test_composability_doc_references_contributed_section():
    text = COMPOSABILITY_DOC.read_text(encoding="utf-8")
    lower = text.lower()
    assert "Mycelium Trails-style Post-Action Section — External Community Contribution" in text
    assert "documentation-only composability guidance" in lower
    assert "no partnership or official integration claim" in lower


def test_outreach_tracker_records_concrete_content_received():
    text = OUTREACH_TRACKER.read_text(encoding="utf-8")
    lower = text.lower()
    assert "concrete_mycelium_section_content_received" in text
    assert "section_target_doc: docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md" in text
    assert "SHA-256(agent_id:action_type:scope:timestamp)" in text
    assert "https://argentum.rgiskard.xyz/trails/verify?payment_hash=<hex>" in text
    assert "not official integration" in lower
    assert "not partnership" in lower


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            TRUST_LOOP_DOC.read_text(encoding="utf-8"),
            COMPOSABILITY_DOC.read_text(encoding="utf-8"),
            OUTREACH_TRACKER.read_text(encoding="utf-8"),
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


def test_env_unchanged_during_mycelium_contribution_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = TRUST_LOOP_DOC.read_text(encoding="utf-8")
    _ = OUTREACH_TRACKER.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
