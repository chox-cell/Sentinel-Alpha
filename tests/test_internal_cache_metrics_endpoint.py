from fastapi.testclient import TestClient

from apps.api.main import app


def test_internal_cache_metrics_endpoint_returns_metrics(monkeypatch):
    from apps.api import main

    monkeypatch.setattr(
        main,
        "get_cache_metrics",
        lambda: {
            "cache_hits": 4,
            "cache_misses": 6,
            "total_requests": 10,
            "hit_rate": 0.4,
            "keys": {},
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    client = TestClient(app)
    response = client.get("/internal/cache-metrics")

    assert response.status_code == 200
    body = response.json()
    assert body["cache_hits"] == 4
    assert body["cache_misses"] == 6
    assert body["total_requests"] == 10
    assert body["hit_rate"] == 0.4
