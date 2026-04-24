#!/usr/bin/env python3
import hashlib
import hmac
import json
import os

import requests
from dotenv import load_dotenv


def _build_headers(raw_body: bytes) -> dict:
    headers = {"content-type": "application/json"}
    secret = (os.getenv("QUICKNODE_WEBHOOK_SECRET") or "").strip()
    if secret:
        signature = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
        headers["x-qn-signature"] = signature
    return headers


def main() -> int:
    load_dotenv()
    webhook_url = (os.getenv("QUICKNODE_WEBHOOK_URL") or "").strip()
    if not webhook_url:
        print("QUICKNODE_WEBHOOK_URL is not configured.")
        return 1

    payload = {
        "contract_address": "0x1111111111111111111111111111111111111111",
        "chain": os.getenv("QUICKNODE_CHAIN", "base"),
        "event_type": "new_deploy",
    }
    raw_body = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    try:
        response = requests.post(
            webhook_url,
            data=raw_body,
            headers=_build_headers(raw_body),
            timeout=20,
        )
    except requests.RequestException as exc:
        print(f"Public webhook test failed: {exc}")
        return 1

    print(f"status={response.status_code}")
    print(response.text[:500])
    return 0 if response.status_code == 200 else 1


if __name__ == "__main__":
    raise SystemExit(main())
