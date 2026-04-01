from baserow import save_to_baserow
from phase1_fetch2 import fetch_medspas, clean_data


def run_phase_1():
    print("🚀 RUNNING MAIN FILE")

    raw_data = fetch_medspas()

    print("AFTER FETCH ✅")

    # 🔥 FIXED VALIDATION
    if raw_data is None:
        print("❌ No data fetched (None).")
        return

    if not isinstance(raw_data, list):
        print("❌ Unexpected data format:", type(raw_data))
        return

    if len(raw_data) == 0:
        print("⚠️ Empty list returned from API")
        return

    # 🔥 DEBUG
    print("DEBUG main → type:", type(raw_data))
    print("DEBUG main → length:", len(raw_data))

    print("Sample name:", raw_data[0].get("title"))

    businesses = clean_data(raw_data)

    print("✅ Cleaned businesses:", len(businesses))

    for business in businesses:
        if not business.get("place_id"):
            continue

        save_to_baserow(business)
        print("✅ Saved:", business.get("name"))


if __name__ == "__main__":
    run_phase_1()