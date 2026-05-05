from pathlib import Path


PLAN = Path("docs/16_launch/COST_DISCIPLINE_PLAN.md")
ROADMAP = Path("docs/16_launch/SENTINEL_RISK_ENGINE_V5_ROADMAP.md")


def test_cost_discipline_docs_exist():
    assert PLAN.exists(), f"missing {PLAN}"
    assert ROADMAP.exists(), f"missing {ROADMAP}"


def test_cost_discipline_plan_required_content():
    text = PLAN.read_text(encoding="utf-8").lower()
    required = [
        "<= $10",
        "contabo",
        "quicknode",
        "avoid paid",
        "postgres",
        "managed db",
        "redis",
        "simulation",
        "no paid provider until demand",
        "do not store secrets",
    ]
    for token in required:
        assert token in text
    assert "enable paid quicknode by default" not in text


def test_roadmap_has_cost_notes():
    text = ROADMAP.read_text(encoding="utf-8").lower()
    required = [
        "v5.5 simulation adapter",
        "no paid provider until demand",
        "may require rpc budget",
    ]
    for token in required:
        assert token in text
