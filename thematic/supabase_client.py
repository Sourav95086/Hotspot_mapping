import os

from dotenv import load_dotenv
from supabase import create_client, Client


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is not set")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is not set")


# ==========================================
# SUPABASE CLIENT
# ==========================================

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==========================================
# FETCH ISSUE
# ==========================================

def fetch_issue(issue_id: int):

    response = (
        supabase
        .table("issue_reports")
        .select(
            "issue_id, "
            "issue_description, "
            "issue_location"
        )
        .eq("issue_id", issue_id)
        .limit(1)
        .execute()
    )

    # --------------------------------------
    # ISSUE NOT FOUND
    # --------------------------------------

    if not response.data:

        return {
            "success": False,
            "message": f"Issue with ID {issue_id} not found",
            "issue": None
        }

    # --------------------------------------
    # ISSUE FOUND
    # --------------------------------------

    return {
        "success": True,
        "message": "Issue fetched successfully",
        "issue": response.data[0]
    }


# ==========================================
# LOCAL TEST ONLY
# ==========================================

if __name__ == "__main__":

    response = fetch_issue(1)

    print(response)