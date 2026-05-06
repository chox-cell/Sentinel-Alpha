import hashlib
from pathlib import Path


DOC_LAUNCH = Path("docs/16_launch/SENTINEL_PRE_POST_AGENT_ACTION_LOOP.md")
DOC_GROWTH = Path("docs/17_growth/PRE_POST_LOOP_REFERENCE_PATTERN.md")
SKETCH = Path("examples/agentkit-sentinel-provider/src/prePostLoopSketch.ts")


def test_pre_post_docs_and_sketch_exist():
    assert DOC_LAUNCH.exists()
    assert DOC_GROWTH.exists()
    assert SKETCH.exists()


def test_required_loop_wording_present():
    launch_text = DOC_LAUNCH.read_text(encoding="utf-8").lower()
    sketch_text = SKETCH.read_text(encoding="utf-8").lower()
    assert "should this agent act" in launch_text
    assert "what happened and can it be verified" in launch_text
    assert "allow/review/block" in launch_text or "allow/review/block" in sketch_text
    assert "no official agentkit integration" in launch_text
    assert "no mycelium trails integration" in launch_text
    assert "no partnership" in launch_text


def test_sketch_placeholders_and_no_wallet_libs():
    text = SKETCH.read_text(encoding="utf-8")
    lower = text.lower()
    assert "executeAction(" in text
    assert "recordPostExecutionTrail(" in text
    forbidden_wallet_markers = ["ethers", "viem", "walletconnect", "private_key", "seed phrase"]
    for marker in forbidden_wallet_markers:
        assert marker not in lower


def test_docs_include_issue_and_context_reference():
    text = DOC_LAUNCH.read_text(encoding="utf-8")
    assert "https://github.com/coinbase/agentkit/issues/1168" in text
    assert "giskard09" in text
    assert "https://argentum.rgiskard.xyz/trails/demo" in text


def test_forbidden_phrases_absent():
    combined = "\n".join(
        [
            DOC_LAUNCH.read_text(encoding="utf-8").lower(),
            DOC_GROWTH.read_text(encoding="utf-8").lower(),
            SKETCH.read_text(encoding="utf-8").lower(),
        ]
    )
    forbidden = [
        "integration is live",
        "official provider is live",
        "guaranteed protection is provided",
        "claims it detects honeypots",
        "claims it prevents mev",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in combined


def test_env_unchanged_during_pre_post_loop_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DOC_LAUNCH.read_text(encoding="utf-8")
    _ = DOC_GROWTH.read_text(encoding="utf-8")
    _ = SKETCH.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
