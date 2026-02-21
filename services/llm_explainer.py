from utils.cache import get_llm_cache, set_llm_cache

def explain_decision(text, verdict, ml_label, confidence, sources):

    verdict_lower = verdict.lower()
    ml_lower = ml_label.lower()

    # Case 1: Fact-check contradicts
    if verdict_lower == "fake news" and sources:
        return (
            f"The ML model predicted '{ml_label}' "
            f"(confidence: {confidence:.2f}). "
            f"Verified external fact-check sources contradict this claim. "
            f"According to the evidence-first policy, the final verdict is "
            f"'{verdict}'."
        )

    # Case 2: Fact-check supports
    if verdict_lower == "likely true news" and sources:
        return (
            f"The ML model predicted '{ml_label}' "
            f"(confidence: {confidence:.2f}). "
            f"Verified external fact-check sources support this claim. "
            f"According to the evidence-first policy, the final verdict is "
            f"'{verdict}'."
        )

    # Case 3: No external evidence
    return (
        f"The ML model predicted '{ml_label}' "
        f"(confidence: {confidence:.2f}). "
        f"No verified external fact-check sources were found. "
        f"The final verdict is '{verdict}'."
    )