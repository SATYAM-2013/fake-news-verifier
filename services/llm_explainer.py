from utils.cache import get_llm_cache, set_llm_cache

def explain_decision(text, verdict, ml_label, confidence, sources):
    cache_key = f"{text}|{verdict}|{ml_label}"

    cached = get_llm_cache(cache_key)
    if cached:
        return cached

    explanation = (
        f"The system classified this claim as '{verdict}'. "
        f"The AI model predicted '{ml_label}' with {confidence*100:.1f}% confidence. "
        f"Fact-check sources found: {len(sources)}."
    )

    set_llm_cache(cache_key, explanation)
    return explanation
