import os
import subprocess
import sys
from pathlib import Path

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
    root = Path(__file__).resolve().parents[1]
    env_path = root / ".env"
    original = env_path.read_text(encoding="utf-8") if env_path.exists() else None
    env_path.write_text("PUBLIC_BASE_URL=\n", encoding="utf-8")
    env = os.environ.copy()
    env["PUBLIC_BASE_URL"] = ""
    try:
        proc = subprocess.run(
            [sys.executable, "scripts/public_smoke_test.py"],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode == 1
        assert "PUBLIC_BASE_URL configured: false" in proc.stdout
    finally:
        if original is None:
            env_path.unlink(missing_ok=True)
        else:
            env_path.write_text(original, encoding="utf-8")
