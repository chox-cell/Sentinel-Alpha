import hashlib
import json
import subprocess
import sys
from pathlib import Path


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/run_fixture_evaluation.py", *args],
        cwd=Path("."),
        capture_output=True,
        text=True,
        check=True,
    )


def test_cli_json_output_parses_and_has_expected_fields():
    proc = _run_cli("--format", "json")
    report = json.loads(proc.stdout)
    assert report["report_type"] == "fixture_evaluation"
    assert report["total_fixtures"] == 8
    assert report["passed"] == 8
    assert report["review"] == 0
    assert "not a security guarantee" in report["disclaimer"].lower()


def test_cli_markdown_output_includes_title_and_summary():
    proc = _run_cli("--format", "markdown")
    text = proc.stdout
    assert "# Fixture Evaluation Report" in text
    assert "| Total fixtures | 8 |" in text
    assert "| Passed | 8 |" in text
    assert "| Review | 0 |" in text


def test_cli_output_writes_to_tmp_path_only(tmp_path):
    output = tmp_path / "fixture-report.json"
    proc = _run_cli("--format", "json", "--output", str(output))
    assert proc.stdout.strip() == ""
    assert output.exists()
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["report_type"] == "fixture_evaluation"


def test_cli_output_has_no_forbidden_claims():
    proc = _run_cli("--format", "json")
    text = proc.stdout.lower()
    assert "honeypot detection" not in text
    assert "malicious certainty" not in text
    assert "guaranteed protection" not in text


def test_env_unchanged_during_cli_runs():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _run_cli("--format", "json")
    _run_cli("--format", "markdown")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
