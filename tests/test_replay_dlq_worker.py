import json

from workers.replay_dlq import run as replay_run


def test_replay_dlq_worker_reads_retries_and_logs(monkeypatch, tmp_path):
    replay_path = tmp_path / "replay.jsonl"
    monkeypatch.setattr(replay_run, "REPLAY_LOG_PATH", replay_path)
    monkeypatch.setattr(
        replay_run,
        "read_dlq",
        lambda limit=50: [
            {
                "trace_id": "t-1",
                "source": "quicknode",
                "candidate": {
                    "contract_address": "0x1111111111111111111111111111111111111111",
                    "chain": "base",
                    "context": {"event_type": "new_deploy"},
                },
            }
        ],
    )
    monkeypatch.setattr(
        replay_run,
        "evaluate_contract",
        lambda contract_address, chain, context=None: {"ok": True},
    )

    summary = replay_run.run(limit=10)
    assert summary["attempted"] == 1
    assert summary["succeeded"] == 1
    assert replay_path.exists()

    lines = replay_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    decoded = json.loads(lines[0])
    assert decoded["succeeded"] == 1
