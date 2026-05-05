import hashlib
import json
from pathlib import Path


MANIFESTO = Path("apps/website/manifesto.html")
DOCTRINE_JSON = Path("apps/website/.well-known/beezshield-doctrine.json")
LLMS = Path("apps/website/llms.txt")
LLMS_FULL = Path("apps/website/llms-full.txt")


def test_manifesto_and_doctrine_json_exist():
    assert MANIFESTO.exists()
    assert DOCTRINE_JSON.exists()
    payload = json.loads(DOCTRINE_JSON.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    assert payload.get("brand") == "BeezShield"


def test_manifesto_required_phrases():
    text = MANIFESTO.read_text(encoding="utf-8")
    required = [
        "BeezShield builds guardians, not traders",
        "Autonomous agents should not execute blind",
        "Sentinel Alpha is a live pre-execution risk decision layer",
        "Trust Object Model is roadmap only",
        "UCP/AP2 commerce context is roadmap only",
        "Ema-Bee is a future commerce safety gate concept",
        "@beezshield/sentinel",
        "x402",
        "ERC-8004",
    ]
    for token in required:
        assert token in text


def test_forbidden_phrases_absent_and_no_secrets():
    combined = "\n".join(
        [
            MANIFESTO.read_text(encoding="utf-8").lower(),
            DOCTRINE_JSON.read_text(encoding="utf-8").lower(),
            LLMS.read_text(encoding="utf-8").lower(),
            LLMS_FULL.read_text(encoding="utf-8").lower(),
        ]
    )
    forbidden = [
        "detects honeypots",
        "prevents mev",
        "prevents prompt injection",
        "full intent verification",
        "guaranteed protection",
        "central bank of trust",
        "b2b arbitrage product",
    ]
    for token in forbidden:
        assert token not in combined
    for marker in ["private_key", "seed phrase", "secret_key", "api_key", "token="]:
        assert marker not in combined


def test_env_unchanged_during_guardian_pack_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = MANIFESTO.read_text(encoding="utf-8")
    _ = DOCTRINE_JSON.read_text(encoding="utf-8")
    _ = LLMS.read_text(encoding="utf-8")
    _ = LLMS_FULL.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
