from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from services.scanner_engine.evaluation_harness import (
    evaluate_fixture_dataset,
    load_base_fixture_dataset,
    summarize_evaluation_results,
)


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_report(fixtures_path: str | None = None) -> dict:
    fixtures = load_base_fixture_dataset(path=fixtures_path)
    results = evaluate_fixture_dataset(fixtures)
    summary = summarize_evaluation_results(results)
    return {
        "report_type": "fixture_evaluation",
        "version": "v6.6.2",
        "generated_at": _iso_now(),
        "total_fixtures": summary["total_fixtures"],
        "passed": summary["passed"],
        "review": summary["review"],
        "coverage_by_fixture_type": summary["coverage_by_fixture_type"],
        "results": results,
        "disclaimer": "Local regression evaluation only; not a security guarantee.",
    }


def _to_markdown(report: dict) -> str:
    lines = [
        "# Fixture Evaluation Report",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total fixtures | {report['total_fixtures']} |",
        f"| Passed | {report['passed']} |",
        f"| Review | {report['review']} |",
        "",
        "## Fixture Results",
        "",
        "| Fixture | Type | Status | Matched | Missing |",
        "|---|---|---|---:|---:|",
    ]
    for row in report["results"]:
        lines.append(
            f"| {row.get('fixture_name')} | {row.get('fixture_type')} | {row.get('evaluation_status')} | "
            f"{len(row.get('matched_signals', []))} | {len(row.get('missing_expected_signals', []))} |"
        )

    missing = {
        row.get("fixture_name"): row.get("missing_expected_signals", [])
        for row in report["results"]
        if row.get("missing_expected_signals")
    }
    lines.extend(["", "## Missing Expected Signals", ""])
    if missing:
        for fixture_name, missing_signals in missing.items():
            lines.append(f"- `{fixture_name}`: {', '.join(missing_signals)}")
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Disclaimer",
            "",
            "Local regression evaluation only; not a security guarantee.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local fixture evaluation harness report.")
    parser.add_argument("--fixtures-path", default=None, help="Optional fixture directory path.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", default=None, help="Optional output path for report.")
    args = parser.parse_args()

    report = _build_report(args.fixtures_path)
    output_text = json.dumps(report, indent=2) if args.format == "json" else _to_markdown(report)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")
    else:
        print(output_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
