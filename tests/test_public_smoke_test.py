import os

from scripts import public_smoke_test


class _StubResp:
    def __init__(self, status_code: int):
        self.status_code = status_code


def test_public_smoke_report_requires_public_base_url(monkeypatch):
    monkeypatch.delenv("PUBLIC_BASE_URL", raising=False)
    report = public_smoke_test.build_public_smoke_report()
    assert report["public_base_url_configured"] is False
    assert report["smoke_test_verdict"] == "fail"
    rendered = public_smoke_test.format_public_smoke_report(report)
    assert "error: PUBLIC_BASE_URL is required" in rendered


def test_public_smoke_report_pass_and_secret_safe(monkeypatch):
    secret_url = "https://secret-host.example/token-value"

    def fake_get(url, timeout=8):
        return _StubResp(200)

    def fake_post(url, json=None, timeout=8):
        assert url.endswith("/contracts/risk-score")
        return _StubResp(402)

    monkeypatch.setattr("scripts.public_smoke_test.requests.get", fake_get)
    monkeypatch.setattr("scripts.public_smoke_test.requests.post", fake_post)

    report = public_smoke_test.build_public_smoke_report(public_base_url=secret_url)
    assert report["smoke_test_verdict"] == "pass"
    rendered = public_smoke_test.format_public_smoke_report(report)
    assert "smoke test verdict: pass" in rendered
    assert secret_url not in rendered


def test_public_smoke_script_exits_non_zero_without_public_base_url(monkeypatch):
    monkeypatch.setenv("PUBLIC_BASE_URL", "")
    report = public_smoke_test.build_public_smoke_report()
    rendered = public_smoke_test.format_public_smoke_report(report)
    assert report["smoke_test_verdict"] == "fail"
    assert "PUBLIC_BASE_URL configured: false" in rendered
