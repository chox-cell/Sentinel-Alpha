import hashlib
from pathlib import Path


REPORT_MD = Path("reports/trust_loop/minimum_verifiable_loop.sample.md")
TRUST_DOC = Path("docs/17_growth/AGENT_TRUST_LOOP_REFERENCE.md")
ALIGNMENT_DOC = Path("docs/17_growth/TRUST_LOOP_FIELD_ALIGNMENT_V1.md")
TRACKER = Path("docs/17_growth/OUTREACH_TRACKER.md")


def test_report_markdown_includes_external_validation_and_payment_hash_notes():
    text = REPORT_MD.read_text(encoding="utf-8").lower()
    assert "externally/community validated by `giskard09`".lower() in text
    assert "`payment_hash` is null in this sample because this is documentation-only" in text
    assert "in a live flow, `payment_hash` links payment authorization context to `post_action_trail`" in text
    assert "not partnership or official integration" in text


def test_trust_loop_and_alignment_docs_include_validation_notes():
    trust = TRUST_DOC.read_text(encoding="utf-8").lower()
    align = ALIGNMENT_DOC.read_text(encoding="utf-8").lower()
    assert "external/community field validation signal received from `giskard09`" in trust
    assert "`payment_hash` may be null in documentation-only samples" in trust
    assert "cross-surface payment-to-trail linkage" in trust
    assert "sample may use null; live flow uses it as cross-surface payment-to-trail key" in align
    assert "yes (hash/reference only)" in align


def test_outreach_tracker_records_mycelium_field_validation():
    text = TRACKER.read_text(encoding="utf-8").lower()
    assert "mycelium_field_validation_signal" in text
    assert "reviewer: giskard09" in text
    assert "validation_scope: trust loop report fixture post_action_trail section" in text
    assert "payment_hash is cross-surface key linking payment authorization context to post_action_trail" in text
    assert "external/community field validation signal only" in text
    assert "not partnership" in text
    assert "not official integration" in text


def test_forbidden_positive_phrases_absent_with_negation_allowed():
    combined = "\n".join(
        [
            REPORT_MD.read_text(encoding="utf-8"),
            TRUST_DOC.read_text(encoding="utf-8"),
            ALIGNMENT_DOC.read_text(encoding="utf-8"),
            TRACKER.read_text(encoding="utf-8"),
        ]
    ).lower()

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
        assert token not in combined

    phrase = "automatic x402 settlement"
    start = 0
    while True:
        idx = combined.find(phrase, start)
        if idx == -1:
            break
        window = combined[max(0, idx - 40) : idx + len(phrase) + 40]
        assert ("no automatic x402 settlement" in window) or ("does not perform automatic x402 settlement" in window)
        start = idx + 1


def test_env_unchanged_during_field_validation_signal_tests():
    env_path = Path(".env")
    before = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    _ = REPORT_MD.read_text(encoding="utf-8")
    _ = TRACKER.read_text(encoding="utf-8")
    after = hashlib.sha256(env_path.read_bytes()).hexdigest() if env_path.exists() else "missing"
    assert before == after
