from dotenv import load_dotenv
from langchain_groq import ChatGroq

from .schema import CivicIssueCheck

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

civic_agent = llm.with_structured_output(CivicIssueCheck)


def detect_civic_issue(issue_description: str) -> CivicIssueCheck:

    prompt = f"""
You are a civic issue detection agent.

Your ONLY task is to determine whether the given text describes
a legitimate civic or public issue.

A civic issue is a problem that affects public infrastructure,
public services, public spaces, the environment, transportation,
sanitation, utilities, or the local community.

Examples of civic issues:
- potholes or damaged roads
- garbage accumulation
- blocked drainage
- sewage overflow
- broken streetlights
- water supply problems
- traffic infrastructure problems
- damaged public facilities
- problems in public parks
- public cleanliness problems
- environmental problems affecting the community

Examples that are NOT civic issues:
- personal health problems
- stomach pain
- relationship problems
- personal requests
- shopping requests
- casual conversation
- jokes
- general questions
- unrelated personal problems

Do NOT classify based only on keywords.
Understand the meaning and intent of the complete report.

Return TRUE only when the report represents a legitimate
civic/public issue.

REPORT:
{issue_description}
"""

    return civic_agent.invoke(prompt)