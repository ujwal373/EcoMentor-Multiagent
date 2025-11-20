import re
from typing import Optional

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
