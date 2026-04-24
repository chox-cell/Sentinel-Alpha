import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app


def test_internal_manifest_endpoint_returns_manifest_json():
    client = TestClient(app)
    response = client.get("/internal/manifest")

    assert response.status_code == 200
    body = response.json()
    expected = json.loads(Path("docs/01_manifest/manifest.json").read_text(encoding="utf-8"))
    assert body == expected
