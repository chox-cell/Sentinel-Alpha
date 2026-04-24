import json
import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def get_cache(key: str):
    value = r.get(key)
    if not value:
        return None
    return json.loads(value)

def set_cache(key: str, value: dict, ttl: int = 300):
    r.setex(key, ttl, json.dumps(value))
