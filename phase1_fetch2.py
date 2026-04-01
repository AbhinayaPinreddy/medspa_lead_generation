import requests
import os
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")

APIFY_URL = "https://api.apify.com/v2/acts/compass~crawler-google-places/run-sync-get-dataset-items"


def fetch_medspas():
    headers = {
        "Authorization": f"Bearer {APIFY_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "searchStringsArray": [
            "medspa Los Angeles",
            "medspa Beverly Hills",
            "medspa Santa Monica",
            "medspa San Diego",
            "medspa San Francisco",
            "medspa Houston",
            "medspa Dallas",
            "medspa Austin",
            "medspa Miami",
            "medspa Chicago"
        ],
        "maxCrawledPlacesPerSearch": 30
    }

    print("📡 Calling Apify Actor...")

    response = requests.post(APIFY_URL, json=payload, headers=headers)

    print("Status Code:", response.status_code)

    if not response.ok:
        print("❌ ERROR FROM APIFY:", response.status_code, response.text)
        return []

    try:
        data = response.json()
    except Exception as e:
        print("❌ JSON Error:", e)
        return []

    if not isinstance(data, list):
        print("❌ Unexpected response format")
        return []

    print("✅ Fetched:", len(data))

    return data


def clean_data(data):
    businesses = []
    seen_ids = set()

    for item in data:
        name = item.get("title") or item.get("name")
        place_id = item.get("placeId")

        if not name or not place_id:
            continue

        # 🔥 Deduplication
        if place_id in seen_ids:
            continue
        seen_ids.add(place_id)

        country = str(item.get("countryCode", "")).upper()
        if country and country != "US":
            continue

        category = str(item.get("categoryName", "")).lower()
        categories = " ".join(item.get("categories", [])).lower()
        combined = category + " " + categories

        if not any(k in combined for k in ["spa", "clinic", "aesthetic"]):
            continue

        business = {
            "name": name,
            "address": item.get("address"),
            "phone": item.get("phone") or item.get("phoneUnformatted"),
            "website": item.get("website"),
            "place_id": place_id,
            "rating": item.get("rating") or item.get("totalScore"),
            "reviews_count": item.get("reviewsCount"),
            "maps_url": item.get("url")
        }

        businesses.append(business)

    return businesses