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
# Extract Simplified Query (Improves API Results)
# -------------------------------------------------
def extract_main_claim(text: str) -> str:
    words = text.split()
    if len(words) > 12:
        return " ".join(words[:12])
    return text


# -------------------------------------------------
# Relevance Check (Smarter & Less Strict)
# -------------------------------------------------
def is_relevant_claim(user_text: str, fact_claim_text: str) -> bool:
    if not fact_claim_text:
        return False

    user_words = set(normalize_text(user_text).split())
    fact_words = set(normalize_text(fact_claim_text).split())

    overlap = user_words.intersection(fact_words)

    # Reduced threshold to avoid missing real claims
    return len(overlap) >= 3


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
# Fact Check Main Function
# -------------------------------------------------
def fact_check_claim(text: str):
    """
    Returns:
    {
        verdict: supports | contradicts | mixed | none
        sources: [urls]
    }
    """

    # ✅ Cache Check
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

    user_text_norm = normalize_text(text)

    for claim in claims:
        fact_claim_text = claim.get("text", "")

        if not is_relevant_claim(text, fact_claim_text):
            continue

        for review in claim.get("claimReview", []):
            url = review.get("url", "")
            rating = review.get("textualRating", "")

            # Only trusted sources
            if not any(pub in url for pub in TRUSTED_PUBLISHERS):
                continue

            classification = classify_rating(rating)

            if classification == "support":
                support += 1
                sources.append(url)

            elif classification == "contradict":
                contradict += 1
                sources.append(url)

    # -------------------------------------------------
    # Final Verdict Logic (Stable & Balanced)
    # -------------------------------------------------
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