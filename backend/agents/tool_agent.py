MOCK_FACTORS = {
    "transport": 0.21,  # kg CO₂ per km
    "electricity": 0.4,  # kg CO₂ per kWh
    "food": 2.0          # kg CO₂ per meal (approx)
}

def calculate_emission(category: str, value: float) -> dict:
    factor = MOCK_FACTORS.get(category.lower(), 0.3)
    emission = round(value * factor, 2)
    return {"category": category, "value": value, "emission_kg": emission}
