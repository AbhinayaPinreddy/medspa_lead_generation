import requests
import re
import os
import time
from urllib.parse import urljoin
from dotenv import load_dotenv
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

BASEROW_API = os.getenv("BASEROW_API_KEY")
TABLE_ID = os.getenv("TABLE_ID")

HEADERS = {
    "Authorization": f"Token {BASEROW_API}",
    "Content-Type": "application/json"
}


def get_rows():
    all_rows = []
    url = f"https://api.baserow.io/api/database/rows/table/{TABLE_ID}/?user_field_names=true"

    while url:
        res = requests.get(url, headers=HEADERS)
        data = res.json()
        all_rows.extend(data.get("results", []))
        url = data.get("next")

    print(f"✅ Total rows fetched: {len(all_rows)}")
    return all_rows


def safe_request(url):
    for _ in range(2):
        try:
            return requests.get(url, timeout=6, verify=False).text
        except:
            continue
    return ""


def extract_emails(html):
    return set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", html))


def extract_instagram(html):
    match = re.findall(r"https?://(?:www\.)?instagram\.com/[^\s\"']+", html)
    return match[0].split("?")[0] if match else ""


def extract_data(base_url):
    emails = set()
    instagram = ""

    pages = [
        base_url,
        urljoin(base_url, "/contact"),
        urljoin(base_url, "/about")
    ]

    for page in pages:
        html = safe_request(page)

        if not html:
            continue

        emails.update(extract_emails(html))

        if not instagram:
            instagram = extract_instagram(html)

    return {
        "emails": ", ".join(list(emails)[:3]),
        "instagram": instagram,
        "email_source": "website" if emails else "none",
        "enrichment_status": "success" if (emails or instagram) else "failed",
        "enrichment_date": datetime.now().strftime("%Y-%m-%d")
    }


def update_row(row_id, data):
    url = f"https://api.baserow.io/api/database/rows/table/{TABLE_ID}/{row_id}/?user_field_names=true"

    payload = {
        "enrichment_status": data.get("enrichment_status", "failed"),
        "enrichment_date": data.get("enrichment_date"),
        "email_source": data.get("email_source", "none")
    }

    if data.get("emails"):
        payload["emails"] = data["emails"]

    if data.get("instagram"):
        payload["instagram"] = data["instagram"]

    requests.patch(url, json=payload, headers=HEADERS)


def run_phase_3():
    print("🚀 Phase 3")

    rows = get_rows()

    for row in rows:
        try:
            # 🔥 HANDLE NOT QUALIFIED
            if row.get("qualification_status") != "pass":
                update_row(row["id"], {
                    "enrichment_status": "skipped",
                    "enrichment_date": datetime.now().strftime("%Y-%m-%d"),
                    "email_source": "none"
                })
                continue

            if row.get("enrichment_status"):
                continue

            website = row.get("website")

            if not website:
                update_row(row["id"], {
                    "enrichment_status": "no_website",
                    "enrichment_date": datetime.now().strftime("%Y-%m-%d"),
                    "email_source": "none"
                })
                continue

            print("Processing:", row.get("name"))

            data = extract_data(website)

            update_row(row["id"], data)

            time.sleep(1)

        except Exception as e:
            print("⚠️ Error:", e)
            continue


if __name__ == "__main__":
    run_phase_3()