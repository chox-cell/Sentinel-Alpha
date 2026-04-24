import sys
from pathlib import Path

# Allow direct execution: python sdk/python/examples/basic_scan.py
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from sdk.python.client import SentinelAlphaClient


def main():
    client = SentinelAlphaClient(base_url="http://127.0.0.1:8000", payment_signature="demo")
    result = client.risk_score(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
        context={"event_type": "new_deploy"},
    )
    print(result)


if __name__ == "__main__":
    main()
