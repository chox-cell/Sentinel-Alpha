#!/usr/bin/env python3
import sys

import requests
from dotenv import load_dotenv


def main() -> int:
    load_dotenv()

    url = "http://127.0.0.1:8000/internal/quicknode-live-check"
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as exc:
        print(f"QuickNode live readiness check failed: {exc}")
        return 1

    if response.status_code != 200:
        print(f"QuickNode live readiness check returned {response.status_code}: {response.text[:300]}")
        return 1

    try:
        body = response.json()
    except ValueError:
        print("QuickNode live readiness check returned non-JSON response.")
        return 1

    ready = bool(body.get("ready_for_live"))
    checks = body.get("checks", {})
    print(f"ready_for_live={ready}")
    print(
        "checks: "
        f"webhook_url_configured={checks.get('webhook_url_configured')} "
        f"webhook_secret_configured={checks.get('webhook_secret_configured')} "
        f"dry_run={checks.get('dry_run')} "
        f"chain={checks.get('chain')}"
    )
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
