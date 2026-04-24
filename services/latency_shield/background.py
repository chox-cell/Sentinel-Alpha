from fastapi import BackgroundTasks

from services.outcome_memory.memory import record_decision
from shared.utils.logger import log_event


def schedule_post_risk_tasks(
    background_tasks: BackgroundTasks,
    *,
    event_payload: dict,
    outcome_record: dict | None,
) -> None:
    background_tasks.add_task(log_event, "risk_score_generated", event_payload)
    if outcome_record:
        background_tasks.add_task(record_decision, outcome_record)
