import os
import requests
import re
from dotenv import load_dotenv
from utils.cache import get_fact_cache, set_fact_cache

load_dotenv()

API_KEY = os.getenv("FACT_CHECK_API_KEY")
API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

TRUSTED_PUBLISHERS = [
    "who.int",
    "cdc.gov",
    "reuters.com",
    "apnews.com",
    "bbc.com",
    "fullfact.org",
    "factcheck.afp.com",
    "politifact.com"
]


# -------------------------------------------------
# Text Normalization
# -------------------------------------------------
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text


# -------------------------------------------------
# Extract Short Query (Improves API Match)
# -------------------------------------------------
def extract_main_claim(text: str) -> str:
    words = text.split()
    return " ".join(words[:12])


# -------------------------------------------------
# Relevance Check
# -------------------------------------------------
def is_relevant_claim(user_text: str, fact_claim_text: str) -> bool:
    if not fact_claim_text:
        return False

    user_words = set(normalize_text(user_text).split())
    fact_words = set(normalize_text(fact_claim_text).split())

    overlap = user_words.intersection(fact_words)

    return len(overlap) >= 2


# -------------------------------------------------
# Rating Classification
# -------------------------------------------------
def classify_rating(rating: str):
    rating = rating.lower()

    if any(word in rating for word in [
        "true", "correct", "accurate", "mostly true"
    ]):
        return "support"

    if any(word in rating for word in [
        "false", "incorrect", "misleading",
        "pants on fire", "mostly false"
    ]):
        return "contradict"

    return "neutral"


# -------------------------------------------------
# Detect Negation
# -------------------------------------------------
def has_negation(text: str) -> bool:
    text = normalize_text(text)
    return any(word in text for word in [
        "not", "no", "never", "doesnt", "does not"
    ])


# -------------------------------------------------
# Main Fact Check Function
# -------------------------------------------------
def fact_check_claim(text: str):
    """
    Returns:
    {
        verdict: supports | contradicts | mixed | none
        sources: [urls]
    }
    """

    cached = get_fact_cache(text)
    if cached:
        return cached

    if not API_KEY:
        return {"verdict": "none", "sources": []}

    simplified_query = extract_main_claim(text)

    params = {
        "query": simplified_query,
        "key": API_KEY,
        "languageCode": "en"
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return {"verdict": "none", "sources": []}

    claims = data.get("claims", [])
    if not claims:
        return {"verdict": "none", "sources": []}

    support = 0
    contradict = 0
    sources = []

    user_negation = has_negation(text)

    for claim in claims:
        fact_claim_text = claim.get("text", "")

        if not is_relevant_claim(text, fact_claim_text):
            continue

        fact_negation = has_negation(fact_claim_text)

        for review in claim.get("claimReview", []):
            url = review.get("url", "")
            rating = review.get("textualRating", "")

            if not any(pub in url for pub in TRUSTED_PUBLISHERS):
                continue

            classification = classify_rating(rating)

            if classification == "neutral":
                continue

            # Polarity-aware scoring
            if classification == "contradict":
                if user_negation == fact_negation:
                    contradict += 1
                else:
                    support += 1

            elif classification == "support":
                if user_negation == fact_negation:
                    support += 1
                else:
                    contradict += 1

            sources.append(url)

    # Final verdict
    if support > contradict and support > 0:
        verdict = "supports"
    elif contradict > support and contradict > 0:
        verdict = "contradicts"
    elif support == 0 and contradict == 0:
        verdict = "none"
    else:
        verdict = "mixed"

    result = {
        "verdict": verdict,
        "sources": list(set(sources))
    }

    set_fact_cache(text, result)
    return result