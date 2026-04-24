import json

from services.outcome_memory import verifier


def test_verify_outcome_block_high_risk_branch():
    verified = verifier.verify_outcome(
        {
            "trace_id": "t-block",
            "contract_address": "0x1",
            "chain": "base",
            "score": 90,
            "action": "BLOCK",
            "threat_class": "behavioral_launch_syndicate",
            "signals": {"shadow_link": 1},
        }
    )
    assert verified["actual_outcome"] == "blocked_high_risk"
    assert verified["verifier_confidence"] == 0.7


def test_verify_outcome_allow_normal_branch():
    verified = verifier.verify_outcome(
        {
            "trace_id": "t-allow",
            "contract_address": "0x2",
            "chain": "base",
            "score": 20,
            "action": "ALLOW",
            "threat_class": "normal",
            "signals": {},
        }
    )
    assert verified["actual_outcome"] == "safe_so_far"
    assert verified["verifier_confidence"] == 0.55


def test_verify_recent_outcomes_writes_jsonl(tmp_path, monkeypatch):
    target = tmp_path / "verified_outcomes.jsonl"
    monkeypatch.setattr(verifier, "VERIFIED_OUTCOMES_PATH", target)
    monkeypatch.setattr(
        verifier,
        "get_recent_decisions",
        lambda limit=50: [
            {
                "trace_id": "t-exit",
                "contract_address": "0x3",
                "chain": "base",
                "score": 88,
                "action": "EXIT_NOW",
                "threat_class": "oracle_dislocation",
                "signals": {"oracle_dislocation": 1},
            }
        ],
    )

    rows = verifier.verify_recent_outcomes(limit=10)
    assert len(rows) == 1
    assert rows[0]["actual_outcome"] == "emergency_risk_confirmed"

    lines = target.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    raw = json.loads(lines[0])
    assert raw["original_trace_id"] == "t-exit"
