import os
import requests

API_KEY = os.getenv("FACT_CHECK_API_KEY")

if not API_KEY:
    raise RuntimeError("FACT_CHECK_API_KEY not set")

url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

params = {
    "query": "salt water cures cancer",
    "key": API_KEY,
    "languageCode": "en"
}

response = requests.get(url, params=params)
data = response.json()

print("Keys:", data.keys())
print("Claims found:", len(data.get("claims", [])))
