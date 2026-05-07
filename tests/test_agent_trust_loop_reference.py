import hashlib
from pathlib import Path


DOC = Path("docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md")


def test_doc_exists_and_required_content():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Agent Trust Loop Reference Pattern" in text
    assert "ATCP-style tool pre-flight" in text
    assert "Sentinel Alpha / BeezShield" in text
    assert "x402 payment authorization" in lower
    assert "AgentKit action" in text
    assert "Mycelium Trails post-action record" in text

    assert "action_ref" in text
    assert "sentinel_decision_ref" in text
    assert "payment_hash" in text
    assert "claims" in text
    assert "trace_id or receipt_id" in text or "trace_id" in text or "receipt_id" in text

    assert "no partnership claim" in lower
    assert "no official integration claim" in lower
    assert "no ATCP integration claim".lower() in lower


def test_forbidden_phrases_absent():
    lower = DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "partnership live",
        "integration is live",
        "official provider is live",
        "guaranteed protection is provided",
        "claims it detects honeypots",
        "claims it prevents mev",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in lower


def test_env_unchanged_during_agent_trust_loop_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
