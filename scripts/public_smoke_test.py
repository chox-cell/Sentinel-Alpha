import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env", override=True)

_TIMEOUT_SEC = 8


def _check_endpoint(base_url: str, path: str, expected_status: int, method: str = "GET", json_payload: dict | None = None) -> dict:
    url = f"{base_url}{path}"
    try:
        if method == "POST":
            resp = requests.post(url, json=json_payload, timeout=_TIMEOUT_SEC)
        else:
            resp = requests.get(url, timeout=_TIMEOUT_SEC)
    except requests.RequestException:
        return {"ok": False, "status_code": None}
    return {"ok": resp.status_code == expected_status, "status_code": resp.status_code}


def build_public_smoke_report(public_base_url: str | None = None) -> dict:
    target = (public_base_url or os.getenv("PUBLIC_BASE_URL") or "").strip().rstrip("/")
    if not target:
        return {
            "public_base_url_configured": False,
            "checks": {},
            "smoke_test_verdict": "fail",
            "error": "PUBLIC_BASE_URL is required",
        }

    checks = {
        "GET /health": _check_endpoint(target, "/health", 200),
        "GET /internal/manifest": _check_endpoint(target, "/internal/manifest", 200),
        "GET /internal/x402/status": _check_endpoint(target, "/internal/x402/status", 200),
        "GET /internal/x402/onchain/status": _check_endpoint(target, "/internal/x402/onchain/status", 200),
        "GET /internal/x402/challenge?lane=basic": _check_endpoint(target, "/internal/x402/challenge?lane=basic", 200),
        "POST /contracts/risk-score without payment returns 402": _check_endpoint(
            target,
            "/contracts/risk-score",
            402,
            method="POST",
            json_payload={
                "contract_address": "0x1111111111111111111111111111111111111111",
                "chain": "base",
                "context": {},
            },
        ),
    }
    passed = all(item["ok"] for item in checks.values())
    return {
        "public_base_url_configured": True,
        "checks": checks,
        "smoke_test_verdict": "pass" if passed else "fail",
    }


def format_public_smoke_report(report: dict) -> str:
    lines = ["Sentinel Alpha Public Smoke Test v2.2"]
    lines.append(f"PUBLIC_BASE_URL configured: {str(report['public_base_url_configured']).lower()}")
    if "error" in report:
        lines.append(f"error: {report['error']}")
        lines.append(f"smoke test verdict: {report['smoke_test_verdict']}")
        return "\n".join(lines)

    for name, result in report["checks"].items():
        status = "pass" if result["ok"] else "fail"
        lines.append(f"{name}: {status} (status={result['status_code']})")
    lines.append(f"smoke test verdict: {report['smoke_test_verdict']}")
    return "\n".join(lines)


def main() -> int:
    report = build_public_smoke_report()
    print(format_public_smoke_report(report))
    return 0 if report["smoke_test_verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
