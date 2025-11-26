from config import get_openai_client, OPENAI_MODEL
from agents.metrics_agent import calculate_sustainability_score

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = get_openai_client()
    return _client



def build_response(ctx: dict) -> str:
    score = ctx.get("sustainability_score", 50)
    if score >= 75:
        sis_reaction = "🌟 Excellent sustainability levels! You're making a strong positive impact."
    elif score >= 25:
        sis_reaction = "💚 Good progress! You're improving steadily — keep going."
    else:
        sis_reaction = "⚠️ You're on the right path — small consistent changes will boost your score."
    system_prompt = (
        "You are EcoMentor, a sustainability coach. "
        "Use the structured context to explain the user's impact and give "
        "1–3 practical, non-preachy suggestions. Be concise."
    )

    emission_line = (
        f"Estimated emission for this activity: "
        f"{ctx['emission_kg']} kg CO₂e in category '{ctx['intent']}'."
        if ctx.get("emission_kg") is not None
        else "No precise emission estimate was available for this message."
    )

    weekly = ctx.get("weekly_summary", {})
    weekly_line = (
        f"Over the last week, total discussed emissions are "
        f"{weekly.get('weekly_total_kg', 0)} kg CO₂e "
        f"with breakdown {weekly.get('breakdown', {})}."
    )

    metrics = ctx.get("metrics", {})
    metrics_line = (
        f"So far, the system has handled {metrics.get('total_queries', 0)} queries, "
        f"with category counts {metrics.get('category_counts', {})}."
    )

    user_context = (
    f"User message: {ctx['message']}\n\n"
    f"SIS Score Reaction: {sis_reaction}\n"
    f"Detected intent: {ctx['intent']}, numeric_value={ctx['numeric']}.\n"
    f"{emission_line}\n\n"
    f"Session summary: {ctx.get('session_summary_text')}\n"
    f"Weekly summary: {weekly_line}\n"
    f"System metrics snapshot: {metrics_line}\n"
    "Now respond directly to the user with positivity and personalized guidance."
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
    except Exception:
        return (
            "I had an issue generating a detailed report, but broadly: focus on "
            "your highest-emission activities first (usually transport, energy, "
            "and food) and make one small, consistent change this week."
        )
