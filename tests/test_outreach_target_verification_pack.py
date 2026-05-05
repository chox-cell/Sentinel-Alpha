import hashlib
from pathlib import Path


PACK_DOC = Path("docs/17_growth/OUTREACH_TARGET_VERIFICATION_PACK.md")
TRACKER_DOC = Path("docs/17_growth/OUTREACH_TRACKER.md")


def test_verification_pack_exists_and_required_fields_present():
    assert PACK_DOC.exists()
    text = PACK_DOC.read_text(encoding="utf-8")
    lower = text.lower()
    assert "target_id" in lower
    assert "source_url" in lower
    assert "evidence_observed" in lower
    assert "status: not contacted" in lower
    assert "agentkit-style example" in lower
    assert "official provider coming next" in lower
    assert "local fixture evaluation as regression evidence only" in lower
    assert "no target without source_url" in lower


def test_verification_pack_contains_required_categories():
    text = PACK_DOC.read_text(encoding="utf-8")
    required_categories = [
        "AgentKit/Base builders",
        "MCP trading/tool servers on Base",
        "x402 builders",
        "Zora/Base asset tools",
        "wallet automation projects",
        "security-minded bot builders",
    ]
    for category in required_categories:
        assert category in text


def test_verification_pack_avoids_forbidden_overclaims():
    lower = PACK_DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "guaranteed protection",
        "detects honeypots",
        "prevents mev",
        "live simulation is enabled",
        "agentkit provider live",
        "official agentkit integration live",
        "full contract coverage",
        "status: contacted",
        "status: integrated",
    ]
    for phrase in forbidden:
        assert phrase not in lower


def test_tracker_remains_not_contacted_and_not_integrated():
    assert TRACKER_DOC.exists()
    tracker = TRACKER_DOC.read_text(encoding="utf-8").lower()
    assert "not contacted" in tracker
    assert "| integrated |" not in tracker


def test_env_unchanged_during_verification_pack_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK_DOC.read_text(encoding="utf-8")
    _ = TRACKER_DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
