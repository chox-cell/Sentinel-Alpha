import hashlib
from pathlib import Path


DRAFTS_DOC = Path("docs/17_growth/OUTREACH_MESSAGE_DRAFTS_BATCH_1.md")
TRACKER_DOC = Path("docs/17_growth/OUTREACH_TRACKER.md")


def test_drafts_file_exists_and_contains_targets():
    assert DRAFTS_DOC.exists()
    text = DRAFTS_DOC.read_text(encoding="utf-8")
    targets = [
        "Coinbase AgentKit",
        "Coinbase x402",
        "Zora Developer Docs",
        "modelcontextprotocol/servers",
        "Safe Core SDK",
        "Coinbase OnchainKit",
        "elizaOS/eliza",
    ]
    for target in targets:
        assert target in text


def test_drafts_include_required_evidence_lines():
    text = DRAFTS_DOC.read_text(encoding="utf-8")
    lower = text.lower()
    assert "source_url:" in lower
    assert "agentkit-style example" in lower
    assert "official provider coming next" in lower
    assert "@beezshield/sentinel" in text
    assert "npm install @beezshield/sentinel" in text
    assert "8 fixtures / 8 passed / 0 review" in lower
    assert "not a security guarantee" in lower
    assert "status: not contacted" in lower


def test_drafts_avoid_forbidden_phrases():
    lower = DRAFTS_DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "guaranteed protection is provided",
        "claims it detects honeypots",
        "claims it prevents mev",
        "live simulation is enabled",
        "claims full contract coverage",
        "agentkit provider is live",
        "official agentkit integration is live",
        "you are vulnerable to",
        "exploited",
    ]
    for phrase in forbidden:
        assert phrase not in lower


def test_tracker_has_no_integrated_or_contacted_marks():
    tracker = TRACKER_DOC.read_text(encoding="utf-8").lower()
    assert "| integrated |" not in tracker
    assert "| contacted |" not in tracker


def test_env_unchanged_during_draft_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DRAFTS_DOC.read_text(encoding="utf-8")
    _ = TRACKER_DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
