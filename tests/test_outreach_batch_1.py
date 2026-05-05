import hashlib
from pathlib import Path


BATCH_DOC = Path("docs/17_growth/OUTREACH_BATCH_1.md")
TRACKER_DOC = Path("docs/17_growth/OUTREACH_TRACKER.md")


def test_outreach_batch_doc_exists_and_required_content():
    assert BATCH_DOC.exists()
    text = BATCH_DOC.read_text(encoding="utf-8")
    lower = text.lower()
    assert "@beezshield/sentinel" in text
    assert "npm install @beezshield/sentinel" in text
    assert "AgentKit-style example" in text
    assert "official provider coming next" in lower
    assert "8 fixtures / 8 passed / 0 review" in lower
    assert "not a security guarantee" in lower
    assert "guardians, not traders" in lower


def test_outreach_batch_doc_avoids_forbidden_phrases():
    lower = BATCH_DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "guaranteed protection",
        "claims it detects honeypots",
        "claims it prevents mev",
        "agentkit provider is live",
        "official agentkit integration is live",
        "live simulation is enabled",
        "claims full contract coverage",
        "status: contacted",
        "status: integrated",
    ]
    for phrase in forbidden:
        assert phrase not in lower


def test_tracker_does_not_fake_contacted_or_integrated_statuses():
    assert TRACKER_DOC.exists()
    text = TRACKER_DOC.read_text(encoding="utf-8").lower()
    assert "| contacted |" not in text
    assert "| integrated |" not in text


def test_env_unchanged_during_outreach_batch_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = BATCH_DOC.read_text(encoding="utf-8")
    _ = TRACKER_DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
