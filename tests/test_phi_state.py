import json

from services.mycelium_engine import phi


def test_load_phi_state_defaults_when_missing(tmp_path, monkeypatch):
    target = tmp_path / "phi_state.json"
    monkeypatch.setattr(phi, "PHI_STATE_PATH", target)

    state = phi.load_phi_state()
    assert state["version"] == phi.PHI_VERSION
    assert "shadow_link" in state["multipliers"]
    assert state["multipliers"]["shadow_link"] == 1.0


def test_save_then_load_phi_state_roundtrip(tmp_path, monkeypatch):
    target = tmp_path / "phi_state.json"
    monkeypatch.setattr(phi, "PHI_STATE_PATH", target)

    phi.save_phi_state(
        {
            "version": phi.PHI_VERSION,
            "updated_at": "2026-01-01T00:00:00+00:00",
            "multipliers": {"shadow_link": 1.2},
        }
    )

    raw = json.loads(target.read_text(encoding="utf-8"))
    assert raw["version"] == phi.PHI_VERSION

    loaded = phi.load_phi_state()
    assert loaded["multipliers"]["shadow_link"] == 1.2
    assert loaded["multipliers"]["bad_cluster"] == 1.0


def test_update_phi_from_outcomes_stub_rules(tmp_path, monkeypatch):
    target = tmp_path / "phi_state.json"
    monkeypatch.setattr(phi, "PHI_STATE_PATH", target)

    updated = phi.update_phi_from_outcomes(
        [
            {
                "action": "BLOCK",
                "score": 90,
                "threat_class": "behavioral_launch_syndicate",
                "signals": {"shadow_link": 1},
            },
            {
                "action": "ALLOW",
                "score": 40,
                "threat_class": "behavioral_launch_syndicate",
                "signals": {"shadow_link": 1},
            },
            {
                "action": "ALLOW",
                "score": 10,
                "threat_class": "normal",
                "signals": {"shadow_link": 1},
            },
        ]
    )

    assert updated["multipliers"]["shadow_link"] > 1.0
    assert updated["multipliers"]["shadow_link"] <= 1.25
