from pathlib import Path


PACKS = [
    Path("docs/17_growth/PR_DRAFT_PACK_X402.md"),
    Path("docs/17_growth/PR_DRAFT_PACK_AGENTKIT.md"),
    Path("docs/17_growth/PR_DRAFT_PACK_ELIZA.md"),
]

TRACKER_DOC = Path("docs/17_growth/OUTREACH_TRACKER.md")


def test_pr_draft_pack_files_exist():
    for pack in PACKS:
        assert pack.exists(), f"missing {pack}"


def test_pr_draft_packs_have_required_sections_and_wording():
    required_tokens = [
        "Purpose",
        "Target issue URL",
        "Proposed tiny change",
        "Example code snippet using @beezshield/sentinel",
        "README/docs snippet",
        "Safety wording",
        "Non-goals",
        "Exact files that would be changed in upstream if approved",
        "Not submitted yet",
        "optional example",
        "pre-execution risk decision",
        "allow / review / block",
        "AgentKit-style example available",
        "official provider coming next",
        "regression evidence only, not a security guarantee",
        "npm install @beezshield/sentinel",
    ]
    for pack in PACKS:
        text = pack.read_text(encoding="utf-8")
        lower = text.lower()
        for token in required_tokens:
            assert token.lower() in lower, f"{token} missing in {pack}"


def test_pr_draft_packs_avoid_forbidden_claims():
    forbidden = [
        "integration is live",
        "provider is live",
        "claims it detects honeypots",
        "claims it prevents mev",
        "guaranteed protection is provided",
        "live simulation is enabled",
        "claims full contract coverage",
    ]
    for pack in PACKS:
        lower = pack.read_text(encoding="utf-8").lower()
        for token in forbidden:
            assert token not in lower, f"{token} unexpectedly present in {pack}"


def test_tracker_has_no_integrated_status():
    text = TRACKER_DOC.read_text(encoding="utf-8").lower()
    assert "| integrated |" not in text
