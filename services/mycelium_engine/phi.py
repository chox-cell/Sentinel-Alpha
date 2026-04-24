import json
import os
from datetime import datetime, timezone
from pathlib import Path

from services.mycelium_engine.engine import WEIGHTS


PHI_STATE_PATH = Path("logs/phi_state.json")
PHI_VERSION = "adaptive-phi-stub-v0.1"
DEFAULT_LEARNING_RATE = 0.01
MIN_MULTIPLIER = 0.75
MAX_MULTIPLIER = 1.25


def _default_multipliers() -> dict:
    return {signal_name: 1.0 for signal_name in WEIGHTS.keys()}


def _clamp_multiplier(value: float) -> float:
    return round(max(MIN_MULTIPLIER, min(MAX_MULTIPLIER, float(value))), 4)


def get_learning_rate() -> float:
    raw = os.getenv("PHI_LEARNING_RATE")
    if raw is None:
        return DEFAULT_LEARNING_RATE

    try:
        eta = float(raw)
    except (TypeError, ValueError):
        return DEFAULT_LEARNING_RATE

    if eta <= 0:
        return DEFAULT_LEARNING_RATE
    return eta


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
    multipliers = {k: _clamp_multiplier(v) for k, v in multipliers.items()}

    return {
        "version": state.get("version", PHI_VERSION),
        "updated_at": state.get("updated_at"),
        "multipliers": multipliers,
    }


def save_phi_state(state: dict) -> None:
    source_multipliers = state.get("multipliers", _default_multipliers())
    multipliers = {
        signal_name: _clamp_multiplier(source_multipliers.get(signal_name, 1.0))
        for signal_name in _default_multipliers().keys()
    }
    payload = {
        "version": state.get("version", PHI_VERSION),
        "updated_at": state.get("updated_at") or datetime.now(timezone.utc).isoformat(),
        "multipliers": multipliers,
    }
    PHI_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PHI_STATE_PATH.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def update_phi_from_outcomes(records: list) -> dict:
    state = load_phi_state()
    multipliers = dict(state.get("multipliers", _default_multipliers()))
    learning_rate = get_learning_rate()

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
                delta = 5 * learning_rate
                multipliers[signal_name] = _clamp_multiplier(multipliers[signal_name] + delta)
            continue

        # Stronger reinforcement when ALLOW later correlates with non-normal threat.
        if action == "ALLOW" and threat_class != "normal":
            for signal_name in triggered:
                delta = 10 * learning_rate
                multipliers[signal_name] = _clamp_multiplier(multipliers[signal_name] + delta)
            continue

        # ALLOW + normal => unchanged.

    return {
        "version": PHI_VERSION,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "multipliers": {k: _clamp_multiplier(v) for k, v in multipliers.items()},
    }
