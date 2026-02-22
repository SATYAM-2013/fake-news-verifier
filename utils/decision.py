from utils.medical_rules import is_medical_claim


def final_decision(ml_result, fact_result):

    ml_label = ml_result.get("label", "").lower()
    confidence = ml_result.get("confidence", 0)

    evidence = fact_result.get("verdict", "none")
    sources = fact_result.get("sources", [])

    # -----------------------------------------
    # 1️⃣ Fact-check overrides (if reliable)
    # -----------------------------------------
    if evidence == "contradicts" and sources:
        return {
            "verdict": "Fake News",
            "reason": "Verified fact-check sources contradict this claim.",
            "sources": sources
        }

    if evidence == "supports" and sources:
        return {
            "verdict": "Likely True News",
            "reason": "Verified fact-check sources support this claim.",
            "sources": sources
        }

    # -----------------------------------------
    # 2️⃣ No fact-check evidence found
    # -----------------------------------------
    if evidence == "none" or not sources:

        if confidence >= 0.90:
            if ml_label == "fake":
                return {
                    "verdict": "Fake News",
                    "reason": "High-confidence AI prediction. No contradicting evidence found.",
                    "sources": []
                }
            else:
                return {
                    "verdict": "Likely True News",
                    "reason": "High-confidence AI prediction. No contradicting evidence found.",
                    "sources": []
                }

        return {
            "verdict": "Uncertain",
            "reason": "Insufficient external evidence and moderate AI confidence.",
            "sources": []
        }

    # -----------------------------------------
    # 3️⃣ Mixed evidence
    # -----------------------------------------
    return {
        "verdict": "Uncertain",
        "reason": "Conflicting information detected from available sources.",
        "sources": sources
    }