from thematic.supabase_client import supabase


def classify_hotspots(city: str):

    # ==========================================
    # 1. Get all category counts for this city
    # ==========================================

    count_response = (
        supabase
        .table("city_category_counts")
        .select("category_id, report_count")
        .eq("city", city)
        .order("category_id")
        .execute()
    )

    count_records = count_response.data or []

    results = []


    # ==========================================
    # 2. Get all reports from this city
    # ==========================================

    report_response = (
        supabase
        .table("issue_reports")
        .select("issue_id")
        .eq("issue_location", city)
        .execute()
    )

    city_reports = report_response.data or []

    city_issue_ids = [
        report["issue_id"]
        for report in city_reports
    ]


    # ==========================================
    # 3. Fetch issues for this city
    # ==========================================

    city_issues = []

    if city_issue_ids:

        issue_response = (
            supabase
            .table("issues")
            .select(
                "issue_id, issue_category, issue_weight"
            )
            .in_("issue_id", city_issue_ids)
            .execute()
        )

        city_issues = issue_response.data or []


    # ==========================================
    # 4. Process every category
    # ==========================================

    for record in count_records:

        category_id = record["category_id"]
        report_count = record["report_count"]


        # ==========================================
        # Get category name
        # ==========================================

        category_response = (
            supabase
            .table("issue_categories")
            .select("category_name")
            .eq("category_id", category_id)
            .maybe_single()
            .execute()
        )

        if not category_response.data:
            continue

        category_name = category_response.data["category_name"]


        # ==========================================
        # Find weights for this city + category
        # ==========================================

        weights = []

        for issue in city_issues:

            if issue["issue_category"] == category_name:

                if issue["issue_weight"] is not None:

                    weights.append(
                        float(issue["issue_weight"])
                    )


        # ==========================================
        # Calculate average weight
        # ==========================================

        if weights:

            average_weight = sum(weights) / len(weights)

        else:

            average_weight = 0


        # ==========================================
        # Calculate hotspot score
        # ==========================================

        hotspot_score = (
            report_count * average_weight
        )


        # ==========================================
        # Classify hotspot
        # ==========================================

        if hotspot_score > 350 :
            issue_class = "hotspot"

        elif hotspot_score > 200:
            issue_class = "moderate"

        else:
            issue_class = "low"


        # ==========================================
        # Add category result
        # ==========================================

        results.append({
            "category_id": category_id,
            "category_name": category_name,
            "city": city,
            "report_count": report_count,
            "average_weight": round(
                average_weight,
                2
            ),
            "hotspot_score": round(
                hotspot_score,
                2
            ),
            "class": issue_class
        })


    # ==========================================
    # Final response
    # ==========================================

    return {
        "success": True,
        "city": city,
        "categories": results
    }


if __name__ == "__main__":

    city = "Bhubaneswar"

    result = classify_hotspots(city)

    print(result)