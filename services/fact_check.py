import os
import requests
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
# Relevance Filter (Prevents False Overrides)
# -------------------------------------------------
def is_relevant_claim(user_text: str, fact_claim_text: str) -> bool:
    """
    Checks whether the fact-check claim text is actually
    relevant to the user's input claim.
    """
    if not fact_claim_text:
        return False

    user_words = set(user_text.lower().split())
    fact_words = set(fact_claim_text.lower().split())

    overlap = user_words.intersection(fact_words)

    # Require minimum overlap threshold
    return len(overlap) >= 5


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

    # ✅ Check cache first
    cached = get_fact_cache(text)
    if cached:
        return cached

    if not API_KEY:
        return {"verdict": "none", "sources": []}

    params = {
        "query": text,
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

    sources = []
    support = 0
    contradict = 0

    claim_text_lower = text.lower()

    # Detect negation in user claim
    negation = any(word in claim_text_lower for word in [
        "not", "no", "never", "doesn't", "does not"
    ])

    for claim in claims:

        fact_claim_text = claim.get("text", "")

        # ✅ Skip irrelevant fact-check claims
        if not is_relevant_claim(text, fact_claim_text):
            continue

        for review in claim.get("claimReview", []):

            url = review.get("url", "")
            rating = review.get("textualRating", "").lower()

            # ✅ Only allow trusted publishers
            if not any(pub in url for pub in TRUSTED_PUBLISHERS):
                continue

            sources.append(url)

            # Normalize rating
            if any(word in rating for word in ["true", "correct", "accurate"]):
                support += 1

            elif any(word in rating for word in ["false", "incorrect", "misleading", "pants on fire"]):
                # Handle negation logic
                if negation:
                    support += 1
                else:
                    contradict += 1

    # Determine final verdict
    if support > contradict:
        verdict = "supports"
    elif contradict > support:
        verdict = "contradicts"
    elif support == 0 and contradict == 0:
        verdict = "none"
    else:
        verdict = "mixed"

    result = {
        "verdict": verdict,
        "sources": list(set(sources))
    }

    # Cache result
    set_fact_cache(text, result)

    return result