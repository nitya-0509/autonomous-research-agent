# core/storage.py
import json
import os
from datetime import datetime
from threading import Lock

ROOT = os.path.dirname(os.path.dirname(__file__))
HISTORY_PATH = os.path.join(ROOT, "history.json")
_lock = Lock()

def _ensure_history():
    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)

def save_record(record: dict):
    _ensure_history()
    with _lock:
        with open(HISTORY_PATH, "r+", encoding="utf-8") as f:
            data = json.load(f)
            record["_saved_at"] = datetime.utcnow().isoformat() + "Z"
            data.insert(0, record)  # newest first
            f.seek(0)
            json.dump(data[:200], f, ensure_ascii=False, indent=2)  # keep latest 200
            f.truncate()

def load_history(limit=20):
    _ensure_history()
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data[:limit]
