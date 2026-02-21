from utils.cache import get_llm_cache, set_llm_cache

def explain_decision(text, verdict, ml_label, confidence, sources):
    """
    Generates structured explanation for the final decision.
    """

    if sources and verdict.lower() != ml_label.lower():
        explanation = (
            f"The ML model predicted '{ml_label}' "
            f"(confidence: {confidence:.2f}). "
            f"However, verified external fact-check sources support this claim. "
            f"According to the evidence-first policy, the final verdict is '{verdict}'."
        )

    elif sources:
        explanation = (
            f"The ML model predicted '{ml_label}' "
            f"(confidence: {confidence:.2f}). "
            f"Verified fact-check sources align with this prediction. "
            f"The final verdict is '{verdict}'."
        )

    else:
        explanation = (
            f"The ML model predicted '{ml_label}' "
            f"(confidence: {confidence:.2f}). "
            f"No verified external evidence was found, so the verdict is based on the model's prediction."
        )

    return explanation