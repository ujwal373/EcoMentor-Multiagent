from typing import Dict, Any, List
from datetime import datetime, timedelta
from agents.intent_agent import POSITIVE_PATTERNS, NEGATIVE_PATTERNS
from agents.metrics_agent import POSITIVE_POINTS, NEGATIVE_POINTS

_MEMORY: Dict[str, Dict[str, Any]] = {}


def get_session(session_id: str) -> Dict[str, Any]:
    if session_id not in _MEMORY:
        _MEMORY[session_id] = {
            "history": [],
            "positive_actions": [],
            "negative_actions": [],
            "emission_log": [],       # list of { timestamp, category, emission }
            "category_totals": {      # sum of emissions per category
                "transport": 0.0,
                "electricity": 0.0,
                "food": 0.0
            }
        }
    return _MEMORY[session_id]


def update_session(session_id: str, interaction: Dict[str, Any]) -> None:
    session = get_session(session_id)

    # store raw history
    session["history"].append(interaction)

    # store emission logs if exists
    if interaction.get("emission_kg") is not None:
        session["emission_log"].append({
            "timestamp": datetime.utcnow(),
            "category": interaction.get("intent"),
            "emission": interaction.get("emission_kg")
        })

        # update category totals
        cat = interaction.get("intent")
        if cat in session["category_totals"]:
            session["category_totals"][cat] += interaction["emission_kg"]

    # --- Positive Action Logging ---
    POSITIVE_POINTS = {
        "tree_planting": 5,
        "positive_transport": 2,
        "public_transport": 1,
        "energy_reduction": 3,
        "renewable_energy": 10,
        "waste_reduction": 3,
        "local_food_choice": 2
    }

    intent = interaction.get("intent")
    if intent in POSITIVE_POINTS:
        session["positive_actions"].append({
            "timestamp": datetime.utcnow(),
            "action": intent,
            "points": POSITIVE_POINTS[intent]
        })

    # --- Negative Action Logging ---
    NEGATIVE_POINTS = {
        "negative_transport": -2,
        "negative_energy": -1,
        "negative_food": -1,
        "negative_waste": -1,
        "negative_local": -1
    }

    if intent in NEGATIVE_POINTS:
        session["negative_actions"].append({
            "timestamp": datetime.utcnow(),
            "action": intent,
            "points": NEGATIVE_POINTS[intent]
        })


def session_summary(session_id: str) -> str:
    session = get_session(session_id)
    history = session["history"]

    if not history:
        return "No past context for this user."

    total = sum((h.get("emission_kg") or 0) for h in history)
    last_intent = history[-1].get("intent", "unknown")

    return (
        f"This user has {len(history)} interactions so far. "
        f"Last activity: {last_intent}. "
        f"Total emissions discussed: {round(total, 2)} kg CO₂e."
    )


def weekly_summary(session_id: str) -> Dict[str, Any]:
    session = get_session(session_id)
    logs = session["emission_log"]

    one_week_ago = datetime.utcnow() - timedelta(days=7)

    weekly_entries = [
        l for l in logs if l["timestamp"] >= one_week_ago
    ]

    weekly_total = sum(l["emission"] for l in weekly_entries)

    breakdown = {}
    for l in weekly_entries:
        breakdown.setdefault(l["category"], 0.0)
        breakdown[l["category"]] += l["emission"]

    return {
        "weekly_total_kg": round(weekly_total, 2),
        "breakdown": breakdown,
        "entries": len(weekly_entries)
    }
