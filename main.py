from thematic.supabase_client import fetch_issue
from anomaly_detecter.anomaly_agent import detect_civic_issue
from thematic.thematic_agent import classify_issue
from category_service import (
    get_or_create_category,
    update_city_category_count
)


def process_issue(issue_id: int):

    # 1. Fetch issue
    result = fetch_issue(issue_id)

    if not result["success"]:
        return result

    issue = result["issue"]

    description = issue["issue_description"]
    city = issue["issue_location"]

    # 2. Anomaly detection
    anomaly_result = detect_civic_issue(description)

    if not anomaly_result.is_civic_issue:
        return {
            "success": True,
            "issue_id": issue_id,
            "is_civic_issue": False,
            "issue_category": None
        }

    # 3. Thematic recognition
    theme_result = classify_issue(description)

    category_name = theme_result.issue_category

    # Get or create the category
    category_result = get_or_create_category(
        category_name
    )

    # Get the category ID
    category_id = category_result["category_id"]

    # Update city + category count
    count_result = update_city_category_count(
        city,
        category_id
        )

    # 5. Final result
    return {
        "success": True,
        "issue_id": issue_id,
        "is_civic_issue": True,
        "issue_category": category_name,
        "category_id": category_result["category_id"],
        "category_created": category_result["created"],
        "city": city,
        "report_count": count_result["report_count"]
    }


if __name__ == "__main__":

    issue_id = 1

    result = process_issue(issue_id)

    print("\n========== FINAL RESULT ==========\n")

    print(result)