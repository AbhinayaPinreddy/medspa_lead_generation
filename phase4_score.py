import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASEROW_API = os.getenv("BASEROW_API_KEY")
TABLE_ID = os.getenv("TABLE_ID")

HEADERS = {
    "Authorization": f"Token {BASEROW_API}",
    "Content-Type": "application/json"
}


# def get_rows():
#     url = f"https://api.baserow.io/api/database/rows/table/{TABLE_ID}/?user_field_names=true"
#     res = requests.get(url, headers=HEADERS)
#     return res.json().get("results", [])
def get_rows():
    all_rows = []
    url = f"https://api.baserow.io/api/database/rows/table/{TABLE_ID}/?user_field_names=true"

    while url:
        try:
            res = requests.get(url, headers=HEADERS)
            data = res.json()

            results = data.get("results", [])
            all_rows.extend(results)

            url = data.get("next")  # 🔥 go to next page

        except Exception as e:
            print("❌ Error fetching rows:", e)
            break

    print(f"✅ Total rows fetched: {len(all_rows)}")
    return all_rows


def calculate_score(row):
    score = 0

    if row.get("qualification_status") == "pass":
        score += 50

    if row.get("emails"):
        score += 20

    if row.get("instagram"):
        score += 10

    try:
        rating = float(row.get("rating", 0))
        if rating >= 4.5:
            score += 10
    except:
        pass

    return score


def update_row(row_id, score):
    url = f"https://api.baserow.io/api/database/rows/table/{TABLE_ID}/{row_id}/?user_field_names=true"

    data = {
        "lead_score": score
    }

    requests.patch(url, json=data, headers=HEADERS)


def run_phase_4():
    print("🚀 Phase 4: Lead Scoring")

    rows = get_rows()

    for row in rows:
        if row.get("lead_score"):
            continue

        score = calculate_score(row)

        update_row(row["id"], score)

        print(row.get("name"), "→ Score:", score)


if __name__ == "__main__":
    run_phase_4()