import requests

def check_contract(base_url: str, contract_address: str, chain: str = "base"):
    res = requests.post(
        f"{base_url}/contracts/risk-score",
        json={"contract_address": contract_address, "chain": chain},
        headers={"PAYMENT-SIGNATURE": "demo"},
        timeout=15,
    )

    try:
        return {
            "status_code": res.status_code,
            "json": res.json(),
        }
    except Exception:
        return {
            "status_code": res.status_code,
            "raw": res.text[:500],
        }

if __name__ == "__main__":
    print(check_contract("http://127.0.0.1:8000", "0x123"))
