import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app


def test_internal_manifest_includes_public_base_url_when_configured(monkeypatch):
    monkeypatch.setenv("PUBLIC_BASE_URL", "https://api.sentinel-alpha.example")
    client = TestClient(app)
    response = client.get("/internal/manifest")
    assert response.status_code == 200
    body = response.json()
    assert body["public_base_url"] == "https://api.sentinel-alpha.example"
    assert "BASE_RPC_URL" not in body


def test_internal_manifest_omits_public_base_url_when_empty(monkeypatch):
    monkeypatch.delenv("PUBLIC_BASE_URL", raising=False)
    client = TestClient(app)
    response = client.get("/internal/manifest")
    assert response.status_code == 200
    body = response.json()
    expected = json.loads(Path("docs/01_manifest/manifest.json").read_text(encoding="utf-8"))
    assert "public_base_url" not in body
    assert body == expected
