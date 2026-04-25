import requests
from typing import Any


class SentinelAlphaClient:
    def __init__(
        self,
        base_url: str,
        payment_header: str | None = None,
        payment_signature: str = "demo",
    ):
        self.base_url = base_url.rstrip("/")
        self.payment_header = payment_header
        self.payment_signature = payment_signature

    def _request(self, method: str, path: str, *, json_payload: dict | None = None, timeout: int = 15) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        if self.payment_header:
            headers = {"X402-PAYMENT": self.payment_header}
        else:
            headers = {"PAYMENT-SIGNATURE": self.payment_signature}

        try:
            response = requests.request(
                method=method,
                url=url,
                json=json_payload,
                headers=headers,
                timeout=timeout,
            )
        except requests.Timeout as exc:
            raise RuntimeError(f"Request timeout for {method} {path}") from exc
        except requests.RequestException as exc:
            raise RuntimeError(f"Request failed for {method} {path}: {exc}") from exc

        if response.status_code != 200:
            raise RuntimeError(
                f"Non-200 response for {method} {path}: {response.status_code} {response.text[:300]}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError(f"Non-JSON response for {method} {path}") from exc

    def scan(self, contract_address: str, chain: str = "base", context: dict | None = None) -> dict:
        payload = {
            "contract_address": contract_address,
            "chain": chain,
            "context": context,
        }
        return self._request("POST", "/contracts/risk-score", json_payload=payload)

    def risk_score(self, contract_address: str, chain: str = "base", context: dict | None = None) -> dict:
        return self.scan(contract_address=contract_address, chain=chain, context=context)

    def health(self) -> dict:
        return self._request("GET", "/health")

    def manifest(self) -> dict:
        return self._request("GET", "/internal/manifest")
