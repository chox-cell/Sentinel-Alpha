from services.mycelium_engine.phi import save_phi_state, update_phi_from_outcomes
from services.outcome_memory.memory import get_recent_decisions


def run(limit: int = 200) -> dict:
    records = get_recent_decisions(limit=limit)
    next_state = update_phi_from_outcomes(records)
    save_phi_state(next_state)
    return next_state


if __name__ == "__main__":
    run()
