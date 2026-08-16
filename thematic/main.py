from supabase_client import fetch_issue
from anomaly_detecter.anomaly_agent import detect_civic_issue
from thematic.thematic_agent import classify_issue


def process_issue(issue_id: int):

    # ---------------------------------------
    # STEP 1: FETCH ISSUE FROM SUPABASE
    # ---------------------------------------

    result = fetch_issue(issue_id)

    if not result["success"]:
        return {
            "success": False,
            "issue_id": issue_id,
            "message": result["message"]
        }

    issue = result["issue"]

    description = issue["issue_description"]


    # ---------------------------------------
    # STEP 2: ANOMALY / CIVIC CHECK
    # ---------------------------------------

    anomaly_result = detect_civic_issue(
        description
    )


    # ---------------------------------------
    # STEP 3: STOP IF NOT CIVIC
    # ---------------------------------------

    if not anomaly_result.is_civic_issue:

        return {
            "success": True,
            "issue_id": issue_id,
            "issue_description": description,
            "is_civic_issue": False,
            "issue_category": None
        }


    # ---------------------------------------
    # STEP 4: THEMATIC RECOGNITION
    # ---------------------------------------

    theme_result = classify_issue(
        description
    )


    # ---------------------------------------
    # STEP 5: FINAL RESULT
    # ---------------------------------------

    return {
        "success": True,
        "issue_id": issue_id,
        "issue_description": description,
        "is_civic_issue": True,
        "issue_category": theme_result.issue_category
    }


if __name__ == "__main__":

    # Change this ID to test another issue
    issue_id = 1

    result = process_issue(issue_id)

    print("\n========== ISSUE ANALYSIS ==========\n")

    print(f"Issue ID       : {result['issue_id']}")
    print(f"Description    : {result.get('issue_description')}")
    print(f"Civic Issue    : {result.get('is_civic_issue')}")
    print(f"Issue Category : {result.get('issue_category')}")

    print("\n====================================\n")