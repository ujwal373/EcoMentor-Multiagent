from agents.intent_agent import detect_intent, extract_numeric_value
from agents.tool_agent import calculate_emission
from agents.memory_agent import update_session, session_summary, weekly_summary
from agents.metrics_agent import log_metrics, get_metrics
from agents.reporter_agent import build_response
from agents.metrics_agent import calculate_sustainability_score

def handle_message(message: str, session_id: str = "default") -> dict:
    # SIS score
    metrics = get_metrics()
    weekly = weekly_summary(session_id)
    score = calculate_sustainability_score(metrics, weekly["weekly_total_kg"])

    # 1) Intent + value
    intent = detect_intent(message)
    numeric = extract_numeric_value(message)

    # 2) Tool agent (emission)
    emission = None
    if intent in {"transport", "electricity", "food"} and numeric is not None:
        calc = calculate_emission(intent, numeric)
        emission = calc["emission_kg"]
    else:
        calc = None

    # 3) Memory agent
    interaction = {
        "intent": intent,
        "message": message,
        "numeric": numeric,
        "emission_kg": emission,
    }
    update_session(session_id, interaction)
    sess_summary = session_summary(session_id)
    weekly = weekly_summary(session_id)

    # 4) Metrics agent
    metrics = log_metrics(session_id, intent, emission)

    # 5) Reporter agent (LLM)
    context = {
        "message": message,
        "session_id": session_id,
        "intent": intent,
        "numeric": numeric,
        "emission_kg": emission,
        "session_summary_text": sess_summary,
        "weekly_summary": weekly,
        "metrics": metrics,
        "sustainability_score": score,
    }
    text = build_response(context)

    # trace is handy for debugging / Kaggle writeup
    trace = {
        "intent": intent,
        "numeric": numeric,
        "emission_calc": calc,
        "session_summary": sess_summary,
        "weekly_summary": weekly,
    }
    return {"text": text, "trace": trace}
