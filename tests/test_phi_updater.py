from workers.phi_updater import run as phi_run


def test_phi_updater_reads_outcomes_and_writes_state(monkeypatch):
    saved = {}

    monkeypatch.setattr(
        phi_run,
        "get_recent_decisions",
        lambda limit=200: [{"action": "BLOCK", "score": 90, "signals": {"shadow_link": 1}}],
    )
    monkeypatch.setattr(
        phi_run,
        "update_phi_from_outcomes",
        lambda records: {
            "version": "adaptive-phi-stub-v0.1",
            "updated_at": "2026-01-01T00:00:00+00:00",
            "multipliers": {"shadow_link": 1.1},
        },
    )
    monkeypatch.setattr(phi_run, "save_phi_state", lambda state: saved.update(state))

    result = phi_run.run(limit=25)

    assert result["version"] == "adaptive-phi-stub-v0.1"
    assert saved["multipliers"]["shadow_link"] == 1.1
