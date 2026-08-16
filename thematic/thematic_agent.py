from dotenv import load_dotenv
from langchain_groq import ChatGroq

from .schemas import IssueCategory

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

thematic_agent = llm.with_structured_output(IssueCategory)


def classify_issue(issue_description: str) -> IssueCategory:

    prompt = f"""
You are a thematic pattern recognition agent for a civic issue system.

Your task is to identify the underlying civic problem described in the
report and assign it to ONE broad, reusable category.

Understand the meaning of the complete report rather than relying only
on individual keywords.

Examples:

Report:
"There is a huge pothole near my house."

Category:
Road Infrastructure


Report:
"The road outside my home is completely broken."

Category:
Road Infrastructure


Report:
"There are several deep cracks on the road."

Category:
Road Infrastructure


Report:
"Garbage has not been collected for five days."

Category:
Waste Management


Report:
"Waste is piling up beside the road."

Category:
Waste Management


Report:
"Several streetlights are not working."

Category:
Public Lighting


Report:
"The drainage near our house is blocked."

Category:
Drainage


Important rules:

1. Create a broad category representing the underlying civic problem.

2. Different descriptions of the same underlying problem should receive
the same category.

3. Do not include locations, names, dates, or individual details in
the category name.

4. Do not create overly specific categories.

Bad:
"Pothole Near My House"

Good:
"Road Infrastructure"

Bad:
"Garbage Near Patia Market"

Good:
"Waste Management"

5. Return exactly ONE category.

REPORT:
{issue_description}
"""

    return thematic_agent.invoke(prompt)