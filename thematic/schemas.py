from pydantic import BaseModel, Field


class IssueCategory(BaseModel):
    issue_category: str = Field(
        description="The broad, normalized category of the civic issue."
    )