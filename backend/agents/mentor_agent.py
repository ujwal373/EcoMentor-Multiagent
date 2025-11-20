import re
from typing import Optional
from config import get_openai_client, OPENAI_MODEL
from agents.tool_agent import calculate_emission
from agents.memory_agent import update_session, session_summary

client = None


def _get_client():
    global client
    if client is None:
        client = get_openai_client()
    return client


def detect_intent(message: str) -> str:
    text = message.lower()
    if any(w in text for w in ["drive", "car", "bus", "km", "transport"]):
        return "transport"
    if any(w in text for w in ["kwh", "electricity", "energy", "appliance"]):
        return "electricity"
    if any(w in text for w in ["food", "meal", "diet", "meat", "vegan"]):
        return "food"
    return "general"


def extract_numeric_value(message: str) -> Optional[float]:
    m = re.search(r"(\d+(\.\d+)?)", message)
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def mentor_reply(message: str, session_id: str = "default") -> str:
    intent = detect_intent(message)
    numeric = extract_numeric_value(message)

    emission_context = "No numeric emission estimate available."
    calc = None
    if intent in {"transport", "electricity", "food"} and numeric is not None:
        calc = calculate_emission(intent, numeric)
        emission_context = (
            f"Estimated emission (rough) for this activity: "
            f"{calc['emission_kg']} kg CO₂e "
            f"for value={numeric} in category='{intent}'."
        )

    past_summary = session_summary(session_id)
    weekly = weekly_summary(session_id)
    weekly_context = (
        f"User's weekly emission total: {weekly['weekly_total_kg']} kg CO₂e. "
        f"Category breakdown: {weekly['breakdown']}. "
    )

    system_prompt = (
        "You are EcoMentor, a friendly sustainability coach. "
        "Help users understand and reduce their carbon footprint. "
        "Use concrete numbers when available and suggest 1–3 realistic next steps. "
        "Keep answers short, clear, and encouraging."
    )

    user_context = (
    f"User message: {message}\n\n"
    f"Detected intent: {intent}.\n"
    f"{emission_context}\n\n"
    f"Previous context: {past_summary}\n\n"
    f"Weekly context: {weekly_context}\n\n"
    "Give a helpful and personalized sustainability suggestion."
)


    # store this interaction in memory before/after LLM (here: before)
    interaction = {
        "intent": intent,
        "message": message,
        "numeric": numeric,
        "emission_kg": calc["emission_kg"] if calc else None,
    }
    update_session(session_id, interaction)

    try:
        c = _get_client()
        resp = c.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_context},
            ],
            temperature=0.4,
            max_tokens=350,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return (
            "I had an issue calling the AI backend, but I’ve stored your activity "
            "and will use it to improve future suggestions. For now, try reducing "
            "frequency, switching to a lower-carbon alternative, and track the change for a week."
        )
