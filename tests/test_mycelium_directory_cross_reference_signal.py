import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "docs/17_growth/X402_DIRECTORY_SUBMISSION_PACK.md"
OUTREACH = REPO_ROOT / "docs/17_growth/OUTREACH_TRACKER.md"
PRE_POST = REPO_ROOT / "docs/17_growth/PRE_POST_LOOP_REFERENCE_PATTERN.md"
CLAIMS = REPO_ROOT / "docs/18_investor/CLAIMS_LEDGER.md"


def test_submission_pack_mycelium_cross_reference():
    text = PACK.read_text(encoding="utf-8")
    low = text.lower()

    assert "mycelium trails" in low
    assert "adjacent community project" in low
    assert "post-execution accountability" in low or "post-execution" in low
    assert "pre-execution" in low
    assert "cross-reference" in low
    assert "both" in low and "live" in low
    assert "no partnership" in low
    assert "no official integration" in low
    assert "no endorsement" in low
    assert "no shared runtime dependency" in low


def test_outreach_giskard09_signal():
    ot = OUTREACH.read_text(encoding="utf-8").lower()
    assert "giskard09" in ot
    assert "mycelium" in ot
    assert "same" in ot
    assert "cross-reference" in ot
    assert "community alignment signal" in ot
    assert "no partnership" in ot
    assert "no integration" in ot or "integration_claim: false" in ot


def test_claims_mycelium_cross_reference_row():
    cl = CLAIMS.read_text(encoding="utf-8").lower()
    assert "mycelium directory cross-reference signal" in cl
    assert "community signal" in cl
    assert "future possible cross-reference" in cl
    assert "no partnership" in cl


def test_directory_targets_still_not_submitted():
    ot = OUTREACH.read_text(encoding="utf-8")
    # x402scan registered; Agentic.Market rejected_needs_fix; Pay.sh + ampersend not submitted
    assert "rejected_needs_fix" in ot
    assert ot.count("| not submitted |") >= 2


def test_pre_post_mentions_future_directory_copy():
    pp = PRE_POST.read_text(encoding="utf-8").lower()
    assert "directory" in pp
    assert "pre/post" in pp or "pre/post" in pp.replace(" ", "")
    assert "documentation-only" in pp or "composability" in pp


def test_forbid_unsafe_positive_phrases_in_signal_surfaces():
    outreach_full = OUTREACH.read_text(encoding="utf-8")
    start = outreach_full.lower().find("## giskard09")
    assert start != -1
    giskard_section = outreach_full[start:]

    claim_lines = [
        ln
        for ln in CLAIMS.read_text(encoding="utf-8").splitlines()
        if "mycelium directory cross-reference signal" in ln.lower()
    ]
    assert len(claim_lines) == 1
    claim_row = claim_lines[0]

    combined = (
        giskard_section.lower()
        + PRE_POST.read_text(encoding="utf-8").lower()
        + claim_row.lower()
    )
    forbidden = [
        "partnership live",
        "official integration",
        "shared runtime dependency",
        "submitted to all directories",
        "guaranteed protection",
        "detects honeypots",
        "prevents mev",
        "prevents prompt injection",
    ]
    for phrase in forbidden:
        assert phrase not in combined, phrase


def test_env_unchanged_during_mycelium_signal_tests():
    env_path = REPO_ROOT / ".env"
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"

    _ = PACK.read_bytes()
    _ = OUTREACH.read_text(encoding="utf-8")
    _ = PRE_POST.read_text(encoding="utf-8")
    _ = CLAIMS.read_text(encoding="utf-8")

    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
