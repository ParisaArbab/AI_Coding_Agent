from functools import lru_cache
from app.agents.graph import CodingAgent
from app.core.config import get_settings
from app.llm.factory import build_llm
from app.services.github_service import GitHubService
from app.services.repository_service import RepositoryService

@lru_cache
def get_agent() -> CodingAgent:
    settings = get_settings()
    return CodingAgent(settings, build_llm(settings), RepositoryService(settings), GitHubService(settings))
