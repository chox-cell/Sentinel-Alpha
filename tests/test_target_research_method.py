"""Growth docs: target research prep (v4.4) copy and tracker honesty."""

import re
from pathlib import Path

METHOD = Path("docs/17_growth/TARGET_RESEARCH_METHOD.md")
TARGETS = Path("docs/17_growth/FIRST_20_BUILDER_TARGETS.md")
TRACKER = Path("docs/17_growth/OUTREACH_TRACKER.md")
RESEARCH_FILES = [METHOD, TARGETS]


def _merged_research_docs() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in RESEARCH_FILES)


def test_target_research_files_exist():
    for p in RESEARCH_FILES:
        assert p.exists(), f"missing file: {p}"
    assert TRACKER.exists(), "OUTREACH_TRACKER.md required for placeholder status checks"


def test_source_verification_required_mentioned():
    merged = _merged_research_docs().lower()
    assert "source verification required" in merged


def test_scoring_criteria_present():
    merged = _merged_research_docs().lower()
    assert "+1" in merged
    assert "uses base" in merged


def test_target_research_required_product_copy():
    merged = _merged_research_docs().lower()
    for token in (
        "@beezshield/sentinel",
        "agentkit-style example",
        "official provider coming next",
    ):
        assert token in merged


def test_target_research_no_forbidden_claims():
    merged = _merged_research_docs().lower()
    forbidden = [
        "agentkit provider live",
        "guaranteed protection",
        "automatic x402 settlement",
    ]
    for token in forbidden:
        assert token not in merged


def test_tracker_no_fake_contacted_or_integrated_for_placeholders():
    """T01–T20 must remain not contacted until real outreach; no fake integrated."""
    tracker = TRACKER.read_text(encoding="utf-8")
    rows = []
    for line in tracker.splitlines():
        m = re.match(r"^\|\s*(T(?:0[1-9]|1[0-9]|20))\s*\|", line)
        if not m:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 10:
            continue
        rows.append((parts[1], parts[8]))
    assert len(rows) == 20
    for _tid, status in rows:
        assert status == "not contacted"
        assert status != "integrated"
