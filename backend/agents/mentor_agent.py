import re
from typing import Optional

from config import get_openai_client, OPENAI_MODEL
from agents.tool_agent import calculate_emission

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


def mentor_reply(message: str) -> str:
    intent = detect_intent(message)
    numeric = extract_numeric_value(message)

    emission_context = ""
    if intent in {"transport", "electricity", "food"} and numeric is not None:
        calc = calculate_emission(intent, numeric)
        emission_context = (
            f"Estimated emission (rough) for this activity: "
            f"{calc['emission_kg']} kg CO₂e "
            f"for value={numeric} in category='{intent}'."
        )

    system_prompt = (
        "You are EcoMentor, a friendly sustainability coach. "
        "Your job is to help users understand and reduce their carbon footprint. "
        "Be concrete, numeric where possible, and suggest 1–3 realistic next steps. "
        "Keep answers short, clear, and non-preachy."
    )

    user_context = (
        f"User message: {message}\n\n"
        f"Detected intent: {intent}.\n"
        f"{emission_context or 'No numeric emission estimate available.'}\n\n"
        "Based on this, explain the impact in simple terms and give actionable suggestions."
    )

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
    except Exception as e:
        # Fallback so the API never fully breaks
        return (
            "I had an issue calling the AI backend, but here’s a rough guideline: "
            f"your situation seems related to {intent}. "
            "Try reducing frequency, switching to a lower-carbon alternative, "
            "and tracking your change for a week."
        )
