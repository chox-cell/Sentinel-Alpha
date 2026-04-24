from services.cache import metrics


def test_record_hit_and_miss_updates_metrics_file(tmp_path, monkeypatch):
    target = tmp_path / "cache_metrics.json"
    monkeypatch.setattr(metrics, "CACHE_METRICS_PATH", target)

    metrics.reset_cache_metrics()
    metrics.record_cache_hit("k1")
    metrics.record_cache_miss("k1")
    metrics.record_cache_miss("k2")

    data = metrics.get_cache_metrics()
    assert data["cache_hits"] == 1
    assert data["cache_misses"] == 2
    assert data["total_requests"] == 3
    assert data["hit_rate"] == 0.3333
    assert data["keys"]["k1"]["hits"] == 1
    assert data["keys"]["k1"]["misses"] == 1
    assert data["keys"]["k2"]["misses"] == 1


def test_reset_cache_metrics_clears_counts(tmp_path, monkeypatch):
    target = tmp_path / "cache_metrics.json"
    monkeypatch.setattr(metrics, "CACHE_METRICS_PATH", target)

    metrics.record_cache_hit("k1")
    metrics.reset_cache_metrics()

    data = metrics.get_cache_metrics()
    assert data["cache_hits"] == 0
    assert data["cache_misses"] == 0
    assert data["total_requests"] == 0
    assert data["keys"] == {}
