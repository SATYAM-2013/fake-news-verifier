# utils/decision.py

from utils.medical_rules import is_medical_claim

def final_decision(ml_result, fact_result):
    ml_label = ml_result.get("label", "").lower()
    confidence = ml_result.get("confidence", 0)
    sources = fact_result.get("sources", [])
    evidence = fact_result.get("verdict")  # supports / contradicts / none

    # 1️⃣ Fact-check overrides everything
    if evidence == "contradicts":
        return {
            "verdict": "Fake News",
            "reason": "Verified fact-check sources contradict this claim.",
            "sources": sources
        }

    if evidence == "supports":
        return {
            "verdict": "Likely True News",
            "reason": "Verified fact-check sources support this claim.",
            "sources": sources
        }

    # 2️⃣ No external evidence found
    if not sources:
        # If ML is very confident
        if confidence >= 0.90:
            if ml_label == "fake":
                return {
                    "verdict": "Fake News",
                    "reason": "High-confidence AI prediction with no supporting evidence found.",
                    "sources": []
                }
            else:
                return {
                    "verdict": "Likely True News",
                    "reason": "High-confidence AI prediction. No contradicting evidence found.",
                    "sources": []
                }

        # Otherwise uncertain
        return {
            "verdict": "Uncertain",
            "reason": "Insufficient evidence and low AI confidence.",
            "sources": []
        }

    # 3️⃣ Fallback
    return {
        "verdict": "Uncertain",
        "reason": "Unable to determine with available information.",
        "sources": sources
    }