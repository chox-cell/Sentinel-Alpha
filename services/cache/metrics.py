import json
from datetime import datetime, timezone
from pathlib import Path


CACHE_METRICS_PATH = Path("logs/cache_metrics.json")


def _default_metrics() -> dict:
    return {
        "cache_hits": 0,
        "cache_misses": 0,
        "keys": {},
        "updated_at": None,
    }


def _load_metrics() -> dict:
    if not CACHE_METRICS_PATH.exists():
        return _default_metrics()
    try:
        data = json.loads(CACHE_METRICS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _default_metrics()

    metrics = _default_metrics()
    metrics.update({k: v for k, v in data.items() if k in metrics})
    if not isinstance(metrics.get("keys"), dict):
        metrics["keys"] = {}
    return metrics


def _save_metrics(metrics: dict) -> None:
    metrics["updated_at"] = datetime.now(timezone.utc).isoformat()
    CACHE_METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_METRICS_PATH.write_text(
        json.dumps(metrics, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )


def record_cache_hit(cache_key: str) -> None:
    metrics = _load_metrics()
    metrics["cache_hits"] += 1
    entry = metrics["keys"].setdefault(cache_key, {"hits": 0, "misses": 0})
    entry["hits"] += 1
    _save_metrics(metrics)


def record_cache_miss(cache_key: str) -> None:
    metrics = _load_metrics()
    metrics["cache_misses"] += 1
    entry = metrics["keys"].setdefault(cache_key, {"hits": 0, "misses": 0})
    entry["misses"] += 1
    _save_metrics(metrics)


def get_cache_metrics() -> dict:
    metrics = _load_metrics()
    total = metrics["cache_hits"] + metrics["cache_misses"]
    hit_rate = (metrics["cache_hits"] / total) if total else 0.0
    return {
        **metrics,
        "total_requests": total,
        "hit_rate": round(hit_rate, 4),
    }


def reset_cache_metrics() -> None:
    _save_metrics(_default_metrics())
