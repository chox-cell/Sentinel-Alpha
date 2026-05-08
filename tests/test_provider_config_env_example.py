import hashlib
from pathlib import Path


ENV_EXAMPLE = Path(".env.example")
GITIGNORE = Path(".gitignore")
ENV_POLICY = Path("docs/16_launch/ENV_SAFETY_POLICY.md")
ACTIVATION_PLAN = Path("docs/16_launch/ABI_SOURCE_PROVIDER_ACTIVATION_PLAN.md")
STRATEGY = Path("docs/16_launch/SENTINEL_DATA_PROVIDER_STRATEGY.md")
GATE = Path("docs/16_launch/SENTINEL_PROVIDER_DECISION_GATE.md")
CLAIMS = Path("docs/18_investor/CLAIMS_LEDGER.md")


def _value_for(text: str, key: str) -> str | None:
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == key:
            return v.strip()
    return None


def test_env_example_exists_and_has_required_placeholders():
    assert ENV_EXAMPLE.exists()
    text = ENV_EXAMPLE.read_text(encoding="utf-8")
    lower = text.lower()

    assert "sentinel_abi_source_provider_enabled=false" in lower
    assert "sentinel_abi_source_provider_name=" in lower
    assert "sentinel_abi_source_provider_timeout_ms=" in lower
    assert "basescan_api_key=" in lower
    assert "etherscan_api_key=" in lower
    assert "sourcify_enabled=false" in lower
    assert "blockscout_base_url=" in lower

    assert _value_for(text, "SENTINEL_ABI_SOURCE_PROVIDER_ENABLED") == "false"
    assert _value_for(text, "SENTINEL_ABI_SOURCE_PROVIDER_NAME") == ""
    assert _value_for(text, "BASESCAN_API_KEY") == ""
    assert _value_for(text, "ETHERSCAN_API_KEY") == ""
    assert _value_for(text, "SOURCIFY_ENABLED") == "false"
    assert _value_for(text, "BLOCKSCOUT_BASE_URL") == ""


def test_env_example_has_no_obvious_real_secrets_and_env_is_gitignored():
    text = ENV_EXAMPLE.read_text(encoding="utf-8")
    for marker in [
        "sk_live_",
        "xoxb-",
        "ghp_",
        "0xabcdef",
        "bearer ",
        "api_key=real",
    ]:
        assert marker not in text.lower()

    gitignore = GITIGNORE.read_text(encoding="utf-8").splitlines()
    assert ".env" in [line.strip() for line in gitignore]


def test_docs_cover_placeholders_only_and_disabled_defaults():
    env_policy = ENV_POLICY.read_text(encoding="utf-8").lower()
    plan = ACTIVATION_PLAN.read_text(encoding="utf-8").lower()
    strategy = STRATEGY.read_text(encoding="utf-8").lower()
    gate = GATE.read_text(encoding="utf-8").lower()
    claims = CLAIMS.read_text(encoding="utf-8").lower()

    assert "`.env.example` may contain placeholders" in env_policy
    assert "must never be mutated by tests" in env_policy
    assert "never commit provider keys" in env_policy

    assert "placeholders are present in `.env.example` only" in plan
    assert "provider disabled by default" in plan
    assert "not required now" in plan
    assert "must never be modified by tests" in plan

    assert "provider disabled by default" in strategy
    assert "keys are optional/future-only and not required now" in strategy
    assert "placeholder presence in `.env.example` plus explicit founder approval" in gate
    assert "provider placeholders exist in `.env.example`" in claims


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            ENV_EXAMPLE.read_text(encoding="utf-8"),
            ACTIVATION_PLAN.read_text(encoding="utf-8"),
            STRATEGY.read_text(encoding="utf-8"),
            GATE.read_text(encoding="utf-8"),
            CLAIMS.read_text(encoding="utf-8"),
        ]
    ).lower()
    forbidden = [
        "live abi coverage is available",
        "full verified-source coverage is available",
        "guaranteed source verification is provided",
        "claims it detects honeypots",
        "guaranteed protection is provided",
        "claims it prevents mev",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in combined


def test_env_unchanged_during_provider_config_env_example_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = ENV_EXAMPLE.read_text(encoding="utf-8")
    _ = ACTIVATION_PLAN.read_text(encoding="utf-8")
    _ = ENV_POLICY.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
