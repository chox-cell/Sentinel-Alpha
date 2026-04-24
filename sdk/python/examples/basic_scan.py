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
