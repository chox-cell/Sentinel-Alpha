import json
from datetime import datetime, timezone
from pathlib import Path

from services.mycelium_engine.engine import WEIGHTS


PHI_STATE_PATH = Path("logs/phi_state.json")
PHI_VERSION = "adaptive-phi-stub-v0.1"


def _default_multipliers() -> dict:
    return {signal_name: 1.0 for signal_name in WEIGHTS.keys()}


def _default_phi_state() -> dict:
    return {
        "version": PHI_VERSION,
        "updated_at": None,
        "multipliers": _default_multipliers(),
    }


def load_phi_state() -> dict:
    if not PHI_STATE_PATH.exists():
        return _default_phi_state()

    try:
        state = json.loads(PHI_STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _default_phi_state()

    multipliers = _default_multipliers()
    multipliers.update(state.get("multipliers", {}))

    return {
        "version": state.get("version", PHI_VERSION),
        "updated_at": state.get("updated_at"),
        "multipliers": multipliers,
    }


def save_phi_state(state: dict) -> None:
    payload = {
        "version": state.get("version", PHI_VERSION),
        "updated_at": state.get("updated_at") or datetime.now(timezone.utc).isoformat(),
        "multipliers": state.get("multipliers", _default_multipliers()),
    }
    PHI_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PHI_STATE_PATH.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def update_phi_from_outcomes(records: list) -> dict:
    state = load_phi_state()
    multipliers = dict(state.get("multipliers", _default_multipliers()))

    for record in records or []:
        action = record.get("action")
        score = int(record.get("score", 0) or 0)
        threat_class = record.get("threat_class")
        signals = record.get("signals") or {}
        triggered = [k for k, v in signals.items() if bool(v) and k in multipliers]

        if not triggered:
            continue

        # Conservative reinforcement for severe blocked outcomes.
        if action in {"BLOCK", "EXIT_NOW"} and score >= 85:
            for signal_name in triggered:
                multipliers[signal_name] = min(1.5, round(multipliers[signal_name] + 0.05, 4))
            continue

        # Stronger reinforcement when ALLOW later correlates with non-normal threat.
        if action == "ALLOW" and threat_class != "normal":
            for signal_name in triggered:
                multipliers[signal_name] = min(1.75, round(multipliers[signal_name] + 0.1, 4))
            continue

        # ALLOW + normal => unchanged.

    return {
        "version": PHI_VERSION,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "multipliers": multipliers,
    }
