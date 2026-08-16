from anomaly_agent import detect_civic_issue
from thematic.supabase_client import fetch_issue

tests = [
    
]


for description in tests:

    result = detect_civic_issue(description)

    print("\nREPORT:", description)
    print("IS CIVIC ISSUE:", result.is_civic_issue)