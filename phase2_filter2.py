import requests
import os
import time
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

BASEROW_API = os.getenv("BASEROW_API_KEY")
TABLE_ID = os.getenv("TABLE_ID")

HEADERS = {
    "Authorization": f"Token {BASEROW_API}",
    "Content-Type": "application/json"
}

RF_KEYWORDS = [
    "rf microneedling",
    "radiofrequency microneedling",
    "morpheus8",
    "potenza",
    "sylfirm"
]

FAT_KEYWORDS = [
    "kybella",
    "fat reduction",
    "double chin",
    "jawline slimming",
    "submental fat",
    "deoxycholic acid",
    "neck fat",
    "face fat",
    "face fat reduction"
]


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
            return requests.get(url, timeout=6, verify=False).text.lower()
        except:
            continue
    return ""


def check_qualification(base_url, extra_text=""):
    pages = [
        base_url,
        base_url + "/services",
        base_url + "/treatments",
        base_url + "/procedures"
    ]

    full_text = extra_text.lower()
    sources = ["google"]

    for page in pages:
        html = safe_request(page)
        if html:
            full_text += html
            sources.append("website")

    found_rf = [k for k in RF_KEYWORDS if k in full_text]
    found_fat = [k for k in FAT_KEYWORDS if k in full_text]

    status = "pass" if (found_rf and found_fat) else "fail"

    confidence = (
        "high" if found_rf and found_fat else
        "medium" if (found_rf or found_fat) else
        "low"
    )

    return status, ", ".join(found_rf + found_fat), ", ".join(set(sources)), confidence


def update_row(row_id, status, keywords, sources, confidence):
    url = f"https://api.baserow.io/api/database/rows/table/{TABLE_ID}/{row_id}/?user_field_names=true"

    payload = {
        "qualification_status": status,
        "matched_keywords": keywords or "none",
        "sources_checked": sources,
        "confidence_note": confidence
    }

    requests.patch(url, json=payload, headers=HEADERS)


def run_phase_2():
    print("🚀 Phase 2")

    rows = get_rows()

    for row in rows:
        try:
            if row.get("qualification_status"):
                continue

            website = row.get("website")

            if not website:
                update_row(row["id"], "fail", "no_website", "none", "low")
                continue

            extra_text = str(row.get("name", "")) + " " + str(row.get("address", ""))

            status, keywords, sources, confidence = check_qualification(website, extra_text)

            update_row(row["id"], status, keywords, sources, confidence)

            print(row.get("name"), "→", status)

            time.sleep(1)

        except Exception as e:
            print("⚠️ Error:", e)
            continue


if __name__ == "__main__":
    run_phase_2()