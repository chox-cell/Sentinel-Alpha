import hashlib
from pathlib import Path


DOC = Path("docs/17_growth/COMPOSABILITY_REFERENCE_DRAFT.md")
SKETCH = Path("examples/agentkit-sentinel-provider/src/prePostLoopSketch.ts")


def test_composability_doc_exists_and_required_content():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    lower = text.lower()
    assert "https://github.com/giskard09/argentum-core/blob/feat/mycelium-trails/docs/MYCELIUM_TRAILS_REFERENCE.md" in text
    assert "external community draft, not dependency" in lower
    assert "Sentinel Alpha / BeezShield" in text
    assert "Do not use AgentShield as our product name" in text
    assert "Sentinel pre-check" in text
    assert "x402 payment authorization" in lower
    assert "AgentKit action" in text
    assert "Mycelium Trails post-action record" in text
    assert "Audit independence" in text
    assert "notSecurityGuarantee" in text
    assert "sentinel_decision_ref" in text
    assert "action_ref" in text
    assert "payment_hash" in text
    assert "claims" in text
    assert "sample-output.json" in text
    for field in ["trail_id", "agent_id", "service", "operation", "action_ref", "payment_hash", "timestamp", "signature_ref", "claims", "success"]:
        assert field in text
    assert "No partnership claim" in text or "no partnership claim" in lower
    assert "no official integration claim" in lower
    assert DOC.exists() and SKETCH.exists()


def test_sketch_includes_sentinel_decision_ref_and_action_ref():
    text = SKETCH.read_text(encoding="utf-8").lower()
    assert "sentinel_decision_ref" in text
    assert "action_ref" in text


def test_forbidden_phrases_absent():
    lower = (DOC.read_text(encoding="utf-8") + "\n" + SKETCH.read_text(encoding="utf-8")).lower()
    forbidden = [
        "partnership live",
        "integration is live and active",
        "official provider is live",
        "guaranteed protection is provided",
        "claims it detects honeypots",
        "claims it prevents mev",
        "live simulation is enabled",
    ]
    for token in forbidden:
        assert token not in lower


def test_env_unchanged_during_composability_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = DOC.read_text(encoding="utf-8")
    _ = SKETCH.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
