def mentor_reply(message: str) -> str:
    # Basic placeholder logic — will later call OpenAI LLM + other agents
    if "car" in message.lower():
        return "Driving emits roughly 2.3 kg CO₂ per 10 km. Try public transport or carpooling."
    elif "electricity" in message.lower():
        return "Reducing appliance standby use can cut ~5% of household energy emissions."
    else:
        return "Let's explore where your biggest emissions come from — transport, food, or energy?"
