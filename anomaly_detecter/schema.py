from pydantic import BaseModel, Field


class CivicIssueCheck(BaseModel):
    is_civic_issue: bool = Field(
        description="True if the text describes a legitimate civic/public issue, otherwise False."
    )