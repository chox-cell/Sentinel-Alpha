from services.mycelium_engine import phi


def test_get_learning_rate_defaults_when_missing(monkeypatch):
    monkeypatch.delenv("PHI_LEARNING_RATE", raising=False)
    assert phi.get_learning_rate() == phi.DEFAULT_LEARNING_RATE


def test_get_learning_rate_uses_env(monkeypatch):
    monkeypatch.setenv("PHI_LEARNING_RATE", "0.02")
    assert phi.get_learning_rate() == 0.02


def test_get_learning_rate_invalid_fallback(monkeypatch):
    monkeypatch.setenv("PHI_LEARNING_RATE", "invalid")
    assert phi.get_learning_rate() == phi.DEFAULT_LEARNING_RATE


def test_update_phi_respects_learning_rate(monkeypatch, tmp_path):
    monkeypatch.setattr(phi, "PHI_STATE_PATH", tmp_path / "phi_state.json")
    monkeypatch.setenv("PHI_LEARNING_RATE", "0.01")

    updated = phi.update_phi_from_outcomes(
        [
            {
                "action": "ALLOW",
                "score": 40,
                "threat_class": "behavioral_launch_syndicate",
                "signals": {"shadow_link": 1},
            }
        ]
    )

    # 1.0 + (10 * 0.01)
    assert updated["multipliers"]["shadow_link"] == 1.1
