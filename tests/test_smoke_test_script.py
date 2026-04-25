from scripts import smoke_test


class _StubResp:
    def __init__(self, status_code: int):
        self.status_code = status_code


def test_smoke_report_pass(monkeypatch):
    def fake_get(url, timeout=8):
        return _StubResp(200)

    def fake_post(url, json=None, timeout=8):
        assert url.endswith("/contracts/risk-score")
        return _StubResp(402)

    monkeypatch.setattr("scripts.smoke_test.requests.get", fake_get)
    monkeypatch.setattr("scripts.smoke_test.requests.post", fake_post)

    report = smoke_test.build_smoke_report(base_url="http://127.0.0.1:8000")
    assert report["smoke_test_verdict"] == "pass"
    rendered = smoke_test.format_smoke_report(report)
    assert "smoke test verdict: pass" in rendered
    assert "POST /contracts/risk-score without payment returns 402: pass (status=402)" in rendered


def test_smoke_report_fail_and_secret_safe(monkeypatch):
    secret_url = "https://secret-host.local/rpc-token"

    def fake_get(url, timeout=8):
        if url.endswith("/internal/manifest"):
            return _StubResp(500)
        return _StubResp(200)

    def fake_post(url, json=None, timeout=8):
        return _StubResp(402)

    monkeypatch.setattr("scripts.smoke_test.requests.get", fake_get)
    monkeypatch.setattr("scripts.smoke_test.requests.post", fake_post)

    report = smoke_test.build_smoke_report(base_url=secret_url)
    assert report["smoke_test_verdict"] == "fail"
    rendered = smoke_test.format_smoke_report(report)
    assert "GET /internal/manifest: fail (status=500)" in rendered
    assert secret_url not in rendered
