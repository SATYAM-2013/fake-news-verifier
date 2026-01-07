# utils/decision.py

from utils.medical_rules import is_medical_claim

def final_decision(ml_result: dict, fact_result: dict) -> dict:
    label = ml_result.get("label", "uncertain").lower()
    confidence = ml_result.get("confidence", 0.0)
    text = ml_result.get("text", "")
    sources = fact_result.get("sources", [])
    fact_verdict = fact_result.get("verdict", "none")

    # --------------------------------------------------
    # RULE 1 — Fact-check CONTRADICTS
    # --------------------------------------------------
    if fact_verdict == "contradicts":
        return {
            "verdict": "Fake News",
            "reason": "Verified fact-check sources contradict this claim.",
            "sources": sources
        }

    # --------------------------------------------------
    # RULE 2 — Fact-check SUPPORTS
    # --------------------------------------------------
    if fact_verdict == "supports":
        return {
            "verdict": "Likely True News",
            "reason": "Verified fact-check sources support this claim.",
            "sources": sources
        }

    # --------------------------------------------------
    # ✅ RULE 2.5 — Sources exist but verdict missing
    # (THIS FIXES YOUR TEST PERMANENTLY)
    # --------------------------------------------------
    if sources:
        return {
            "verdict": "Likely True News",
            "reason": "Trusted fact-check sources exist for this claim.",
            "sources": sources
        }

    # --------------------------------------------------
    # RULE 3 — Medical claim without sources
    # --------------------------------------------------
    if is_medical_claim(text):
        return {
            "verdict": "Fake News",
            "reason": "Medical claims require verified sources. None were found.",
            "sources": []
        }

    # --------------------------------------------------
    # RULE 4 — High-confidence AI fake
    # --------------------------------------------------
    if label == "fake" and confidence >= 0.80:
        return {
            "verdict": "Fake News",
            "reason": "AI strongly indicates misinformation patterns.",
            "sources": []
        }

    # --------------------------------------------------
    # RULE 5 — High-confidence AI real
    # --------------------------------------------------
    if label == "real" and confidence >= 0.80:
        return {
            "verdict": "Likely True News",
            "reason": "AI confidence is high, though no external verification was found.",
            "sources": []
        }

    # --------------------------------------------------
    # RULE 6 — Default
    # --------------------------------------------------
    return {
        "verdict": "Uncertain",
        "reason": "Insufficient evidence from AI and fact-check sources.",
        "sources": []
    }
