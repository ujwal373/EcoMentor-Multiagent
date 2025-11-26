import re
from typing import Optional

POSITIVE_PATTERNS = {
    "tree_planting": ["planted", "tree", "trees", "sapling"],
    "positive_transport": ["cycled", "bike", "biking", "cycling"],
    "public_transport": ["bus", "tram", "train", "lrt", "public transport"],
    "energy_reduction": ["reduced electricity", "energy saving", "saved energy"],
    "renewable_energy": ["solar", "renewable", "green energy", "wind power"],
    "waste_reduction": ["compost", "composted", "food waste", "reduced waste"],
    "local_food_choice": ["local produce", "seasonal food", "bought local"]
}

NEGATIVE_PATTERNS = {
    "negative_transport": ["drive", "car", "bus", "km", "transport"],
    "negative_energy": ["kwh", "electricity", "energy", "appliance"],
    "negative_food": ["food", "meal", "diet", "meat", "vegan"],
    "negative_waste": ["trash", "garbage", "recycle", "plastic"],
    "negative_local": ["imported", "global", "far away", "non-local"]
}

def detect_intent(message: str) -> str:
    text = message.lower()
    if any(w in text for w in ["drive", "car", "bus", "km", "transport"]):
        return "transport"
    if any(w in text for w in ["kwh", "electricity", "energy", "appliance"]):
        return "electricity"
    if any(w in text for w in ["food", "meal", "diet", "meat", "vegan"]):
        return "food"
    return "general"
    # Positive action detection
    for intent, keywords in POSITIVE_PATTERNS.items():
        if any(k in text for k in keywords):
            return intent
    # Negative action detection
    for intent, keywords in NEGATIVE_PATTERNS.items():
        if any(k in text for k in keywords):
            return intent
    return "general"

def extract_numeric_value(message: str) -> Optional[float]:
    m = re.search(r"(\d+(\.\d+)?)", message)
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None
