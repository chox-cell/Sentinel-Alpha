from fastapi.testclient import TestClient

from apps.api.main import app
from shared.config.limits import get_ingestion_limits


def test_ingestion_limits_defaults(monkeypatch):
    monkeypatch.delenv("SENTINEL_MAX_CANDIDATES_PER_WEBHOOK", raising=False)
    monkeypatch.delenv("SENTINEL_MAX_EVALUATIONS_PER_WEBHOOK", raising=False)
    monkeypatch.delenv("SENTINEL_MAX_PAYLOAD_BYTES_WARN", raising=False)
    monkeypatch.delenv("SENTINEL_MAX_PAYLOAD_BYTES_HARD", raising=False)

    limits = get_ingestion_limits()
    assert limits["max_candidates_per_webhook"] == 50
    assert limits["max_evaluations_per_webhook"] == 10
    assert limits["max_payload_bytes_warn"] == 500000
    assert limits["max_payload_bytes_hard"] == 3000000


def test_internal_ingestion_status_endpoint(monkeypatch):
    monkeypatch.setenv("SENTINEL_MAX_CANDIDATES_PER_WEBHOOK", "60")
    monkeypatch.setenv("SENTINEL_MAX_EVALUATIONS_PER_WEBHOOK", "5")
    monkeypatch.setenv("SENTINEL_MAX_PAYLOAD_BYTES_WARN", "1000")
    monkeypatch.setenv("SENTINEL_MAX_PAYLOAD_BYTES_HARD", "2000")

    client = TestClient(app)
    response = client.get("/internal/ingestion/status")
    assert response.status_code == 200
    assert response.json() == {
        "max_candidates_per_webhook": 60,
        "max_evaluations_per_webhook": 5,
        "max_payload_bytes_warn": 1000,
        "max_payload_bytes_hard": 2000,
    }
