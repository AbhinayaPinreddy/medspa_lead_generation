import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASEROW_API = os.getenv("BASEROW_API_KEY")
TABLE_ID = os.getenv("TABLE_ID")


def save_to_baserow(business):
    url = f"https://api.baserow.io/api/database/rows/table/{TABLE_ID}/?user_field_names=true"

    headers = {
        "Authorization": f"Token {BASEROW_API}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=business, headers=headers)

    if response.status_code not in [200, 201]:
        print("❌ Baserow Error:", response.text)
    else:
        print("📥 Added to Baserow:", business.get("name"))