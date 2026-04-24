import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SENTINEL_BASE_URL", "http://127.0.0.1:8000")
PAYMENT_SIGNATURE = os.getenv("PAYMENT_DEMO_SIGNATURE", "demo")

TEST_CASES = [
    {
        "contract_address": "0x0000000000000000000000000000000000000000",
        "chain": "base",
        "context": {"event_type": "new_deploy"},
    },
    {
        "contract_address": "0x123",
        "chain": "base",
        "context": {"event_type": "new_deploy"},
    },
    {
        "contract_address": "0x1111111111111111111111111111111111111111",
        "chain": "base",
        "context": {
            "event_type": "first_liquidity",
            "liquidity_unlocked": True,
            "bad_cluster": True,
        },
    },
    {
        "contract_address": "0x2222222222222222222222222222222222222222",
        "chain": "base",
        "context": {
            "event_type": "new_deploy",
            "oracle_dislocation": True,
            "simulation_revert": True,
        },
    },
]

while True:
    for payload in TEST_CASES:
        res = requests.post(
            f"{BASE_URL}/contracts/risk-score",
            json=payload,
            headers={"PAYMENT-SIGNATURE": PAYMENT_SIGNATURE},
            timeout=15,
        )

        print("STATUS:", res.status_code)
        print("RAW:", res.text[:500])

        try:
            print("JSON:", res.json())
        except Exception:
            print("NOT JSON RESPONSE")

        print("------")
        time.sleep(1)
