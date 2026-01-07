from utils.decision import final_decision

def test_medical_claim_without_sources_is_fake():
    ml_result = {
        "label": "fake",
        "confidence": 0.8,
        "text": "Salt water cures cancer"
    }
    fact_result = {"sources": []}

    decision = final_decision(ml_result, fact_result)

    assert decision["verdict"] == "Fake News"


def test_claim_with_fact_sources_is_true():
    ml_result = {
        "label": "fake",
        "confidence": 0.4,
        "text": "Covid vaccines cause infertility"
    }
    fact_result = {
        "sources": ["https://fullfact.org/example"]
    }

    decision = final_decision(ml_result, fact_result)

    assert decision["verdict"] == "Likely True News"


def test_high_confidence_fake_ai():
    ml_result = {
        "label": "fake",
        "confidence": 0.9,
        "text": "Miracle cure discovered"
    }
    fact_result = {"sources": []}

    decision = final_decision(ml_result, fact_result)

    assert decision["verdict"] == "Fake News"


def test_low_confidence_uncertain():
    ml_result = {
        "label": "uncertain",
        "confidence": 0.45,
        "text": "Scientists are studying a new phenomenon"
    }
    fact_result = {"sources": []}

    decision = final_decision(ml_result, fact_result)

    assert decision["verdict"] == "Uncertain"
