def final_decision(ml_result, fact_result):

    ml_label = ml_result.get("label", "").lower()
    confidence = ml_result.get("confidence", 0)

    evidence = fact_result.get("verdict", "none")
    sources = fact_result.get("sources", [])

    # 1️⃣ Fact-check override
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

    # 2️⃣ No fact-check evidence
    # Lower threshold from 0.90 → 0.65
    if not sources:

        if confidence >= 0.65:
            if ml_label == "fake":
                return {
                    "verdict": "Fake News",
                    "reason": "AI prediction (moderate-to-high confidence). No external contradiction found.",
                    "sources": []
                }
            else:
                return {
                    "verdict": "Likely True News",
                    "reason": "AI prediction (moderate-to-high confidence). No contradicting evidence found.",
                    "sources": []
                }

        # Very low confidence
        return {
            "verdict": "Uncertain",
            "reason": "Low AI confidence and no external fact-check evidence.",
            "sources": []
        }

    # 3️⃣ Mixed evidence fallback
    return {
        "verdict": "Uncertain",
        "reason": "Conflicting or insufficient external information.",
        "sources": sources
    }