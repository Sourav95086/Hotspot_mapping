from thematic.supabase_client import supabase


def classify_hotspots(city: str):

    response = (
        supabase
        .table("city_category_counts")
        .select("category_id, report_count")
        .eq("city", city)
        .execute()
    )

    records = response.data

    results = []

    for record in records:

        count = record["report_count"]

        if count >= 50:
            issue_class = "hotspot"

        elif count >= 20:
            issue_class = "moderate"

        else:
            issue_class = "low"

        results.append({
            "category_id": record["category_id"],
            "city": city,
            "class": issue_class
        })

    return {
        "success": True,
        "city": city,
        "categories": results
    }


if __name__ == "__main__":

    city = "KIIT Square"

    result = classify_hotspots(city)

    print(result)