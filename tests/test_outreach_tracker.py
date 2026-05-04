"""Growth docs: outreach execution tracker copy and placeholder honesty."""

import re
from pathlib import Path

TRACKER = Path("docs/17_growth/OUTREACH_TRACKER.md")
TARGETS = Path("docs/17_growth/FIRST_20_BUILDER_TARGETS.md")
RULES = Path("docs/17_growth/OUTREACH_OPERATING_RULES.md")
FILES = [TRACKER, TARGETS, RULES]


def _merged() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in FILES)


def test_outreach_growth_files_exist():
    for p in FILES:
        assert p.exists(), f"missing file: {p}"


def test_tracker_has_t01_and_t20():
    text = TRACKER.read_text(encoding="utf-8")
    assert "| T01 |" in text
    assert "| T20 |" in text


def test_tracker_status_allowed_values_mentioned():
    text = TRACKER.read_text(encoding="utf-8").lower()
    for status in (
        "not contacted",
        "contacted",
        "replied",
        "interested",
        "rejected",
        "integrated",
    ):
        assert status in text


def test_outreach_required_copy():
    merged = _merged().lower()
    required = [
        "@beezshield/sentinel",
        "npm install @beezshield/sentinel",
        "agentkit-style example",
        "official provider coming next",
    ]
    for token in required:
        assert token in merged


def test_outreach_no_overclaim_phrases():
    merged = _merged().lower()
    forbidden = [
        "agentkit provider live",
        "guaranteed protection",
        "automatic x402 settlement",
    ]
    for token in forbidden:
        assert token not in merged


def test_placeholder_rows_not_integrated():
    """Placeholder T01–T20 must not claim integrated; status column stays not contacted."""
    tracker = TRACKER.read_text(encoding="utf-8")
    rows = []
    for line in tracker.splitlines():
        m = re.match(r"^\|\s*(T(?:0[1-9]|1[0-9]|20))\s*\|", line)
        if not m:
            continue
        parts = [p.strip() for p in line.split("|")]
        # leading/trailing empty from split
        if len(parts) < 10:
            continue
        rows.append((parts[1], parts[8]))  # ID, Status
    assert len(rows) == 20
    for tid, status in rows:
        assert tid in {f"T{i:02d}" for i in range(1, 21)}
        assert status == "not contacted"
        assert status != "integrated"
