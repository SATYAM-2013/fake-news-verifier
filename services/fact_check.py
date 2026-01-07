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


def fact_check_claim(text: str):
    cached = get_fact_cache(text)
    if cached:
        return cached

    """
    Returns:
    {
        verdict: supports | contradicts | mixed | none
        sources: [urls]
    }
    """

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

    claim_text = text.lower()
    negation = any(word in claim_text for word in ["not", "no", "never", "doesn't", "does not"])

    for claim in claims:
        for review in claim.get("claimReview", []):
            url = review.get("url", "")
            rating = review.get("textualRating", "").lower()

            if not any(pub in url for pub in TRUSTED_PUBLISHERS):
                continue

            sources.append(url)

            if rating in ["true", "correct", "accurate"]:
                support += 1

            elif rating in ["false", "incorrect", "pants on fire", "misleading"]:
                if negation:
                    support += 1
                else:
                    contradict += 1

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
    set_fact_cache(text, result)
    return result

    return {
        "verdict": verdict,
        "sources": list(set(sources))
    }
