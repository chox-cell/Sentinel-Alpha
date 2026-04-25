from sdk.python.client import SentinelAlphaClient


def main():
    client = SentinelAlphaClient(
        base_url="http://localhost:8000",
        payment_header="tx:0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    result = client.scan(
        contract_address="0x1111111111111111111111111111111111111111",
        chain="base",
    )
    print(result)


if __name__ == "__main__":
    main()
