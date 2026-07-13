from enum import StrEnum
from pydantic import BaseModel, Field, model_validator

class TaskType(StrEnum):
    ISSUE_FIX = "issue_fix"
    REPOSITORY_QA = "repository_qa"
    CODE_REVIEW = "code_review"
    BUG_TRIAGE = "bug_triage"
    DOCUMENTATION = "documentation"

class AgentRequest(BaseModel):
    task_type: TaskType
    instruction: str = Field(min_length=3, max_length=10000)
    repository_path: str | None = None
    github_owner: str | None = None
    github_repo: str | None = None
    issue_number: int | None = Field(default=None, ge=1)
    create_pull_request: bool = False

    @model_validator(mode="after")
    def validate_source(self):
        local_source = bool(self.repository_path)
        remote_source = bool(self.github_owner and self.github_repo)
        if not local_source and not remote_source:
            raise ValueError("Provide repository_path or both github_owner and github_repo.")
        if self.task_type == TaskType.ISSUE_FIX and remote_source and not self.issue_number:
            raise ValueError("issue_number is required for a remote issue_fix task.")
        return self
