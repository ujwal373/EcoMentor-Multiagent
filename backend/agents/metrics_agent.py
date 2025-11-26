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
    "timestamps": [],  # for tracing,
    "positive_actions": [],
    "negative_actions": []
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
    # Ensure positive actions exist
    metrics.setdefault("positive_actions", [])
    # Ensure negative actions exist
    metrics.setdefault("negative_actions", [])
    # Positive action logging
    if intent in POSITIVE_POINTS:
        metrics["positive_actions"].append({
            "timestamp": datetime.utcnow(),
            "action": intent,
            "points": POSITIVE_POINTS[intent]
        })

    # Negative action logging
    if intent in NEGATIVE_POINTS:
        metrics["negative_actions"].append({
            "timestamp": datetime.utcnow(),
            "action": intent,
            "points": NEGATIVE_POINTS[intent]
        })

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

def calculate_sustainability_score(metrics, weekly_current, weekly_previous=0):
    total_queries = metrics["total_queries"]
    
    # 1. Baseline emission score (40%)
    weekly_em = weekly_current
    baseline = max(0, 40 - (weekly_em * 0.8))

    # 2. Improvement score (25%)
    if weekly_previous > 0:
        improvement = 25 * (weekly_previous - weekly_em) / max(weekly_previous, weekly_em)
    else:
        improvement = 12  # neutral mid-score for first week

    improvement = max(0, improvement)

    # 3. Category mix score (15%)
    counts = metrics["category_counts"]
    weights = {"electricity": 1.0, "food": 0.8, "transport": 0.5, "general": 0.7}

    mix_raw = sum(counts[c] * weights.get(c, 1.0) for c in counts)
    mix = max(0, 15 - mix_raw)

    # 4. Engagement score (10%)
    engagement = min(10, total_queries * 0.5)

    # 5. Consistency score (10%)
    distinct_days = len({ts["ts"][:10] for ts in metrics["timestamps"]})
    consistency = min(10, distinct_days * 2)

    score = baseline + improvement + mix + engagement + consistency
    score = min(100, max(0, score))

    # Positive action bonus (maximum +20)
    positive_actions = metrics.get("positive_actions", [])
    positive_boost = min(20, sum(a["points"] for a in positive_actions))
    score += positive_boost

    # Negative action penalty (maximum -10)
    negative_actions = metrics.get("negative_actions", [])
    negative_penalty = min(10, sum(a["points"] for a in negative_actions))
    score -= negative_penalty

    return round(score, 2)
