import re

MEDICAL_KEYWORDS = [
    "cancer", "diabetes", "covid", "vaccine", "cure",
    "treatment", "medicine", "health", "disease"
]

def is_medical_claim(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in MEDICAL_KEYWORDS)
