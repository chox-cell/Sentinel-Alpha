from workers.outcome_verifier import run as worker_run


def test_outcome_verifier_worker_runs(monkeypatch):
    monkeypatch.setattr(
        worker_run,
        "verify_recent_outcomes",
        lambda limit=50: [{"original_trace_id": "t-1", "actual_outcome": "safe_so_far"}],
    )

    result = worker_run.run(limit=25)
    assert len(result) == 1
    assert result[0]["original_trace_id"] == "t-1"
