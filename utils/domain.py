def detect_domain(text: str) -> str:
    text = text.lower()

    if any(word in text for word in ["cancer", "virus", "medicine", "health", "vitamin"]):
        return "health"

    if any(word in text for word in ["nasa", "planet", "space", "physics", "science"]):
        return "science"

    if any(word in text for word in ["election", "government", "minister", "policy"]):
        return "politics"

    return "general"
