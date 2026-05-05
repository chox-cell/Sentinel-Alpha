import hashlib
import json
from pathlib import Path


JSON_REPORT = Path("reports/fixture_evaluation/latest.json")
MD_REPORT = Path("reports/fixture_evaluation/latest.md")


def test_report_artifact_files_exist():
    assert JSON_REPORT.exists()
    assert MD_REPORT.exists()


def test_json_report_parses_and_has_expected_summary():
    report = json.loads(JSON_REPORT.read_text(encoding="utf-8"))
    assert report["report_type"] == "fixture_evaluation"
    assert report["total_fixtures"] == 8
    assert report["passed"] == 8
    assert report["review"] == 0
    assert "not a security guarantee" in str(report.get("disclaimer", "")).lower()
    assert isinstance(report.get("results"), list) and len(report["results"]) == 8


def test_markdown_report_includes_required_sections():
    text = MD_REPORT.read_text(encoding="utf-8")
    assert "Local Fixture Evaluation" in text
    assert "| Metric | Value |" in text
    assert "## Fixture Results" in text
    assert "## Disclaimer" in text


def test_reports_have_no_forbidden_claims():
    text = (JSON_REPORT.read_text(encoding="utf-8") + "\n" + MD_REPORT.read_text(encoding="utf-8")).lower()
    assert "honeypot detection" not in text
    assert "malicious certainty" not in text
    assert "guaranteed protection" not in text
    assert "full contract coverage" not in text


def test_env_unchanged_during_artifact_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = JSON_REPORT.read_text(encoding="utf-8")
    _ = MD_REPORT.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
