from pydantic import BaseModel, Field

class AgentResponse(BaseModel):
    task_type: str
    summary: str
    analysis: str
    proposed_changes: list[str] = Field(default_factory=list)
    patch: str | None = None
    files_considered: list[str] = Field(default_factory=list)
    pull_request_url: str | None = None
    warnings: list[str] = Field(default_factory=list)
