from typing import Any, TypedDict

class AgentState(TypedDict, total=False):
    request: Any
    repository_context: str
    files_considered: list[str]
    issue_context: str
    analysis: str
    final_text: str
    warnings: list[str]
