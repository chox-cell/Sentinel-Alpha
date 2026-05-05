import hashlib
from pathlib import Path


PACK_DOC = Path("docs/17_growth/OUTREACH_TARGET_VERIFICATION_PACK.md")
TRACKER_DOC = Path("docs/17_growth/OUTREACH_TRACKER.md")


def _table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if line.startswith("| T"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def test_verified_research_has_minimum_real_targets_or_explains_why():
    text = PACK_DOC.read_text(encoding="utf-8")
    rows = _table_rows(text)
    real_rows = [r for r in rows if len(r) >= 3 and r[2].startswith("http")]
    assert len(real_rows) >= 5 or "fewer than 5" in text.lower()


def test_each_real_target_has_source_url_and_not_contacted_status():
    rows = _table_rows(PACK_DOC.read_text(encoding="utf-8"))
    real_rows = [r for r in rows if len(r) >= 9 and r[2].startswith("http")]
    assert real_rows
    for row in real_rows:
        source_url = row[2]
        status = row[8].lower()
        assert source_url.startswith("http")
        assert status == "not contacted"


def test_no_contacted_or_integrated_status_claims_for_real_targets():
    rows = _table_rows(PACK_DOC.read_text(encoding="utf-8"))
    real_rows = [r for r in rows if len(r) >= 9 and r[2].startswith("http")]
    for row in real_rows:
        status = row[8].lower()
        assert status != "contacted"
        assert status != "integrated"


def test_required_categories_represented_where_possible():
    text = PACK_DOC.read_text(encoding="utf-8")
    categories = [
        "AgentKit/Base builders",
        "MCP tool servers on Base",
        "x402 builders",
        "Zora/Base asset tools",
        "wallet automation projects",
        "security-minded bot builders",
    ]
    present = [c for c in categories if c in text]
    assert len(present) >= 5


def test_safe_messaging_and_forbidden_phrases():
    text = PACK_DOC.read_text(encoding="utf-8")
    lower = text.lower()
    assert "agentkit-style example" in lower
    assert "official provider coming next" in lower
    assert "regression evidence only" in lower
    forbidden = [
        "guaranteed protection",
        "detects honeypots",
        "prevents mev",
        "live simulation is enabled",
        "agentkit provider live",
        "official agentkit integration live",
        "full contract coverage",
    ]
    for phrase in forbidden:
        assert phrase not in lower


def test_tracker_still_not_contacted_and_not_integrated():
    tracker = TRACKER_DOC.read_text(encoding="utf-8").lower()
    assert "not contacted" in tracker
    assert "| integrated |" not in tracker


def test_env_unchanged_during_verified_research_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = PACK_DOC.read_text(encoding="utf-8")
    _ = TRACKER_DOC.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
