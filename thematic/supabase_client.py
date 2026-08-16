import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def fetch_issue(issue_id: int):

    response = (
        supabase
        .table("issue_reports")
        .select("issue_id, issue_description, issue_location")
        .eq("issue_id", issue_id)
        .maybe_single()
        .execute()
    )

    if response.data is None:
        return {
            "success": False,
            "message": f"Issue with ID {issue_id} not found",
            "issue": None
        }

    return {
        "success": True,
        "message": "Issue fetched successfully",
        "issue": response.data
    }

responce = fetch_issue(1)
print(responce)