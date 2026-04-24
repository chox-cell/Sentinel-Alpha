import pytest

from sdk.python.client import SentinelAlphaClient


class _StubResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text

    def json(self):
        if isinstance(self._json_data, Exception):
            raise self._json_data
        return self._json_data


def test_client_health_manifest_risk_score(monkeypatch):
    calls = []

    def fake_request(method, url, json=None, headers=None, timeout=15):
        calls.append((method, url, json, headers, timeout))
        if url.endswith("/health"):
            return _StubResponse(json_data={"ok": True})
        if url.endswith("/internal/manifest"):
            return _StubResponse(json_data={"name": "Sentinel Alpha"})
        return _StubResponse(json_data={"api_version": "2026.8.0"})

    monkeypatch.setattr("sdk.python.client.requests.request", fake_request)

    client = SentinelAlphaClient("http://localhost:8000", payment_signature="demo")
    assert client.health()["ok"] is True
    assert client.manifest()["name"] == "Sentinel Alpha"
    result = client.risk_score("0x1111111111111111111111111111111111111111")
    assert result["api_version"] == "2026.8.0"
    assert calls[2][0] == "POST"
    assert calls[2][3]["PAYMENT-SIGNATURE"] == "demo"


def test_client_non_200_raises(monkeypatch):
    def fake_request(method, url, json=None, headers=None, timeout=15):
        return _StubResponse(status_code=500, text="boom")

    monkeypatch.setattr("sdk.python.client.requests.request", fake_request)
    client = SentinelAlphaClient("http://localhost:8000")

    with pytest.raises(RuntimeError, match="Non-200 response"):
        client.health()


def test_client_non_json_raises(monkeypatch):
    def fake_request(method, url, json=None, headers=None, timeout=15):
        return _StubResponse(json_data=ValueError("no json"))

    monkeypatch.setattr("sdk.python.client.requests.request", fake_request)
    client = SentinelAlphaClient("http://localhost:8000")

    with pytest.raises(RuntimeError, match="Non-JSON response"):
        client.manifest()


def test_client_timeout_raises(monkeypatch):
    import requests

    def fake_request(method, url, json=None, headers=None, timeout=15):
        raise requests.Timeout("timeout")

    monkeypatch.setattr("sdk.python.client.requests.request", fake_request)
    client = SentinelAlphaClient("http://localhost:8000")

    with pytest.raises(RuntimeError, match="Request timeout"):
        client.health()
