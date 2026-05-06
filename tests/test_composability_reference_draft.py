import hashlib
from pathlib import Path


DOC = Path("docs/17_growth/COMPOSABILITY_REFERENCE_DRAFT.md")


def test_composability_doc_exists_and_required_content():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    lower = text.lower()
    assert "Sentinel pre-check" in text
    assert "x402 payment authorization" in lower
    assert "AgentKit action" in text
    assert "post-action trail record" in lower
    assert "Audit independence" in text
    assert "notSecurityGuarantee" in text
    assert "sample-output.json" in text
    for field in ["agent_id", "action", "payment_hash", "claims", "timestamp", "signature"]:
        assert field in text
    assert "No partnership claim" in text or "no partnership claim" in lower
    assert "no official integration claim" in lower


def test_forbidden_phrases_absent():
    lower = DOC.read_text(encoding="utf-8").lower()
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
        assert token not in lower


def test_env_unchanged_during_composability_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
