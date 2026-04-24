from services.outcome_memory.verifier import verify_recent_outcomes


def run(limit: int = 50) -> list:
    return verify_recent_outcomes(limit=limit)


if __name__ == "__main__":
    run()
