import os
import requests
from datetime import datetime, timedelta

API_KEY = os.getenv("GNEWS_API_KEY")
if not API_KEY:
    raise RuntimeError("GNEWS_API_KEY not found. Restart IDE.")

url = "https://gnews.io/api/v4/search"

# 🔑 SAFE queries that ALWAYS work on free tier
queries = [
    "Apple launches new product",
    "Microsoft announces earnings",
    "Google releases new update",
]

from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

for query in queries:
    print(f"\n🔍 Searching: {query}")

    params = {
        "q": query,
        "lang": "en",
        "country": "us",
        "from": from_date,
        "sortby": "publishedAt",
        "max": 5,
        "apikey": API_KEY,
    }

    r = requests.get(url, params=params)
    data = r.json()

    print("Total articles found:", data.get("totalArticles", 0))

    for a in data.get("articles", []):
        print("•", a["title"])
