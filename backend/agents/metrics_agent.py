import json
from datetime import datetime
import os

METRICS_FILE = "metrics.json"

# Initialize zeroed metrics structure
DEFAULT_METRICS = {
    "total_queries": 0,
    "category_counts": {
        "transport": 0,
        "electricity": 0,
        "food": 0,
        "general": 0
    },
    "total_emissions_logged": 0.0,
    "session_query_counts": {},
    "timestamps": []  # for tracing
}

def load_metrics():
    if not os.path.exists(METRICS_FILE):
        return DEFAULT_METRICS.copy()
    try:
        with open(METRICS_FILE, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_METRICS.copy()


def save_metrics(metrics):
    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2, default=str)


def log_metrics(session_id: str, intent: str, emission: float | None):
    metrics = load_metrics()

    # Total queries
    metrics["total_queries"] += 1

    # Category counts
    if intent in metrics["category_counts"]:
        metrics["category_counts"][intent] += 1
    else:
        metrics["category_counts"]["general"] += 1

    # Emission accumulation
    if emission is not None:
        metrics["total_emissions_logged"] += emission

    # Session query counts
    metrics["session_query_counts"].setdefault(session_id, 0)
    metrics["session_query_counts"][session_id] += 1

    # Timestamp log
    metrics["timestamps"].append({
        "ts": datetime.utcnow().isoformat(),
        "intent": intent,
        "session_id": session_id,
        "emission": emission
    })

    save_metrics(metrics)
    return metrics


def get_metrics():
    return load_metrics()
