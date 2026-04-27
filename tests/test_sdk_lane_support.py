from pathlib import Path

from sdk.python.client import SentinelAlphaClient


class _StubResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data if json_data is not None else {"ok": True}
        self.text = text

    def json(self):
        return self._json_data


def test_python_sdk_scan_lane_header(monkeypatch):
    calls = []

    def fake_request(method, url, json=None, headers=None, timeout=15):
        calls.append((method, url, json, headers, timeout))
        return _StubResponse()

    monkeypatch.setattr("sdk.python.client.requests.request", fake_request)
    client = SentinelAlphaClient("http://localhost:8000", payment_signature="demo")
    client.scan("0x1111111111111111111111111111111111111111", lane="executive")
    assert calls[0][3]["X-SENTINEL-LANE"] == "executive"


def test_typescript_sdk_scan_lane_signature_present():
    content = Path("sdk/typescript/client.ts").read_text(encoding="utf-8")
    assert "async scan(contractAddress: string, chain = \"base\", lane = \"basic\")" in content
    assert "\"X-SENTINEL-LANE\": lane" in content
