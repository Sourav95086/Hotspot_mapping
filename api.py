from fastapi import FastAPI, HTTPException

from thematic.supabase_client import fetch_issue, supabase
from anomaly_detecter.anomaly_agent import detect_civic_issue
from thematic.thematic_agent import classify_issue

from category_service import (
    get_or_create_category,
    update_city_category_count
)

from hotspot_service import classify_hotspots


app = FastAPI(
    title="Civic Issue Analysis API",
    description="Anomaly detection and thematic pattern recognition",
    version="1.0.0"
)


@app.get("/")
def root():

    return {
        "success": True,
        "message": "Civic Issue Analysis API is running"
    }


# ==========================================
# ANALYZE ONE ISSUE
# ==========================================

@app.post("/analyze/{issue_id}")
def analyze_issue(issue_id: int):

    result = fetch_issue(issue_id)

    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    issue = result["issue"]

    description = issue["issue_description"]
    city = issue["issue_location"]


    # Anomaly detection

    anomaly_result = detect_civic_issue(
        description
    )


    # Not a civic issue

    if not anomaly_result.is_civic_issue:

        return {
            "success": True,
            "issue_id": issue_id,
            "issue_description": description,
            "is_civic_issue": False,
            "issue_category": None
        }


    # Thematic recognition

    theme_result = classify_issue(
        description
    )

    category_name = theme_result.issue_category


    # Category management

    category_result = get_or_create_category(
        category_name
    )

    category_id = category_result["category_id"]


    # City + category count

    count_result = update_city_category_count(
        city,
        category_id
    )


    return {
        "success": True,
        "issue_id": issue_id,
        "issue_description": description,
        "is_civic_issue": True,
        "issue_category": category_result["category_name"],
        "category_id": category_id,
        "category_created": category_result["created"],
        "city": city,
        "report_count": count_result["report_count"]
    }


# ==========================================
# ROUTE 1
# Category class for a city
# ==========================================

@app.get("/hotspots/{city}")
def get_city_hotspots(city: str):

    return classify_hotspots(city)


# ==========================================
# ROUTE 2
# Issues for a specific city + category
# ==========================================

@app.get("/hotspots/{city}/{category_id}/issues")
def get_category_issues(
    city: str,
    category_id: int
):

    response = (
        supabase
        .table("issue_reports")
        .select(
            "issue_id, issue_description, "
            "issue_location, latitude, longitude, category_id"
        )
        .eq("issue_location", city)
        .eq("category_id", category_id)
        .execute()
    )

    reports = response.data

    results = []

    for report in reports:

        issue_id = report["issue_id"]

        # Fetch weight from issues table

        weight_response = (
            supabase
            .table("issues")
            .select("issue_weight")
            .eq("issue_id", issue_id)
            .maybe_single()
            .execute()
        )

        issue_weight = None

        if weight_response.data:
            issue_weight = weight_response.data["issue_weight"]


        results.append({
            "issue_id": issue_id,
            "issue_description": report["issue_description"],
            "issue_location": report["issue_location"],
            "category_id": report["category_id"],
            "latitude": report["latitude"],
            "longitude": report["longitude"],
            "issue_weight": issue_weight
        })


    return {
        "success": True,
        "city": city,
        "category_id": category_id,
        "total_issues": len(results),
        "issues": results
    }