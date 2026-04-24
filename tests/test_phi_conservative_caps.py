from services.mycelium_engine import phi


def test_update_phi_caps_at_live_safe_max(monkeypatch, tmp_path):
    monkeypatch.setattr(phi, "PHI_STATE_PATH", tmp_path / "phi_state.json")
    monkeypatch.setenv("PHI_LEARNING_RATE", "0.05")

    # Repeated strong updates should still cap at 1.25.
    records = [
        {
            "action": "ALLOW",
            "score": 40,
            "threat_class": "behavioral_launch_syndicate",
            "signals": {"shadow_link": 1},
        }
        for _ in range(20)
    ]
    updated = phi.update_phi_from_outcomes(records)
    assert updated["multipliers"]["shadow_link"] == 1.25


def test_load_phi_clamps_out_of_range_values(monkeypatch, tmp_path):
    path = tmp_path / "phi_state.json"
    monkeypatch.setattr(phi, "PHI_STATE_PATH", path)

    phi.save_phi_state(
        {
            "version": phi.PHI_VERSION,
            "updated_at": "2026-01-01T00:00:00+00:00",
            "multipliers": {"shadow_link": 2.0, "bad_cluster": 0.1},
        }
    )

    loaded = phi.load_phi_state()
    assert loaded["multipliers"]["shadow_link"] == 1.25
    assert loaded["multipliers"]["bad_cluster"] == 0.75
