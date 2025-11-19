from typing import Dict, Any, List

# Very simple in-memory store: { session_id: { "history": [ ... ] } }
_MEMORY: Dict[str, Dict[str, Any]] = {}


def get_session(session_id: str) -> Dict[str, Any]:
    if session_id not in _MEMORY:
        _MEMORY[session_id] = {"history": []}
    return _MEMORY[session_id]


def update_session(session_id: str, interaction: Dict[str, Any]) -> None:
    session = get_session(session_id)
    history: List[Dict[str, Any]] = session.setdefault("history", [])
    history.append(interaction)


def session_summary(session_id: str) -> str:
    session = get_session(session_id)
    history: List[Dict[str, Any]] = session.get("history", [])
    if not history:
        return "No past context for this user."

    total_emission = sum(
        (h.get("emission_kg") or 0.0) for h in history
    )
    last_intent = history[-1].get("intent") or "unknown"
    return (
        f"This user has {len(history)} previous interactions. "
        f"Last focus area: {last_intent}. "
        f"Approx total emissions discussed so far: {round(total_emission, 2)} kg CO₂e."
    )
