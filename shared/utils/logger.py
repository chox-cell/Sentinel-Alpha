from pathlib import Path
from datetime import datetime, timezone
import json

LOG_FILE = Path("logs/events.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_event(event_type: str, payload: dict):
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "payload": payload,
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
