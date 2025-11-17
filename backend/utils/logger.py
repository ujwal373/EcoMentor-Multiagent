import json, os
from datetime import datetime

LOG_FILE = "logs.json"

def log_to_file(entry: dict):
    entry["timestamp"] = datetime.utcnow().isoformat()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    else:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([entry], f, indent=2)
