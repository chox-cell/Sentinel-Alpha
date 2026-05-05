import hashlib
from pathlib import Path


CHECKLIST_DOC = Path("docs/17_growth/MANUAL_OUTREACH_EXECUTION_CHECKLIST.md")
TRACKER_DOC = Path("docs/17_growth/OUTREACH_TRACKER.md")


def test_checklist_exists_and_core_sections_present():
    assert CHECKLIST_DOC.exists()
    text = CHECKLIST_DOC.read_text(encoding="utf-8").lower()
    assert "pre-send checklist" in text
    assert "approved evidence" in text
    assert "human founder sends manually" in text
    assert "status can change from not contacted to contacted only after actual send" in text
    assert "never use integrated unless pr merged or public proof exists" in text
    assert "one polite follow-up max" in text


def test_checklist_includes_approved_evidence_items():
    text = CHECKLIST_DOC.read_text(encoding="utf-8")
    assert "@beezshield/sentinel" in text
    assert "npm install @beezshield/sentinel" in text
    assert "/contracts/risk-score" in text
    assert "AgentKit-style example available" in text
    assert "official provider coming next" in text
    assert "8 fixtures / 8 passed / 0 review" in text
    assert "not a security guarantee" in text


def test_forbidden_phrases_absent_in_positive_claim_context():
    lower = CHECKLIST_DOC.read_text(encoding="utf-8").lower()
    forbidden = [
        "guaranteed protection is provided",
        "claims it detects honeypots",
        "claims it prevents mev",
        "live simulation is enabled",
        "claims full contract coverage",
        "agentkit provider is live",
        "official agentkit integration is live",
        "you are vulnerable to",
        "this project was exploited",
    ]
    for phrase in forbidden:
        assert phrase not in lower


def test_outreach_tracker_has_no_contacted_or_integrated_status_rows():
    tracker = TRACKER_DOC.read_text(encoding="utf-8").lower()
    assert "| contacted |" not in tracker
    assert "| integrated |" not in tracker


def test_env_unchanged_during_manual_outreach_checklist_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = CHECKLIST_DOC.read_text(encoding="utf-8")
    _ = TRACKER_DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
